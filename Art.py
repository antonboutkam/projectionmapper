import cv2
import numpy as np
import colorsys

class Art:
    center_h = 0



    def draw_coolness(self, canvas, contours):
        for contour in contours:
            canvas = self.draw_skip_lines(canvas, contour, 2, (0, 255, 0), 1, 0)
            # canvas = self.draw_skip_lines(canvas, contour, 3, (0, 255, 0), 1, 2)

            # compute the center of the contour
            M = cv2.moments(contour)
            c_x = int(M["m10"] / M["m00"])
            c_y = int(M["m01"] / M["m00"])
            self.center_h = self.center_h + 10
            if self.center_h > 255:
                self.center_h = 0

            color = colorsys.hsv_to_rgb(self.center_h, 255, 255)
            canvas = self.draw_center_lines(canvas, contour, c_x, c_y, color, 1)
        return canvas

    def draw_center_lines(self, canvas, contour, center_x, center_y, color, thickness):
        n = contour.ravel()
        i = 0
        it = 0
        for j in n:
            if (i % 2) == 0:
                x = n[i]
                y = n[(i + 1)]
                it = it + 1
                if (it % 5) == 0:
                    cv2.line(canvas, (center_x, center_y), (x, y), color, thickness)

            i = i + 1

        return canvas

    def draw_skip_lines(self, canvas, contour, step, color, thickness, start):
        n = contour.ravel()
        i = 0
        lines = []
        prev_x = None
        prev_y = None

        for j in n:
            if (i % step) == 0:
                x = n[i]
                y = n[(i + 1)]

                if prev_x is None:
                    prev_x = x
                    prev_y = y
                    continue
                else:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), color, thickness)
                    prev_x = x
                    prev_y = y
            i = i + 1

        return canvas
