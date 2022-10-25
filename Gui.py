import cv2
import numpy as np


class Gui:
    window_name = 'GUI'
    threshold_enable = 1
    threshold = 127
    threshold_mode = 0
    calibration_threshold = 23
    contour_thickness = 1

    draw_contour_min = 1
    draw_contour_max = 20

    contour_r = 255
    contour_g = 0
    contour_b = 0

    blur_enable = 1
    blur1 = 5
    blur2 = 5

    enable_dilate = 0
    enable_erode = 0

    enable_remove_color = 0
    color_to_remove = 0

    canny_enable = 1
    canny1 = 50
    canny2 = 150

    input_source = 0

    def show(self):
        # create a black image

        img = np.zeros([200, 350, 3], np.uint8)

        # define a null callback function for Trackbar
        def button_click(x, y):
            print("button click", x, y)

        def trackbar_change(x):
            pass

        cv2.namedWindow(self.window_name)
        # cv2.createButton("Init", button_click, "sleep", cv2.QT_PUSH_BUTTON, 1)
        # cv2.createButton("Wake", button_click, "wake", cv2.QT_PUSH_BUTTON, 2)
        # cv2.createButton("Tree", button_click, "tree", cv2.QT_PUSH_BUTTON, 3)

        # Create trackbars
        # arguments: trackbar_name, window_name, default_value, max_value, callback_fn
        cv2.createTrackbar("Calibration threshold", self.window_name, self.calibration_threshold, 255, trackbar_change)

        cv2.createTrackbar("Input source", self.window_name, self.input_source, 2, trackbar_change)
        cv2.createTrackbar("Contour thickness", self.window_name, self.contour_thickness, 6, trackbar_change)

        cv2.createTrackbar("Threshold enable", self.window_name, self.threshold_enable, 1, trackbar_change)
        cv2.createTrackbar("Threshold", self.window_name, self.threshold, 255, trackbar_change)
        cv2.createTrackbar("Threshold mode", self.window_name, self.threshold_mode, 1, trackbar_change)

        cv2.createTrackbar("Contour Red", self.window_name, self.contour_r, 255, trackbar_change)
        cv2.createTrackbar("Contour Green", self.window_name, self.contour_g, 255, trackbar_change)
        cv2.createTrackbar("Contour Blue", self.window_name, self.contour_b, 255, trackbar_change)
        cv2.createTrackbar("Draw contour min", self.window_name, self.draw_contour_min, 40, trackbar_change)
        cv2.createTrackbar("Draw contour max", self.window_name, self.draw_contour_max, 40, trackbar_change)

        cv2.createTrackbar("Enable dilate", self.window_name, self.enable_dilate, 1, trackbar_change)
        cv2.createTrackbar("Enable erode", self.window_name, self.enable_erode, 1, trackbar_change)



        cv2.createTrackbar("Blur enable", self.window_name, self.blur_enable, 10, trackbar_change)
        cv2.createTrackbar("Blur 1", self.window_name, self.blur1, 10, trackbar_change)
        cv2.createTrackbar("Blur 2", self.window_name, self.blur2, 10, trackbar_change)

        cv2.createTrackbar("Color remove enable", self.window_name, self.enable_remove_color, 1, trackbar_change)
        cv2.createTrackbar("RGB (0,1,2) to remove", self.window_name, self.color_to_remove, 2, trackbar_change)


        cv2.createTrackbar("Canny enable", self.window_name, self.canny_enable, 1, trackbar_change)
        cv2.createTrackbar("Canny 1", self.window_name, self.canny1, 255, trackbar_change)
        cv2.createTrackbar("Canny 2", self.window_name, self.canny2, 255, trackbar_change)

    def update(self):
        self.calibration_threshold = cv2.getTrackbarPos("Calibration threshold", self.window_name)
        self.input_source = cv2.getTrackbarPos("Input source", self.window_name)
        self.contour_thickness = cv2.getTrackbarPos("Contour thickness", self.window_name)

        self.threshold_enable = cv2.getTrackbarPos("Threshold enable", self.window_name)
        self.threshold = cv2.getTrackbarPos("Threshold", self.window_name)
        self.threshold_mode = cv2.getTrackbarPos("Threshold mode", self.window_name)

        self.contour_r = cv2.getTrackbarPos("Contour Red", self.window_name)
        self.contour_g = cv2.getTrackbarPos("Contour Green", self.window_name)
        self.contour_b = cv2.getTrackbarPos("Contour Blue", self.window_name)

        self.draw_contour_min = cv2.getTrackbarPos("Draw contour min", self.window_name)
        self.draw_contour_max = cv2.getTrackbarPos("Draw contour max", self.window_name)

        self.blur_enable = cv2.getTrackbarPos("Blur enable", self.window_name)
        self.blur1 = cv2.getTrackbarPos("Blur 1", self.window_name) + 1
        self.blur2 = cv2.getTrackbarPos("Blur 2", self.window_name) + 1

        self.enable_dilate = cv2.getTrackbarPos("Enable dilate", self.window_name)
        self.enable_erode = cv2.getTrackbarPos("Enable erode", self.window_name)

        self.enable_remove_color = cv2.getTrackbarPos("Color remove enable", self.window_name)
        self.color_to_remove = cv2.getTrackbarPos("RGB (0,1,2) to remove", self.window_name)

        self.canny_enable = cv2.getTrackbarPos("Canny enable", self.window_name)
        self.canny1 = cv2.getTrackbarPos("Canny 1", self.window_name)
        self.canny2 = cv2.getTrackbarPos("Canny 2", self.window_name)
