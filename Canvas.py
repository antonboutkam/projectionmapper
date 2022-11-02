from Cam import Cam
from Source import Source
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

    def show_large(self, frame_name, frame):
        width, height = frame.shape[:2]
        new_width = (width * 1)
        new_height = (height * 1)
        # print("Width ", width, ", height ", height, "New Width ", new_width, ", new height ", new_height)
        large = cv2.resize(frame, (new_width, new_height))
        cv2.imshow(frame_name, large)

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
        self.monitor.add("Canvas cam perspective", projection_area_cam_perspective)

        gpu_mask = self.pre_processor.process(projection_area_cam_perspective.copy(), self.gui, self.monitor)
        mask = gpu_mask.download()
        self.monitor.add_gpu("Canvas mask", gpu_mask)
        if len(mask.shape) == 2:
            gpu_mask_color = cv2.cuda.cvtColor(gpu_mask, cv2.COLOR_GRAY2RGB)
        else:
            gpu_mask_color = gpu_mask

        video_source = self.source.frame()
        gpu_video_source = cv2.cuda_GpuMat()
        gpu_video_source.upload(video_source)

        if video_source.shape[2] == 1:
            gpu_video_source = cv2.cuda.cvtColor(gpu_video_source, cv2.COLOR_GRAY2RGB)

        mask_color = gpu_mask_color.download()
        if self.gui.video_size_mode == 0:
            gpu_video_mask_size = cv2.cuda.resize(gpu_video_source, (mask.shape[1], mask.shape[0]))
            mask_applied = np.where(mask_color[:, :] == [0, 0, 0], mask_color, gpu_video_mask_size.download())
        elif self.gui.video_size_mode == 1:
            # im, contours, hierarchy = cv2.findContours(gpu_mask.download(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            # Calculate image moments of the detected contour
            # M = cv2.moments(contours[0])
            # cont_center_x = round(M['m10'] / M['m00'])
            # cont_center_y = round(M['m01'] / M['m00'])
            (y, x) = np.where(mask == 255)
            (top_y, top_x) = (np.min(y), np.min(x))
            (bottom_y, bottom_x) = (np.max(y), np.max(x))
            width = bottom_x - top_x
            height = bottom_y - top_y
            gpu_video_scale_fit = cv2.cuda.resize(gpu_video_source, (width, height))
            video_scale_fit = gpu_video_scale_fit.download()
            video_positioning = np.zeros([mask.shape[0], mask.shape[1], 3], dtype=np.uint8)
            print("mask shape", mask.shape)
            print("video positioning shape", video_positioning.shape)
            print("video scale fit shape", video_scale_fit.shape)
            print('top_y', top_y, 'bottom_y', bottom_y, 'top_x', top_x, 'bottom_X', bottom_x)
            print('mask_applied[', top_y, ':', bottom_y, ', ', top_x, ':', bottom_x, '] = ', video_scale_fit.shape, ')')
            video_positioning[top_y:bottom_y, top_x:bottom_x] = video_scale_fit
            mask_applied = np.where(mask_color[:, :] == [0, 0, 0], mask_color, video_positioning)

        # print('mask color shape', mask_color.shape)
        # print('video source mask size shape', video_source_mask_size.shape)

        # print('mask applied shape', mask_applied.shape)
        self.monitor.add("Canvas mask applied", mask_applied)

        # full_canvas = np.zeros([mask.shape[1], mask.shape[0], 3], dtype=np.uint8)222s
        offset_x = (0 - math.ceil(self.gui.max_offset_x / 2)) + self.gui.offset_x
        offset_y = (0 - math.ceil(self.gui.max_offset_y / 2)) + self.gui.offset_y
        # top_y = self.top_y+offset_y
        # bottom_y = self.bottom_y+offset_y + 1
        # top_x = self.top_x+offset_x
        # bottom_x = self.bottom_x+offset_x + 1

        # print('topy', top_y)
        # print('bottomy', bottom_y)
        # print('topx', top_x)
        # print('bottomx', bottom_x)
        # print('mask shape', mask_applied)
        full_canvas = np.zeros_like(current_frame)
        # mask_cutout = self._white_frame[top_y:bottom_y + 1, top_x:bottom_x + 1]

        h = mask.shape[0]
        w = mask.shape[1]

        if offset_y > 0:
            src_top_y = 0
            src_bottom_y = h - offset_y
            dest_top_y = offset_y
            dest_bottom_y = h
        else:
            src_top_y = 0 - offset_y  # offset_y is negatief, als offset_y -20 is dan is het min min 20 oftewel plus 20
            src_bottom_y = h
            dest_top_y = 0
            dest_bottom_y = h + offset_y  # offset_y is dus negatief, gaan andere kant op

        if offset_x > 0:
            src_top_x = 0
            src_bottom_x = w - offset_x
            dest_top_x = offset_x
            dest_bottom_x = w
        else:
            src_top_x = 0 - offset_x
            src_bottom_x = w
            dest_top_x = 0
            dest_bottom_x = w + offset_x


        full_canvas[dest_top_y:dest_bottom_y, dest_top_x:dest_bottom_x] = mask_applied[src_top_y:src_bottom_y,
                                                                          src_top_x:src_bottom_x]
        # full_canvas[10:300, 0:400] = mask_applied[0:290, 0:400]
        # full_canvas[-10:300, 0:400] = mask_applied[0:290, 0:400]

        if self.gui.replace_black:
            # Find all black pixels
            black_pixels = np.where(
                (full_canvas[:, :, 0] == 0) &
                (full_canvas[:, :, 1] == 0) &
                (full_canvas[:, :, 2] == 0)
            )
            # set those pixels to whatever value is configured
            full_canvas[black_pixels] = [self.gui.replace_black, self.gui.replace_black, self.gui.replace_black]

        # out = picture[self.top_y:self.bottom_y + 1, self.top_x:self.bottom_x + 1]
        # mask_resized = cv2.resize(mask, (768, 1024))
        # mask_resized_color = cv2.cvtColor(mask_resized, cv2.COLOR_GRAY2RGB)

        self.monitor.add("Result", full_canvas)
        full_canvas = cv2.resize(full_canvas, (projector.screen_res[0], projector.screen_res[1]))
        self.monitor.add("Result resized", full_canvas)
        #        out = np.where(input_source_rect[:, :] == [0, 0, 0], input_source_rect, mask)
        # out = np.where(mask_resized_color[:, :] == [0, 0, 0], mask_resized_color, input_source_rect)
        # self.monitor.add("Out", out)
        self.monitor.display()
        projector.draw(full_canvas)
