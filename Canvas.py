from Cam import Cam
from Projector import Projector
import cv2
import numpy as np

class Canvas:
    top_y = None
    top_x = None
    bottom_y = None
    bottom_x = None
    cam = None
    initial_frame = None

    def init(self, top_y, bottom_y, top_x, bottom_x, initial_frame):
        self.top_y = top_y
        self.bottom_y = bottom_y
        self.top_x = top_x
        self.bottom_x = bottom_x
        self.cam = Cam()
        self.initial_frame = initial_frame

    def capture(self):
        picture = self.cam.picture()
        out = picture[self.top_y:self.bottom_y + 1, self.top_x:self.bottom_x + 1]
        return out

    def show_large(self, frame_name, frame):
        width, height = frame.shape[:2]
        new_width = (width * 4)
        new_height = (height * 4)
        print("Width ", width, ", height ", height, "New Width ", new_width, ", new height ", new_height)
        large = cv2.resize(frame, (new_width, new_height))
        cv2.imshow(frame_name, large)

    def play(self):
        projector = Projector()
        current_frame = self.capture()


        low_blue = np.array([90, 150, 0])
        high_blue = np.array([150, 255, 255])

        # convert BGR to HSV
        current_frame_hsv = cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV)
        color_mask = 255 - cv2.inRange(current_frame_hsv, low_blue, high_blue)
        current_frame_without_blue = cv2.bitwise_and(current_frame, current_frame, mask=color_mask)



        # vret, current_thresh = cv2.threshold(current_bgr, 127, 255, 0)
        # ret, initial_tresh = cv2.threshold(initial_bgr, 127, 255, 0)

        difference = cv2.subtract(self.initial_frame, current_frame)
        difference_reverse = cv2.subtract(current_frame, self.initial_frame)

        current_bgr = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        initial_bgr = cv2.cvtColor(self.initial_frame, cv2.COLOR_BGR2GRAY)
        difference_bgr = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

        # self.show_large("Current tresh", current_thresh)
        # self.show_large("Initial tresh", initial_tresh)
        self.show_large("Current bgr", current_bgr)
        self.show_large("Current frame no blue", current_frame_without_blue)
        self.show_large("Original new frame", current_frame)
        self.show_large("Diff", difference)
        self.show_large("Diff reverse", difference)


        frame4 = current_frame
        ret, current_tresh = cv2.threshold(current_bgr, 127, 255, 0)
        curr_contours, hierarchy = cv2.findContours(current_tresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        out = np.zeros_like(current_frame)
        out.fill(255)

        contour_count = len(curr_contours)

        if contour_count > 0 :
            sorted_contours = sorted(curr_contours, key=cv2.contourArea, reverse=True)
            largest_contour = sorted_contours[0]
            cv2.drawContours(out, largest_contour, -1, (0, 0, 255), 2)
            cv2.drawContours(frame4, largest_contour, -1, (0, 0, 255), 2)

        self.show_large("Diff contours 1", frame4)
        self.show_large("Frame 4", cv2.flip(frame4, 0))
        self.show_large("Out", cv2.flip(out, 0))
        projector.draw(out)

