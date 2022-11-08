from Cam import Cam
from Source import Source
from File import File
from PreProcessor import PreProcessor
from Monitor import Monitor
import cv2
import numpy as np
import cupy as cp
import math


class Canvas:
    top_y = None
    top_x = None
    bottom_y = None
    bottom_x = None
    cam = None
    gui = None
    initial_frame = None
    pre_processor = None
    projector = None
    monitor = None
    source = None
    resized_source_videos = None

    def init(self, top_y, bottom_y, top_x, bottom_x, initial_frame, gui, cam, monitor):
        self.top_y = top_y
        self.bottom_y = bottom_y
        self.top_x = top_x
        self.bottom_x = bottom_x
        self.cam = cam
        self.initial_frame = initial_frame
        self.gui = gui
        self.pre_processor = PreProcessor()
        self.monitor = monitor
        self.source = Source()
        self.source.start(gui)

    def capture(self):
        # print("Capture")
        picture = self.cam.picture()
        out = picture[self.top_y:self.bottom_y + 1, self.top_x:self.bottom_x + 1]
        return out

    def _get_input(self, current_frame):
        if self.gui.input_source == 0:
            # print("Using current frame as input")
            input_source = current_frame
        elif self.gui.input_source == 1:
            # print("Using initial frame - current frame as input")
            input_source = cv2.subtract(self.initial_frame, current_frame)
        else:
            # print("Using current frame  - initial frame as input")
            input_source = cv2.subtract(current_frame, self.initial_frame)
        return input_source

    def play(self, projector):

        current_frame = self.capture()
        projection_area_cam_perspective = self._get_input(current_frame)
        self.monitor.add("Input", projection_area_cam_perspective)

        gpu_pre_processed_mask = self.pre_processor.process(projection_area_cam_perspective, self.gui, self.monitor)
        pre_processed_mask = gpu_pre_processed_mask.download()

        mask_list = self.extract_mask_list(gpu_pre_processed_mask, projection_area_cam_perspective)

        if len(pre_processed_mask.shape) == 2:
            gpu_full_mask_color = cv2.cuda.cvtColor(gpu_pre_processed_mask, cv2.COLOR_GRAY2RGB)
        else:
            gpu_full_mask_color = gpu_pre_processed_mask

        video_source = self.source.frame()
        self.monitor.add("Source " + str(self.gui.video_source), video_source)
        gpu_video_source = cv2.cuda_GpuMat()
        gpu_video_source.upload(video_source)

        if video_source.shape[2] == 1:
            gpu_video_source = cv2.cuda.cvtColor(gpu_video_source, cv2.COLOR_GRAY2RGB)
        mask_color = gpu_full_mask_color.download()
        video_positioned = np.zeros_like(current_frame)
        mask_applied = np.zeros_like(mask_color)
        self.resized_source_videos = []
        for index, current_mask in enumerate(mask_list):
            if self.gui.video_size_mode == 0:
                gpu_video_mask_size = cv2.cuda.resize(gpu_video_source,
                                                      (current_frame.shape[1], current_frame.shape[0]))
                mask_applied = np.where(mask_color[:, :] == [0, 0, 0], mask_color, gpu_video_mask_size.download())
            elif self.gui.video_size_mode == 1:
                # im, contours, hierarchy = cv2.findContours(gpu_mask.download(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                # Calculate image moments of the detected contour
                # M = cv2.moments(contours[0])
                # cont_center_x = round(M['m10'] / M['m00'])
                # cont_center_y = round(M['m01'] / M['m00'])

                (y, x) = np.where(current_mask == 255)

                (top_y, top_x) = (np.min(y), np.min(x))
                (bottom_y, bottom_x) = (np.max(y), np.max(x))
                width = bottom_x - top_x
                height = bottom_y - top_y
                if width < 3 or height < 3:
                    # print('to small' , width, height)
                    continue
                # print('width', width, 'height', height)
                gpu_video_scale_fit = cv2.cuda.resize(gpu_video_source, (width, height))
                video_scale_fit = gpu_video_scale_fit.download()
                # self.monitor.add("VScal2Fit " + str(index), video_scale_fit)
                video_positioned[top_y:bottom_y, top_x:bottom_x] = video_scale_fit

        mask_count = len(mask_list)
        # self.monitor.add(str(mask_count) + " clip merge", video_positioned)
        if self.gui.video_size_mode == 1:
            mask_applied = np.where(mask_color[:, :] == [0, 0, 0], mask_color, video_positioned)

        # print('mask color shape', mask_color.shape)
        # print('video source mask size shape', video_source_mask_size.shape)

        # print('mask applied shape', mask_applied.shape)
        self.monitor.add("Clips masked", mask_applied)

        offset_x = (0 - math.ceil(self.gui.max_offset_x / 2)) + self.gui.offset_x
        offset_y = (0 - math.ceil(self.gui.max_offset_y / 2)) + self.gui.offset_y

        full_canvas = np.zeros_like(current_frame)

        h = pre_processed_mask.shape[0]
        w = pre_processed_mask.shape[1]

        if offset_y > 0:
            src_top_y = 0
            src_bottom_y = h - offset_y
            dst_top_y = offset_y
            dst_bottom_y = h
        else:
            src_top_y = 0 - offset_y  # offset_y is negatief, als offset_y -20 is dan is het min min 20 oftewel plus 20
            src_bottom_y = h
            dst_top_y = 0
            dst_bottom_y = h + offset_y  # offset_y is dus negatief, gaan andere kant op

        if offset_x > 0:
            src_top_x = 0
            src_bottom_x = w - offset_x
            dst_top_x = offset_x
            dst_bottom_x = w
        else:
            src_top_x = 0 - offset_x
            src_bottom_x = w
            dst_top_x = 0
            dst_bottom_x = w + offset_x

        mask_applied_offsets = mask_applied[src_top_y:src_bottom_y, src_top_x:src_bottom_x]
        full_canvas[dst_top_y:dst_bottom_y, dst_top_x:dst_bottom_x] = mask_applied_offsets

        if self.gui.replace_black:
            # Find all black pixels
            black_pixels = np.where(
                (full_canvas[:, :, 0] == 0) &
                (full_canvas[:, :, 1] == 0) &
                (full_canvas[:, :, 2] == 0)
            )
            # set those pixels to whatever value is configured
            full_canvas[black_pixels] = [self.gui.replace_black, self.gui.replace_black, self.gui.replace_black]

        self.monitor.add("Result", full_canvas)
        full_canvas = cv2.resize(full_canvas, (projector.screen_res[0], projector.screen_res[1]))
        self.monitor.add("Final result", full_canvas)
        self.monitor.display()
        projector.draw(full_canvas)

    def extract_mask_list(self, gpu_mask, current_frame):
        file = File()
        file.start(self.gui)

        mask_list = []
        if self.gui.find_contour_enable == 1:
            root_contours = []
            root_contour_idx = []

            self.monitor.add_gpu("Extract Input", gpu_mask)
            base_mask = gpu_mask.download()
            # print("Seeking contours ")
            all_contours, hierarchy = cv2.findContours(base_mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            all_contours_img = cv2.drawContours(current_frame, all_contours, -1, (0, 0, 255), 3)
            self.monitor.add("All contours", all_contours_img)

            blank_mask = np.zeros_like(base_mask)
            for index, contour in enumerate(all_contours[self.gui.draw_contour_min:self.gui.draw_contour_max]):
                # poly_contour = cv2.approxPolyDP(contour, 0.3 * cv2.arcLength(contour, True), True)
                drawn_mask = blank_mask.copy()

                if self.gui.approx_poly:
                    contour = cv2.approxPolyDP(contour, self.gui.approx_poly_precision/1000 * cv2.arcLength(contour, True), True)
                    file.append('approxPolyDP-' + str(index) + '.txt', contour)

                if self.gui.hull:
                    contour = cv2.convexHull(contour)
                    file.append('convexHull-' + str(index) + '.txt', contour)

                cv2.fillConvexPoly(contour, contour, 255)

                # area = cv2.contourArea(contour)
                # self.monitor.add("Contour " + str(index), drawn_mask)
                mask_list.append(drawn_mask)
        else:
            # print("Find contours disabled")
            mask_list.append(gpu_mask.download())
        return mask_list
