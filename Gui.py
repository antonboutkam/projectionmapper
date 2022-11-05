import cv2
import numpy as np


class Gui:
    window_main = 'Main config'
    window_calibration = 'Calibration config'
    window_preprocessing = 'Preprocessing config'
    window_output = 'Output config'
    window_object_tracing = 'Object tracing config'

    main_show_calibration = 1
    main_show_preprocessing = 1
    main_show_monitor = 1
    main_show_output_config = 1

    threshold_enable = 1
    threshold = 193
    threshold_mode = 0

    calibration_manual_min_x = 0
    calibration_manual_max_x = 100
    calibration_manual_min_y = 0
    calibration_manual_max_y = 100

    calibration_recalibrate = False
    calibration_threshold = 90
    calibration_manual_mode = 0
    calibration_luminosity = 127
    calibration_show_project_cutout = 1
    calibration_show_threshold = 0
    calibration_show_input_source = 1
    calibration_show_found_contours = 1
    calibration_convex_hull = 0
    contour_thickness = 1

    offset_x = 400
    offset_y = 400

    replace_black = 0

    max_offset_x = 800
    max_offset_y = 800
    find_contour_enable = 0
    draw_contour_min = 0
    draw_contour_max = 6

    contour_r = 255
    contour_g = 0
    contour_b = 0


    blur_enable = 0
    blur1 = 5
    blur2 = 5

    enable_dilate = 0
    dilate_kernel_x = 5
    dilate_kernel_y = 5

    enable_erode = 1
    erode_kernel_x = 5
    erode_kernel_y = 5

    enable_remove_color = 0
    color_to_remove = 0
    mask_scale = 90
    canny_enable = 0

    canny1 = 50
    canny2 = 150

    input_source = 0
    video_size_mode = 0
    video_source = 0
    video_source_brightness = 127

    def init(self, cam):
        self.calibration_manual_max_x = cam.width
        self.calibration_manual_max_y = cam.height

    def main_config(self):
        cv2.namedWindow(self.window_main)
        cv2.createTrackbar("Show calibration", self.window_main, self.main_show_calibration, 1, self.trackbar_change)
        cv2.createTrackbar("Show preprocessing", self.window_main, self.main_show_preprocessing, 1, self.trackbar_change)
        cv2.createTrackbar("Show monitor", self.window_main, self.main_show_monitor, 1, self.trackbar_change)
        cv2.createTrackbar("Show output config", self.window_main, self.main_show_output_config, 1, self.trackbar_change)

    def calibration_config(self):
        if self.main_show_calibration:
            cv2.namedWindow(self.window_calibration)
            cv2.createTrackbar("Calibration threshold", self.window_calibration, self.calibration_threshold, 255, self.trackbar_change)
            cv2.createTrackbar("Calibration luminosity", self.window_calibration, self.calibration_luminosity, 255, self.trackbar_change)
            cv2.createTrackbar("Calibration manual mode", self.window_calibration, self.calibration_manual_mode, 1,self.trackbar_change)
            cv2.createTrackbar("Calibration convex hull", self.window_calibration, self.calibration_convex_hull, 1, self.trackbar_change)

            cv2.createTrackbar("Cam cut min X", self.window_calibration, self.calibration_manual_min_x, 1, self.trackbar_change)
            cv2.createTrackbar("Cam cut max X", self.window_calibration, self.calibration_manual_max_x, 1, self.trackbar_change)
            cv2.createTrackbar("Cam cut min Y", self.window_calibration, self.calibration_manual_min_y, 1, self.trackbar_change)
            cv2.createTrackbar("Cam cut max Y", self.window_calibration, self.calibration_manual_max_y, 1, self.trackbar_change)

            cv2.createTrackbar("Input source", self.window_calibration, self.input_source, 2, self.trackbar_change)

            cv2.createTrackbar("Show cutout", self.window_calibration, self.calibration_show_project_cutout, 1, self.trackbar_change)
            cv2.createTrackbar("Show threshold", self.window_calibration, self.calibration_show_threshold, 1, self.trackbar_change)

            cv2.createTrackbar("Show input source", self.window_calibration, self.calibration_show_input_source, 1, self.trackbar_change)

            cv2.createTrackbar("Show found contours", self.window_calibration, self.calibration_show_found_contours, 1,self.trackbar_change)
            cv2.createTrackbar("Preview contour thickness", self.window_calibration, self.contour_thickness, 6, self.trackbar_change)
        else:
            cv2.destroyWindow(self.window_calibration)

    def output_config(self):
        if self.main_show_output_config:
            cv2.namedWindow(self.window_output)
            cv2.createTrackbar("Video source", self.window_output, self.video_source, 1, self.trackbar_change)
            cv2.createTrackbar("Video size mode", self.window_output, self.video_size_mode, 1, self.trackbar_change)
            cv2.createTrackbar("Video brightness", self.window_output, self.video_source_brightness, 255, self.trackbar_change)
            cv2.createTrackbar("Offset X", self.window_output, self.offset_x, self.max_offset_x, self.trackbar_change)
            cv2.createTrackbar("Offset Y", self.window_output, self.offset_y, self.max_offset_y, self.trackbar_change)
            cv2.createTrackbar("Replace black", self.window_output, self.replace_black, 255,self.trackbar_change)
            cv2.createTrackbar("Mask scale", self.window_output, self.mask_scale, 100, self.trackbar_change)
        else:
            cv2.destroyWindow(self.window_output)

    def object_tracing_config(self):
        cv2.namedWindow(self.window_object_tracing)
        cv2.createTrackbar("Threshold enable", self.window_object_tracing, self.threshold_enable, 1,self.trackbar_change)
        cv2.createTrackbar("Threshold", self.window_object_tracing, self.threshold, 255, self.trackbar_change)
        cv2.createTrackbar("Threshold mode", self.window_object_tracing, self.threshold_mode, 1, self.trackbar_change)
        cv2.createTrackbar("Canny enable", self.window_object_tracing, self.canny_enable, 1, self.trackbar_change)
        cv2.createTrackbar("Canny 1", self.window_object_tracing, self.canny1, 255, self.trackbar_change)
        cv2.createTrackbar("Canny 2", self.window_object_tracing, self.canny2, 255, self.trackbar_change)

        cv2.createTrackbar("Contour enable", self.window_object_tracing, self.find_contour_enable, 1, self.trackbar_change)
        cv2.createTrackbar("Draw contour min", self.window_object_tracing, self.draw_contour_min, 40,self.trackbar_change)
        cv2.createTrackbar("Draw contour max", self.window_object_tracing, self.draw_contour_max, 40,self.trackbar_change)

    def preprocessing_config(self):
        if self.main_show_preprocessing:
            cv2.namedWindow(self.window_preprocessing)
            cv2.createTrackbar("Enable dilate", self.window_preprocessing, self.enable_dilate, 1, self.trackbar_change)
            cv2.createTrackbar("Dilate kernel x", self.window_preprocessing, self.dilate_kernel_x, 15, self.trackbar_change)
            cv2.createTrackbar("Dilate kernel y", self.window_preprocessing, self.dilate_kernel_y, 15, self.trackbar_change)
            cv2.createTrackbar("Enable erode", self.window_preprocessing, self.enable_erode, 1, self.trackbar_change)
            cv2.createTrackbar("Erode kernel x", self.window_preprocessing, self.erode_kernel_x, 15, self.trackbar_change)
            cv2.createTrackbar("Erode kernel y", self.window_preprocessing, self.erode_kernel_y, 15, self.trackbar_change)
            cv2.createTrackbar("Blur enable", self.window_preprocessing, self.blur_enable, 1, self.trackbar_change)
            cv2.createTrackbar("Blur 1", self.window_preprocessing, self.blur1, 10, self.trackbar_change)
            cv2.createTrackbar("Blur 2", self.window_preprocessing, self.blur2, 10, self.trackbar_change)
            cv2.createTrackbar("Color remove enable", self.window_preprocessing, self.enable_remove_color, 1, self.trackbar_change)
            cv2.createTrackbar("RGB (0,1,2) to remove", self.window_preprocessing, self.color_to_remove, 2, self.trackbar_change)
        else:
            cv2.destroyWindow(self.window_preprocessing)

    def trackbar_change(self, x):
        pass

    def show(self):
        # create a black image
        img = np.zeros([200, 350, 3], np.uint8)

        self.main_config()
        self.calibration_config()
        self.preprocessing_config()
        self.output_config()
        self.object_tracing_config()

    def update(self):

        if cv2.getWindowProperty(self.window_main, cv2.WND_PROP_VISIBLE):
            self.main_show_calibration = cv2.getTrackbarPos("Show calibration", self.window_main)
            self.main_show_preprocessing = cv2.getTrackbarPos("Show preprocessing", self.window_main)
            self.main_show_monitor = cv2.getTrackbarPos("Show monitor", self.window_main)
            self.main_show_output_config = cv2.getTrackbarPos("Show output config", self.window_main)

        if cv2.getWindowProperty(self.window_calibration, cv2.WND_PROP_VISIBLE):
            tmp = cv2.getTrackbarPos("Calibration threshold", self.window_calibration)
            if tmp != self.calibration_threshold:
                self.calibration_recalibrate = True
            self.calibration_threshold = tmp

            tmp = cv2.getTrackbarPos("Calibration luminosity", self.window_calibration)
            if tmp != self.calibration_luminosity:
                self.calibration_recalibrate = True
            self.calibration_luminosity = tmp

            tmp = cv2.getTrackbarPos("Calibration manual mode", self.window_calibration)
            if tmp != self.calibration_manual_mode:
                self.calibration_recalibrate = True
            self.calibration_manual_mode = tmp

            tmp = cv2.getTrackbarPos("Cam cut min X", self.window_calibration)
            if tmp != self.calibration_manual_min_x:
                self.calibration_recalibrate = True
            self.calibration_manual_min_x = tmp

            tmp = cv2.getTrackbarPos("Cam cut max X", self.window_calibration)
            if tmp != self.calibration_manual_max_x:
                self.calibration_recalibrate = True
            self.calibration_manual_max_x = tmp

            tmp = cv2.getTrackbarPos("Cam cut min Y", self.window_calibration)
            if tmp != self.calibration_manual_min_y:
                self.calibration_recalibrate = True
            self.calibration_manual_min_y = tmp

            tmp = cv2.getTrackbarPos("Cam cut max Y", self.window_calibration)
            if tmp != self.calibration_manual_max_y:
                self.calibration_recalibrate = True
            self.calibration_manual_max_y = tmp

            tmp = cv2.getTrackbarPos("Calibration convex hull", self.window_calibration)
            if tmp != self.calibration_convex_hull:
                self.calibration_recalibrate = True
            self.calibration_convex_hull = tmp

            tmp = cv2.getTrackbarPos("Input source", self.window_calibration)
            if tmp != self.input_source:
                self.calibration_recalibrate = True
            self.input_source = tmp

            tmp = cv2.getTrackbarPos("Show input source", self.window_calibration)
            if tmp != self.calibration_show_input_source:
                self.calibration_recalibrate = True
            self.calibration_show_input_source = tmp

            tmp = cv2.getTrackbarPos("Show cutout", self.window_calibration)
            if tmp != self.calibration_show_project_cutout:
                self.calibration_recalibrate = True
            self.calibration_show_project_cutout = tmp

            tmp = cv2.getTrackbarPos("Show threshold", self.window_calibration)
            if tmp != self.calibration_show_threshold:
                self.calibration_recalibrate = True
            self.calibration_show_threshold = tmp

            tmp = cv2.getTrackbarPos("Show found contours", self.window_calibration)
            if tmp != self.calibration_show_found_contours:
                self.calibration_recalibrate = True
            self.calibration_show_found_contours = tmp

            tmp = cv2.getTrackbarPos("Preview contour thickness", self.window_calibration)
            if tmp != self.contour_thickness:
                self.calibration_recalibrate = True
            self.contour_thickness = tmp

        if cv2.getWindowProperty(self.window_object_tracing, cv2.WND_PROP_VISIBLE):
            self.threshold_enable = cv2.getTrackbarPos("Threshold enable", self.window_object_tracing)
            self.threshold = cv2.getTrackbarPos("Threshold", self.window_object_tracing)
            self.threshold_mode = cv2.getTrackbarPos("Threshold mode", self.window_object_tracing)
            self.find_contour_enable = cv2.getTrackbarPos("Contour enable", self.window_object_tracing)
            self.draw_contour_min = cv2.getTrackbarPos("Draw contour min", self.window_object_tracing)
            self.draw_contour_max = cv2.getTrackbarPos("Draw contour max", self.window_object_tracing)
            self.canny_enable = cv2.getTrackbarPos("Canny enable", self.window_object_tracing)
            self.canny1 = cv2.getTrackbarPos("Canny 1", self.window_object_tracing)
            self.canny2 = cv2.getTrackbarPos("Canny 2", self.window_object_tracing)

        if cv2.getWindowProperty(self.window_preprocessing, cv2.WND_PROP_VISIBLE):
            if self.blur_enable:
                self.blur1 = cv2.getTrackbarPos("Blur 1", self.window_preprocessing) + 1
                self.blur2 = cv2.getTrackbarPos("Blur 2", self.window_preprocessing) + 1
            self.blur_enable = cv2.getTrackbarPos("Blur enable", self.window_preprocessing)

            if self.enable_dilate:
                self.dilate_kernel_x = cv2.getTrackbarPos("Dilate kernel x", self.window_preprocessing)
                self.dilate_kernel_y = cv2.getTrackbarPos("Dilate kernel y", self.window_preprocessing)
            self.enable_dilate = cv2.getTrackbarPos("Enable dilate", self.window_preprocessing)

            if self.enable_erode:
                self.erode_kernel_x = cv2.getTrackbarPos("Erode kernel x", self.window_preprocessing)
                self.erode_kernel_y = cv2.getTrackbarPos("Erode kernel y", self.window_preprocessing)
            self.enable_erode = cv2.getTrackbarPos("Enable erode", self.window_preprocessing)

            if self.enable_remove_color:
                self.color_to_remove = cv2.getTrackbarPos("RGB (0,1,2) to remove", self.window_preprocessing)
            self.enable_remove_color = cv2.getTrackbarPos("Color remove enable", self.window_preprocessing)

        if cv2.getWindowProperty(self.window_output, cv2.WND_PROP_VISIBLE):
            self.video_source = cv2.getTrackbarPos("Video source", self.window_output)
            self.video_source_brightness = cv2.getTrackbarPos("Video brightness", self.window_output)
            self.video_size_mode = cv2.getTrackbarPos("Video size mode", self.window_output)
            self.mask_scale = cv2.getTrackbarPos("Mask scale", self.window_output)

            tmp =  cv2.getTrackbarPos("Offset X", self.window_output)
            if self.offset_x != tmp:
                self.offset_x = tmp
                print('Offset X', tmp)
            self.offset_x = cv2.getTrackbarPos("Offset X", self.window_output)
            self.offset_y = cv2.getTrackbarPos("Offset Y", self.window_output)
            self.replace_black = cv2.getTrackbarPos("Replace black", self.window_output)