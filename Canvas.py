from Cam import Cam


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
        current_frame = init.canvas.capture()

        current_bgr = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        initial_bgr = cv2.cvtColor(self.initial_frame, cv2.COLOR_BGR2GRAY)

        ret, current_thresh = cv2.threshold(current_bgr, 127, 255, 0)
        ret, initial_tresh = cv2.threshold(initial_bgr, 127, 255, 0)

        difference_tresh = cv2.subtract(current_thresh, current_thresh)
        contours, hierarchy = cv2.findContours(difference_tresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.imshow("New frame 1", frame)

        width, height = frame.shape[:2]
        print("Width ", width, ", height ", height, "New Width ", new_width, ", new height ", new_height)
        new_width = (width * 4)
        new_height = (height * 4)

        frame2 = cv2.resize(frame, (new_width, new_height))
        frame3 = frame
        cv2.drawContours(frame3, [contours[0]], -1, (255, 0, 0), 3)
        frame3 = cv2.resize(frame, (new_width, new_height))

        cv2.imshow("New frame 2", frame2)
        cv2.imshow("New frame 3", frame3)
