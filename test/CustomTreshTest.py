class CustomTreshTest :
    def fake_code(self):
        cv2.imwrite("qqqqqqqq.jpg", white_fullcolor)
        cv2.imshow("White full color", white_fullcolor)
        white_fullcolor_hsv = cv2.cvtColor(white_fullcolor, cv2.COLOR_BGR2HSV)
        cv2.imwrite('picture.jpg', white_fullcolor_hsv)
        print("Center pixel: ", white_fullcolor_hsv)
        (w, h) = white_fullcolor_hsv.shape[:2]
        center_x = math.ceil(w / 2)
        center_y = math.ceil(h / 2)
        (center_h, center_s, center_v) = white_fullcolor_hsv[center_y, center_x]
        print("Center h,s,v: (", center_h, ",", center_s, ",", center_v, ")")
        (left_top_h, left_top_s, left_top_v) = white_fullcolor_hsv[5, 5]
        print("Left top h,s,v: (", left_top_h, ",", left_top_s, ",", left_top_v, ")")
        (right_bottom_h, right_bottom_s, right_bottom_v) = white_fullcolor_hsv[w - 5, h - 5]
        print("Right bottom h,s,v: (", right_bottom_h, ",", right_bottom_s, ",", right_bottom_v, ")")

        avg_outer_h = math.ceil((left_top_h + right_bottom_h) / 2)

        h_min = center_h - 2
        print("hmin", h_min)
        min = (h_min, 0, 0)
        print(min)
        _, custom_thresh = cv2.inRange(white_fullcolor_hsv, min, (127, 255, 255))
        cv2.imshow("Custom tresh", custom_thresh)

        # blue_dist = center_h - avg_outer_blue
        # green_dist = center_s - avg_outer_green
        # middle_blue_dist = math.ceil(blue_dist / 2)
        # middle_green_dist = math.ceil(gree_dist / 2)
        # min_blue = center_h - middle_blue_dist
        # min_green = center_s - middle_green_dist
        # lower_gb = np.array ([min_blue, min_green, 200], dtype="uint8")
        # upper_gb = np.array([0, 0, 255], dtype="uint8")

        #
        cv2.imwrite("rrr.jpg", white_fullcolor)
        # white_fullcolor = cv2.resize(white_fullcolor, (640, 360))

        cv2.imshow("White BGR", white_bgr)
        # white_bgr = self._white_frame

        # kernel = np.ones((5, 5), np.uint8)
        # white_bgr = cv2.dilate(white_bgr, kernel)
        # thresh = cv2.erode(thresh, None)
        # white_bgr = cv2.GaussianBlur(white_bgr, (7, 7), 0)





    def kep_2:
        contour_info = list()
        detected_contours, hierarchy = cv2.findContours(input_preprocessed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE,
                                                        offset=(self.gui.offset_x, self.gui.offset_y))
        self.monitor.add
        contour_count = len(detected_contours)
        preview = current_frame

        height, width = input_preprocessed.shape[:2]
        mask = np.zeros((height, width), np.uint8)

        if contour_count > 0:
            # print("Contour count ", contour_count)
            # cv2.resize(mask, (width, height))
            for ci in detected_contours[self.gui.draw_contour_min:self.gui.draw_contour_max]:
                # print("area ", cv2.contourArea(ci))
                hull = cv2.convexHull(ci)
                cv2.fillConvexPoly(mask, hull, 255)
            # mask = cv2.dilate(mask, None, iterations=10)
            # mask = cv2.erode(mask, None, iterations=10)
            # mask = cv2.GaussianBlur(mask, (5, 5), 0)
            # mask_stack = np.dstack([mask] * 3)
            # mask_stack = mask_stack.astype('float32') / 255.0

            #  self.monitor.add("Mask", output)

            # detected_contours = sorted(detected_contours, key=cv2.contourArea, reverse=True)

            # print(detected_contours)
            cv2.drawContours(preview, detected_contours[self.gui.draw_contour_min:self.gui.draw_contour_max], -1,
                             (self.gui.contour_b, self.gui.contour_g, self.gui.contour_r),
                             self.gui.contour_thickness)
            self.monitor.add("Preview", preview)

            cv2.drawContours(mask, detected_contours[self.gui.draw_contour_min:self.gui.draw_contour_max], -1,
                             (self.gui.contour_b, self.gui.contour_g, self.gui.contour_r),
                             self.gui.contour_thickness)

            self.monitor.add("Mask", mask)
            # print("Current frame COLOR 0", current_frame[0])
            # print("Current frame BGR 0", input_source[0])

            # self.self.monitor.add("Original", current_frame)
            # self.self.monitor.add("Input BGR", input_source)

            # self.show_large("Input GRAY", input_preprocessed)
            # self.show_large("Original + contours", preview)
            # self.self.monitor.add("Output", output)
