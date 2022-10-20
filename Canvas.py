from Cam import Cam
from Projector import Projector
import cv2

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

        current_bgr = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        initial_bgr = cv2.cvtColor(self.initial_frame, cv2.COLOR_BGR2GRAY)

        # vret, current_thresh = cv2.threshold(current_bgr, 127, 255, 0)
        # ret, initial_tresh = cv2.threshold(initial_bgr, 127, 255, 0)

        difference_bgr = cv2.subtract(initial_bgr, current_bgr)

        # self.show_large("Current tresh", current_thresh)
        # self.show_large("Initial tresh", initial_tresh)
        self.show_large("Original new frame", current_frame)
        self.show_large("Diff bgr", difference_bgr)

        frame4 = current_frame
        ret, difference_tresh = cv2.threshold(difference_bgr, 127, 255, 0)
        diff_contours, hierarchy = cv2.findContours(difference_tresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame4, diff_contours, -1, (0, 255, 0), 3)
        self.show_large("Diff contours 1", frame4)

        projector.draw(frame4)

