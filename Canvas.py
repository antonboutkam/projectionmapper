from Cam import Cam
from Projector import Projector
from PreProcessor import PreProcessor
from Monitor import Monitor
from Gui import Gui
import cv2
import numpy as np


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

    def init(self, top_y, bottom_y, top_x, bottom_x, initial_frame, gui):
        self.top_y = top_y
        self.bottom_y = bottom_y
        self.top_x = top_x
        self.bottom_x = bottom_x
        self.cam = Cam()
        self.initial_frame = initial_frame
        self.gui = gui
        self.gui.show()
        self.pre_processor = PreProcessor()
        self.monitor = Monitor()

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

    def play(self):
        projector = Projector()
        current_frame = self.capture()
        input_source = self._get_input(current_frame)
        input_preprocessed = self.pre_processor.process(input_source.copy(), self.gui, self.monitor)

        contour_info = list()
        detected_contours, hierarchy = cv2.findContours(input_preprocessed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contour_count = len(detected_contours)
        output = preview = current_frame

        height, width = input_preprocessed.shape[:2]
        mask = np.zeros((height, width), np.uint8)

        if contour_count > 0:
            print("Contour count ", contour_count)
            # cv2.resize(mask, (width, height))
            for ci in detected_contours[self.gui.draw_contour_min:self.gui.draw_contour_max]:
                # print("area ", cv2.contourArea(ci))
                hull = cv2.convexHull(ci)
                cv2.fillConvexPoly(mask, hull, 255)
            # mask = cv2.dilate(mask, None, iterations=10)
            # mask = cv2.erode(mask, None, iterations=10)
            # mask = cv2.GaussianBlur(mask, (5, 5), 0)
            # mask_stack = np.dstack([mask] * 3)
            # mask_stack = mask_stack.astype('float32') / 255.0

            self.monitor.add("Mask", output)

            # detected_contours = sorted(detected_contours, key=cv2.contourArea, reverse=True)

            print(detected_contours)
            cv2.drawContours(preview, detected_contours[self.gui.draw_contour_min:self.gui.draw_contour_max], -1, (self.gui.contour_b, self.gui.contour_g, self.gui.contour_r),
                             self.gui.contour_thickness)
            cv2.drawContours(mask, detected_contours[self.gui.draw_contour_min:self.gui.draw_contour_max], -1, (self.gui.contour_b, self.gui.contour_g, self.gui.contour_r),
                             self.gui.contour_thickness)

            # print("Current frame COLOR 0", current_frame[0])
            # print("Current frame BGR 0", input_source[0])

            # self.monitor.add("Original", current_frame)
            # self.monitor.add("Input BGR", input_source)

            self.show_large("Input GRAY", input_preprocessed)
            self.show_large("Original + contours", preview)
            # self.monitor.add("Output", output)

        self.monitor.display()

        mask_contents = cv2.imread('./assets/testbeeld-1024x768.jpg')
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        mask = cv2.resize(mask, (1024, 768));

        mask = np.where(mask_contents[:, :] == [0, 0, 0], mask_contents, mask)

        projector.draw(mask)
