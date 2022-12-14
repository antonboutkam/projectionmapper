from Cam import Cam
from Source import Source
from Manipulation import Manipulation
from File import File
from PreProcessor import PreProcessor
from Art import Art
from Monitor import Monitor
import cv2
import numpy as np
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
    simple_contours = []
    art = None

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
        self.art = Art()

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
        if len(mask_list) > 0:
            mask_applied = np.zeros_like(mask_list[0])
        else:
            print("No masks found")
            mask_applied = np.zeros_like(pre_processed_mask)

        mask_applied_rev = mask_applied.copy()
        black_mask_rgb = np.zeros_like(mask_color)
        video_positioned = black_mask_rgb.copy()
        self.resized_source_videos = []
        scale_locked = False
        locked_scale = []
        file = File()
        for index, current_mask in enumerate(mask_list):
            if self.gui.video_size_mode == 0:
                self.monitor.add("MASK", current_mask)
                gpu_video_mask_size = cv2.cuda.resize(gpu_video_source,
                                                      (current_frame.shape[1], current_frame.shape[0]))
                video_positioned = gpu_video_mask_size.download()
            elif self.gui.video_size_mode > 0:
                if self.gui.video_size_mode == 1 or scale_locked is False:
                    (y, x) = np.where(current_mask == 255)
                    if len(y) == 0 or len(x) == 0:
                        continue
                    (top_y, top_x) = (np.min(y), np.min(x))
                    (bottom_y, bottom_x) = (np.max(y), np.max(x))
                    width = bottom_x - top_x
                    height = bottom_y - top_y
                    locked_scale.append((y, x, top_y, top_x, bottom_y, bottom_y, width, height))
                else: # self.gui.video_size_mode == 2 and scale_locked is True:
                    (y, x, top_y, top_x, bottom_y, bottom_y, width, height) = locked_scale[index]

                if self.gui.main_log_stuff:
                    print("Current mask shape", current_mask.shape)
                    print("Current mask", current_mask)
                    print("X", x, "y", y)

                if width < 3 or height < 3:
                    # print('to small' , width, height)
                    continue

                # print('width', width, 'height', height)
                gpu_video_scale_fit = cv2.cuda.resize(gpu_video_source, (width, height))
                video_scale_fit = gpu_video_scale_fit.download()
                # self.monitor.add("VScal2Fit " + str(index), video_scale_fit)
                video_positioned[top_y:bottom_y, top_x:bottom_x] = video_scale_fit

            current_mask_rgb = cv2.cvtColor(current_mask, cv2.COLOR_GRAY2RGB)
            mask_applied_rev = np.where(current_mask[:, :] == [0, 0, 0], current_mask, mask_applied)
            mask_applied = np.where(current_mask[:, :] == [0, 0, 0], mask_applied_rev, current_mask)
            self.monitor.add("MSK_MG" + str(index), mask_applied)
            self.monitor.add("MSK_RMG" + str(index), mask_applied_rev)

        self.monitor.add("VID_POS", video_positioned)
        self.monitor.add("MSK_CB", mask_applied)
        self.monitor.add("MSK_RCB", mask_applied_rev)
        mask_applied_rgb =  cv2.cvtColor(mask_applied, cv2.COLOR_GRAY2RGB)
        video_masked_rev = np.where(mask_applied_rgb[:, :] == [0, 0, 0], video_positioned, mask_applied_rgb)
        video_masked = np.where(mask_applied_rgb[:, :] == [0, 0, 0], mask_applied_rgb, video_positioned)

        # print('mask color shape', mask_color.shape)
        # print('video source mask size shape', video_source_mask_size.shape)

        # print('mask applied shape', mask_applied.shape)
        self.monitor.add("VID_MASKED", video_masked)
        self.monitor.add("VID_MASKED_REV", video_masked_rev)

        if len(self.simple_contours) > 0:
            self.art.draw_coolness(video_masked, self.simple_contours)

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

        mask_applied_offsets = video_masked[src_top_y:src_bottom_y, src_top_x:src_bottom_x]
        full_canvas[dst_top_y:dst_bottom_y, dst_top_x:dst_bottom_x] = mask_applied_offsets

        # Now rotate the image back if needed
        full_canvas = Manipulation.rotate(full_canvas, 0 - self.gui.calibration_rotate)

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
            all_contours = sorted(all_contours, key=cv2.contourArea, reverse=True)

            blank_mask = np.zeros_like(base_mask)
            blank_mask_rgb = cv2.cvtColor(blank_mask, cv2.COLOR_GRAY2RGB)
            self.simple_contours = []
            for index, contour in enumerate(all_contours[self.gui.draw_contour_min:self.gui.draw_contour_max]):
                # poly_contour = cv2.approxPolyDP(contour, 0.3 * cv2.arcLength(contour, True), True)
                draw_mask = blank_mask.copy()

                if self.gui.hull:
                    contour = cv2.convexHull(contour)
                    file.append('convexHull-' + str(index) + '.txt', contour)
                    preview = blank_mask_rgb.copy()
                    cv2.drawContours(preview, [contour], -1, (0, 255, 0), 2)
                    self.monitor.add('convexHull-' + str(index), preview)

                if self.gui.approx_poly:
                    contour = cv2.approxPolyDP(contour, self.gui.approx_poly_precision/100 * cv2.arcLength(contour, True), True)
                    file.append('approxPolyDP-' + str(index) + '.txt', contour)
                    preview = blank_mask_rgb.copy()
                    cv2.drawContours(preview, [contour], -1, (0, 0, 255), 2)
                    self.monitor.add('approxPolyDP-' + str(index), preview)

                cv2.fillConvexPoly(draw_mask, contour, 255)
                self.monitor.add("Draw mask" + str(index), draw_mask)

                if self.gui.simplify_contour:
                    contour = self.simplify_contour(contour)

                cv2.fillConvexPoly(draw_mask, contour, 255)
                self.monitor.add("Simple mask" + str(index), draw_mask)


                # area = cv2.contourArea(contour)
                # self.monitor.add("Contour " + str(index), drawn_mask)
                mask_list.append(draw_mask)
        else:
            # print("Find contours disabled")
            mask_list.append(gpu_mask.download())
        return mask_list

    def simplify_contour(self, contour):
        n = contour.ravel()
        i = 0
        prev_x = None
        prev_y = None
        simple_contour = []
        for j in n:
            if (i % 2) == 0:
                x = n[i]
                y = n[i + 1]

                if prev_x is None:
                    prev_x = x
                if prev_y is None:
                    prev_y = y

                dist = math.sqrt(math.pow(x - prev_x, 2) + math.pow(y - prev_y, 2))
                if dist > self.gui.simplify_contour_dist:
                    simple_contour.append([x, y])
            i = i + 1

        contour = np.array(simple_contour).reshape((-1, 1, 2)).astype(np.int32)
        self.simple_contours.append(contour)
        return contour
