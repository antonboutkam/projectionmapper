from Projector import Projector
from Canvas import Canvas
from Cam import Cam
import cv2
import numpy as np


class Init:
    initialized = False
    _white_frame = None
    _black_frame = None
    contours_ = None
    canvas = None

    def run(self, running_time):
        projector = Projector()
        cam = Cam()

        if running_time < 5:
            projector.white()
            self._white_frame = cam.picture()
        elif running_time < 9:
            projector.black()
            self._black_frame = cam.picture()
        else:
            white_fullcolor = np.copy(self._white_frame)
            white_bgr = cv2.cvtColor(self._white_frame, cv2.COLOR_BGR2GRAY)
            black_bgr = cv2.cvtColor(self._black_frame, cv2.COLOR_BGR2GRAY)

            # compute difference
            difference = cv2.subtract(white_bgr, black_bgr)

            print('tracing contours')
            ret, thresh = cv2.threshold(difference, 127, 255, 0)

            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            print(len(contours))
            # Create mask where white is what we want, black otherwise
            mask = np.zeros_like(white_bgr)


            # -----------------
            sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

            largest_contour = sorted_contours[0]

            # ------------
            cv2.drawContours(mask, largest_contour, -1, 255, -1)
            cv2.drawContours(white_fullcolor, largest_contour, -1, (255, 0, 0), 5)

            # cv2.drawContours(self._black_frame, contours, -1, (128, 255, 0), cv2.LINE_4)
            # white_small = cv2.resize(white_fullcolor, (800, 800), interpolation=cv2.INTER_AREA)
            # black_small = cv2.resize(self._black_frame, (800, 800), interpolation=cv2.INTER_AREA)
            # difference_small = cv2.resize(difference, (800, 800), interpolation=cv2.INTER_AREA)


            # cv2.imshow("Black", black_small)
            # cv2.imshow("Difference", difference_small)

            # Extract out the object and place into output image
            out = np.zeros_like(white_bgr)
            out[mask == 255] = white_bgr[mask == 255]

            # Now crop
            (y, x) = np.where(mask == 255)
            (top_y, top_x) = (np.min(y), np.min(x))
            (bottom_y, bottom_x) = (np.max(y), np.max(x))
            out = self._white_frame[top_y:bottom_y + 1, top_x:bottom_x + 1]

            # Show the output image
            cv2.imshow("White", white_fullcolor)
            # cv2.imshow('Cam area', out)
            projector = Projector()
            projector.white()
            self.canvas = Canvas()
            self.canvas.init(top_y, bottom_y, top_x, bottom_x, out)
            self.initialized = True





