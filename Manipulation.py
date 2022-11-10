import numpy as np
import cv2



class Manipulation:

    @staticmethod
    def rotate(self, frame, degrees):
        if degrees == 0:
            return frame
        (h, w) = frame.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        # rotate our image by 45 degrees around the center of the image
        M = cv2.getRotationMatrix2D((cX, cY), degrees, 1.0)
        return cv2.warpAffine(frame, M, (w, h))

    @staticmethod
    def color_reduction(frame_rgb, red, green, blue):
        if red > 0 or green > 0 or blue > 0:
            frame_black = np.zeros_like(frame_rgb)
            frame_black[..., [0]] = red
            frame_black[..., [1]] = green
            frame_black[..., [2]] = blue
            frame_rgb = frame_rgb.substract(frame_black)
        return frame_rgb

    @staticmethod
    def area_of_interest(frame_rgb, cut_l, cut_r, cut_t, cut_b):
        if cut_l > 0 or cut_r > 0 or cut_t > 0 or cut_b > 0:
            frame_black = np.zeros_like(frame_rgb)
            s = frame_black.shape

            y_t = cut_t
            y_b = s[0] - cut_b
            x_l = cut_l
            x_r = s[1] - cut_r

            frame_black[y_t:y_b, x_l:x_r] = frame_rgb[y_t:y_b, x_l:x_r]
            return frame_black
        return frame_rgb
