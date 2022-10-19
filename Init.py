from Projector import Projector
from Cam import Cam
import cv2
import numpy as np


class Init:
    initialized = False
    _white_frame = None
    _black_frame = None
    contours_ = None

    def run(self, running_time):
        projector = Projector()
        cam = Cam()

        if running_time < 3:
            projector.white()
            self._white_frame = cam.picture()
        elif running_time < 6:
            projector.black()
            self._black_frame = cam.picture()
        else:
            main_white_frame = np.copy(self._white_frame);
            white = cv2.cvtColor(self._white_frame, cv2.COLOR_BGR2GRAY)
            black = cv2.cvtColor(self._black_frame, cv2.COLOR_BGR2GRAY)

            # compute difference
            difference = cv2.subtract(white, black)

            print('tracing contours')
            ret, thresh = cv2.threshold(difference, 127, 255, 0)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            print(len(contours))
            cv2.drawContours(main_white_frame, [contours[0]], -1, (128, 255, 0), 1)


            # cv2.drawContours(self._black_frame, contours, -1, (128, 255, 0), cv2.LINE_4)
            white_small = cv2.resize(main_white_frame, (800, 800), interpolation=cv2.INTER_AREA)
            # black_small = cv2.resize(self._black_frame, (800, 800), interpolation=cv2.INTER_AREA)
            difference_small = cv2.resize(difference, (800, 800), interpolation=cv2.INTER_AREA)

            cv2.imshow("White", white_small)
            # cv2.imshow("Black", black_small)
            cv2.imshow("Difference", difference_small)




