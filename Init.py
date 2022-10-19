from Projector import Projector
from Cam import Cam
import cv2

class Init:
    initialized = False
    _white_frame = None
    _black_frame = None

    def run(self, running_time):
        projector = Projector()
        cam = Cam()

        if running_time < 5:
            projector.white()
            self._white_frame = cam.picture()
        elif running_time < 8:
            projector.black()
            self._black_frame = cam.picture()
        else:
            white = cv2.cvtColor(self._white_frame, cv2.COLOR_BGR2GRAY)
            black = cv2.cvtColor(self._black_frame, cv2.COLOR_BGR2GRAY)

            ret, thresh = cv2.threshold(white, 127, 255, 0)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            cv2.drawContours(black, contours, 0, (0, 255, 0), 3)

            # compute difference
            difference = cv2.subtract(white, black)

            white_small = cv2.resize(white, (800, 800), interpolation=cv2.INTER_AREA)
            black_small = cv2.resize(black, (800, 800), interpolation=cv2.INTER_AREA)
            difference_small = cv2.resize(difference, (800, 800), interpolation=cv2.INTER_AREA)

            cv2.imshow("White", white_small)
            cv2.imshow("Black", black_small)
            cv2.imshow("Difference", difference_small)




