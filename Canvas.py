from Cam import Cam
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

    def play(self):
        current_frame = self.capture()

        current_bgr = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        initial_bgr = self.initial_frame # is al bgr

        ret, current_thresh = cv2.threshold(current_bgr, 127, 255, 0)
        ret, initial_tresh = cv2.threshold(initial_bgr, 127, 255, 0)

        cv2.imshow("Current tresh", current_thresh)
        cv2.imshow("Initial tresh", initial_tresh)

        difference_tresh = cv2.subtract(current_thresh, initial_tresh)
        difference_tresh_reverse = cv2.subtract(current_thresh, initial_tresh)
        contours, hierarchy = cv2.findContours(difference_tresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.imshow("Difference tresh", difference_tresh)
        cv2.imshow("Difference tresh reverse", difference_tresh_reverse)

        cv2.imshow("New frame 1", current_frame)

        width, height = current_frame.shape[:2]
        new_width = (width * 4)
        new_height = (height * 4)

        print("Width ", width, ", height ", height, "New Width ", new_width, ", new height ", new_height)

        frame2 = cv2.resize(current_frame, (new_width, new_height))
        frame3 = current_frame
        cv2.drawContours(frame3, contours, -1, (255, 0, 0), 3)
        frame3 = cv2.resize(current_frame, (new_width, new_height))

        cv2.imshow("New frame 2", frame2)
        cv2.imshow("New frame 3", frame3)
