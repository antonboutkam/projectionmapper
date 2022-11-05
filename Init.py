import cv2
import numpy as np
from Canvas import Canvas
from Monitor import Monitor


class Init:
    initialized = False
    _white_frame = None
    _black_frame = None
    contours_ = None
    canvas = None

    def run(self, running_time, gui, projector, cam):

        print("runnning time", running_time)
        if running_time < 2:
            # Moves the window in position
            projector.light(gui.calibration_luminosity)
            print("picture")
            self._white_frame = cam.picture()
        elif running_time < 3:
            print("wait black")
            projector.black()
        else:
            print("calibrate 1")
            # cv2.imshow("White", self._white_frame)
            white_fullcolor = np.copy(self._white_frame)
            print("source shape: ", white_fullcolor.shape)
            white_bgr = cv2.cvtColor(self._white_frame, cv2.COLOR_BGR2GRAY)
            print("calibrate 2")
#            white_bgr = cv2.GaussianBlur(white_bgr, (5, 5), 0)
            print("start thresh")
            ret, thresh = cv2.threshold(white_bgr, gui.calibration_threshold, 255, cv2.THRESH_BINARY)
            print("start comt")
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contour_count = len(contours)
            print("Found ", contour_count, "  during init state")

            if contour_count == 0:
                gui.calibration_threshold = gui.calibration_threshold + 1
                return None

            # Create mask where white is what we want, black otherwise
            mask = np.zeros_like(white_bgr)
            # -----------------
            print("sort")
            sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
            largest_contour = sorted_contours[0]

            # ------------
            print("draw largest")
            cv2.drawContours(mask, largest_contour, -1, 255, -1)

            if gui.calibration_show_found_contours:
                print("show found")
                cv2.drawContours(white_fullcolor, largest_contour, -1, (255, 0, 0), 3)
                # for contour in contours:
                #    cv2.drawContours(white_fullcolor, contour, -1, (randrange(255), randrange(255), randrange(255)), 3)

            if gui.calibration_convex_hull:
                print("show convex 10")
                for contour in contours[0:10]:
                    hull = cv2.convexHull(contour)
                    cv2.fillConvexPoly(white_fullcolor, hull, 255)

            # @todo, volgens mij heeft deze regel geen nut
            mask_cutout = np.zeros_like(white_bgr)
            mask_cutout[mask == 255] = white_bgr[mask == 255]

            # Now crop
            (y, x) = np.where(mask == 255)
            (top_y, top_x) = (np.min(y), np.min(x))
            (bottom_y, bottom_x) = (np.max(y), np.max(x))
            # print(top_y, ':', (bottom_y + 1), ', ', top_x, ':', (bottom_x + 1))
            mask_cutout = self._white_frame[top_y:bottom_y + 1, top_x:bottom_x + 1]

            width = bottom_x - top_x
            height = bottom_y - top_y
            aspect_ratio = width / height
            monitor = Monitor()
            monitor.start(gui, aspect_ratio)

            print("aspect ratio: " + str(aspect_ratio))
            # Show the output image
            if gui.calibration_show_input_source:
                monitor.add("Source", white_fullcolor)

            # cv2.imshow("WhiteBGR", white_bgr)
            if gui.calibration_show_threshold:
                monitor.add("Threshold", thresh)

            if gui.calibration_show_project_cutout:
                monitor.add("Cutout", mask_cutout)

            self.canvas = Canvas()
            # print("INit canvas")
            print("Initialization complete")
            self.canvas.init(top_y, bottom_y, top_x, bottom_x, mask_cutout, gui, cam, monitor)
            self.initialized = True
