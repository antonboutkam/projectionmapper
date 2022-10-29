import cv2
import numpy as np


class Gui:
    window_runtime = 'Runtime config'
    window_etc = 'Etc config'
    
    threshold_enable = 1
    threshold = 193
    threshold_mode = 0
    calibration_threshold = 90
    calibration_luminosity = 127
    contour_thickness = 1

    offset_x = 400
    offset_y = 400
    max_offset_x = 800
    max_offset_y = 800
    draw_contour_min = 1
    draw_contour_max = 20

    contour_r = 255
    contour_g = 0
    contour_b = 0

    blur_enable = 0
    blur1 = 5
    blur2 = 5

    enable_dilate = 0
    enable_erode = 1

    enable_remove_color = 0
    color_to_remove = 0
    mask_scale = 90
    canny_enable = 0

    canny1 = 50
    canny2 = 150

    input_source = 0
    video_source = 0
    video_source_brightness = 127

    def show(self):
        # create a black image

        img = np.zeros([200, 350, 3], np.uint8)

        # define a null callback function for Trackbar
        def button_click(x, y):
            print("button click", x, y)

        def trackbar_change(x):
            pass

        cv2.namedWindow(self.window_runtime)
        cv2.namedWindow(self.window_etc)
        # cv2.createButton("Init", button_click, "sleep", cv2.QT_PUSH_BUTTON, 1)
        # cv2.createButton("Wake", button_click, "wake", cv2.QT_PUSH_BUTTON, 2)
        # cv2.createButton("Tree", button_click, "tree", cv2.QT_PUSH_BUTTON, 3)

        # Create trackbars
        # arguments: trackbar_name, window_runtime, default_value, max_value, callback_fn
        cv2.createTrackbar("Calibration threshold", self.window_etc, self.calibration_threshold, 255, trackbar_change)
        cv2.createTrackbar("Calibration luminosity", self.window_etc, self.calibration_luminosity, 255, trackbar_change)

        cv2.createTrackbar("Input source", self.window_etc, self.input_source, 2, trackbar_change)
        cv2.createTrackbar("Contour thickness", self.window_etc, self.contour_thickness, 6, trackbar_change)

        cv2.createTrackbar("Video source", self.window_etc, self.video_source, 1, trackbar_change)
        cv2.createTrackbar("Video brightness", self.window_etc, self.video_source_brightness, 255, trackbar_change)

        cv2.createTrackbar("Threshold enable", self.window_etc, self.threshold_enable, 1, trackbar_change)
        cv2.createTrackbar("Threshold", self.window_etc, self.threshold, 255, trackbar_change)
        cv2.createTrackbar("Threshold mode", self.window_etc, self.threshold_mode, 1, trackbar_change)

        cv2.createTrackbar("Mask scale", self.window_runtime, self.mask_scale, 100, trackbar_change)
        cv2.createTrackbar("Contour Red", self.window_runtime, self.contour_r, 255, trackbar_change)
        cv2.createTrackbar("Contour Green", self.window_runtime, self.contour_g, 255, trackbar_change)
        cv2.createTrackbar("Contour Blue", self.window_runtime, self.contour_b, 255, trackbar_change)

        cv2.createTrackbar("Offset X", self.window_runtime, self.offset_x, self.max_offset_x, trackbar_change)
        cv2.createTrackbar("Offset Y", self.window_runtime, self.offset_y, self.max_offset_y    , trackbar_change)

        cv2.createTrackbar("Draw contour min", self.window_runtime, self.draw_contour_min, 40, trackbar_change)
        cv2.createTrackbar("Draw contour max", self.window_runtime, self.draw_contour_max, 40, trackbar_change)

        cv2.createTrackbar("Enable dilate", self.window_runtime, self.enable_dilate, 1, trackbar_change)
        cv2.createTrackbar("Enable erode", self.window_runtime, self.enable_erode, 1, trackbar_change)

        cv2.createTrackbar("Blur enable", self.window_runtime, self.blur_enable, 10, trackbar_change)
        cv2.createTrackbar("Blur 1", self.window_runtime, self.blur1, 10, trackbar_change)
        cv2.createTrackbar("Blur 2", self.window_runtime, self.blur2, 10, trackbar_change)

        cv2.createTrackbar("Color remove enable", self.window_runtime, self.enable_remove_color, 1, trackbar_change)
        cv2.createTrackbar("RGB (0,1,2) to remove", self.window_runtime, self.color_to_remove, 2, trackbar_change)

        cv2.createTrackbar("Canny enable", self.window_runtime, self.canny_enable, 1, trackbar_change)
        cv2.createTrackbar("Canny 1", self.window_runtime, self.canny1, 255, trackbar_change)
        cv2.createTrackbar("Canny 2", self.window_runtime, self.canny2, 255, trackbar_change)

    def update(self):
        self.calibration_threshold = cv2.getTrackbarPos("Calibration threshold", self.window_etc)
        self.calibration_luminosity = cv2.getTrackbarPos("Calibration luminosity", self.window_etc)

        self.input_source = cv2.getTrackbarPos("Input source", self.window_etc)
        self.contour_thickness = cv2.getTrackbarPos("Contour thickness", self.window_etc)

        self.video_source = cv2.getTrackbarPos("Video source", self.window_etc)
        self.video_source_brightness = cv2.getTrackbarPos("Video brightness", self.window_etc)

        self.threshold_enable = cv2.getTrackbarPos("Threshold enable", self.window_etc)
        self.threshold = cv2.getTrackbarPos("Threshold", self.window_etc)
        self.threshold_mode = cv2.getTrackbarPos("Threshold mode", self.window_etc)

        self.contour_r = cv2.getTrackbarPos("Contour Red", self.window_runtime)
        self.contour_g = cv2.getTrackbarPos("Contour Green", self.window_runtime)
        self.contour_b = cv2.getTrackbarPos("Contour Blue", self.window_runtime)

        self.mask_scale = cv2.getTrackbarPos("Mask scale", self.window_runtime)
        self.offset_x = cv2.getTrackbarPos("Offset X", self.window_runtime)
        self.offset_y = cv2.getTrackbarPos("Offset Y", self.window_runtime)

        self.draw_contour_min = cv2.getTrackbarPos("Draw contour min", self.window_runtime)
        self.draw_contour_max = cv2.getTrackbarPos("Draw contour max", self.window_runtime)

        self.blur_enable = cv2.getTrackbarPos("Blur enable", self.window_runtime)
        self.blur1 = cv2.getTrackbarPos("Blur 1", self.window_runtime) + 1
        self.blur2 = cv2.getTrackbarPos("Blur 2", self.window_runtime) + 1

        self.enable_dilate = cv2.getTrackbarPos("Enable dilate", self.window_runtime)
        self.enable_erode = cv2.getTrackbarPos("Enable erode", self.window_runtime)

        self.enable_remove_color = cv2.getTrackbarPos("Color remove enable", self.window_runtime)
        self.color_to_remove = cv2.getTrackbarPos("RGB (0,1,2) to remove", self.window_runtime)

        self.canny_enable = cv2.getTrackbarPos("Canny enable", self.window_runtime)
        self.canny1 = cv2.getTrackbarPos("Canny 1", self.window_runtime)
        self.canny2 = cv2.getTrackbarPos("Canny 2", self.window_runtime)
