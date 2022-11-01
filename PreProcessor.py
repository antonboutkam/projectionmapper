import math

import cv2
import numpy as np
import random as rng


class PreProcessor:
    def process(self, frame, gui, monitor):
        output = frame.copy()

        monitor.add("PreProc input", frame)
        if gui.enable_remove_color:
            # Completely remove {color_to_remove} from the source image
            output[..., [gui.color_to_remove]] = 0
            monitor.add("PreProc Color removed", output)

        gpu_output = cv2.cuda_GpuMat()
        gpu_output.upload(output)

        gpu_output = cv2.cuda.cvtColor(gpu_output, cv2.COLOR_BGR2GRAY)
        monitor.add_gpu("PreProc GRAY", gpu_output)

        if gui.canny_enable:
            detector = cv2.cuda.createCannyEdgeDetector(gui.canny1, gui.canny2)
            gpu_output = detector.detect(gpu_output)
            monitor.add_gpu("PreProc Canny", gpu_output)

        if gui.enable_dilate:
            dilate_kernel = np.ones((gui.dilate_kernel_y, gui.dilate_kernel_x), np.uint8)
            dilated = cv2.dilate(gpu_output.download(), dilate_kernel, iterations=2)
            gpu_output.upload(dilated)
            monitor.add("PreProc Erode", dilated)

        if gui.enable_erode:
            erode_kernel = np.ones((gui.erode_kernel_y, gui.erode_kernel_x), np.uint8)
            eroded = cv2.erode(gpu_output.download(), erode_kernel, iterations=2)
            gpu_output.upload(eroded)
            monitor.add("PreProc Dilate", eroded)

        if gui.blur_enable:
            blurred = cv2.cuda.blur(gpu_output.download(), (gui.blur1, gui.blur2))
            gpu_output.upload(blurred)
            monitor.add("PreProc Blur", blurred)

        if gui.threshold_enable:
            # ret, output = cv2.threshold(output, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            ret, gpu_output = cv2.cuda.threshold(gpu_output, gui.threshold, 255, cv2.THRESH_BINARY)
            monitor.add_gpu("PreProc Threshold", gpu_output)


        if gui.find_contour_enable:
            im, contours, hierarchy = cv2.findContours(gpu_output.download(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            hull_list = []
            for contour in contours[gui.draw_contour_min:gui.draw_contour_min]:
                hull = cv2.convexHull(contour)
                hull_list.append(hull)

            drawing = np.zeros((output.shape[0], output.shape[1], 3), dtype=np.uint8)
            for i in range(len(hull_list)):
                color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
                cv2.drawContours(drawing, hull_list[i], i, color)

            monitor.add("Hulls", drawing)
            gpu_output = cv2.cuda_GpuMat()
            gpu_output.upload(drawing)

        monitor.add_gpu("PreProc Result", gpu_output)

        if False:
            # resize and center
            scale_percent = gui.mask_scale  # percent of original size
            if scale_percent < 100:
                new_width = int(output.shape[1] * scale_percent / 100)
                new_height = int(output.shape[0] * scale_percent / 100)
                print(new_height, new_width)
                resize_offset_x = math.ceil((output.shape[1] - new_width) / 2)
                resize_offset_y = math.ceil((output.shape[0] - new_height) / 2)
                new_dim = (new_height, new_width)

                print(new_dim)
                # resize image
                output_resized = cv2.resize(output, new_dim, interpolation=cv2.INTER_AREA)
                print(output_resized.shape)
                # print("Preview container shape ", shape)

                output_underlay = np.zeros_like(output)
                print(output.shape)
                output_underlay[resize_offset_y:resize_offset_y + new_height,
                resize_offset_x:resize_offset_x + new_width] = output_resized
            output = output_underlay
            monitor.add("PreProc Resized", output)

        # Correct offset
        # M = np.float32([
        #     [1, 0, math.ceil(gui.max_offset_x/2) - gui.offset_x],
        #     [0, 1, math.ceil(gui.max_offset_y/2) - gui.offset_y]
        # ])
        # output = cv2.warpAffine(output, M, (output.shape[1], output.shape[0]))
        # monitor.add("PreProc Resized", output)

        return gpu_output
