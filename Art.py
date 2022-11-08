import cv2


class Art:
    def draw_coolness(self, canvas, contours):
        for contour in contours:
            canvas = self.draw_skip_lines(canvas, contour, 2, (0, 255, 0), 1)
            canvas = self.draw_skip_lines(canvas, contour, 2, (255, 0, 0), 1)
        return canvas

    def draw_skip_lines(self, canvas, contour, step, color, thickness):
        n = contour.ravel()
        i = 0
        lines = []
        prev_x = None
        prev_y = None
        for j in n:
            if i > start:
                continue
            if (i % step) == 0:
                x = n[i]
                y = n[i + 1]

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
