from Cam import Cam
from Source import Source
from PreProcessor import PreProcessor
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
        self.monitor.add("Cam perspective", projection_area_cam_perspective)
        #projection_area_cam_perspective = cv2.resize(projection_area_cam_perspective, (projector.screen_res[0], projector.screen_res[1]))
        mask = self.pre_processor.process(projection_area_cam_perspective.copy(), self.gui, self.monitor)
        self.monitor.add("Mask", projection_area_cam_perspective)

        self.monitor.display()
        video_source = self.source.frame()

        mask_color = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        print('mask color shape', mask_color.shape)
        # input_source_rect = input_source[0:1024, 0:768]
        if video_source.shape[2] == 1:
            video_source = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        video_source_mask_size = cv2.resize(video_source, (mask.shape[1], mask.shape[0]))
        print('mask color shape', mask_color.shape)
        print('video source mask size shape', video_source_mask_size.shape)
        mask_applied = np.where(mask_color[:, :] == [0, 0, 0], mask_color, video_source_mask_size)
        print('mask applied shape', mask_applied.shape)
        self.monitor.add("Mask applied", projection_area_cam_perspective)

        full_canvas = np.zeros([mask.shape[1], mask.shape[0], 3], dtype=np.uint8)
        offset_x = (0 - math.ceil(self.gui.max_offset_x / 2)) + self.gui.offset_x
        offset_y = (0 - math.ceil(self.gui.max_offset_y / 2)) + self.gui.offset_y
        top_y = self.top_y+offset_y
        bottom_y = self.bottom_y+offset_y + 1
        top_x = self.top_x+offset_x
        bottom_x = self.bottom_x+offset_x + 1

        print('topy', top_y)
        print('bottomy', bottom_y)
        print('topx', top_x)
        print('bottomx', bottom_x)
        print('mask shape', mask_applied)
        full_canvas = np.zeros_like(current_frame)
        full_canvas = mask_applied
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
        full_canvas = cv2.resize(full_canvas, (self.projector.screen_res[0], self.projector.screen_res[1]))
        self.monitor.add("Result resized", full_canvas)
#        out = np.where(input_source_rect[:, :] == [0, 0, 0], input_source_rect, mask)
        # out = np.where(mask_resized_color[:, :] == [0, 0, 0], mask_resized_color, input_source_rect)
        # self.monitor.add("Out", out)
        projector.draw(full_canvas)
