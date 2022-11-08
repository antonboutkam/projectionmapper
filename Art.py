import cv2


class Art:
    def draw_coolness(self, canvas, contours):
        for contour in contours:
            canvas = self.draw_skip_lines(canvas, contour, 2, (0, 255, 0), 1, 0)
            canvas = self.draw_skip_lines(canvas, contour, 3, (255, 0, 0), 1, 2)
        return canvas

    def draw_skip_lines(self, canvas, contour, step, color, thickness, start):
        n = contour.ravel()
        i = 0
        lines = []
        prev_x = None
        prev_y = None
        while True:
            if i >= len(contour):
                break
            for j in n:
                if i < start:
                    i = i + 1
                    continue
                if (i % step) == 0:
                    x = n[i % len(contour)]
                    y = n[(i + 1) % len(contour)]

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
