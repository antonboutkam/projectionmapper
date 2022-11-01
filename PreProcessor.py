import math

import cv2
import numpy as np


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
            gpu_output = cv2.cuda.Canny(gpu_output, gui.canny1, gui.canny2)
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
            im, gpu_contours, hierarchy = cv2.cuda.findContours(gpu_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            contour_output = np.zeros_like(output)
            gpu_contour_output = cv2.cuda_GpuMat()
            gpu_contour_output.upload(contour_output)
            for gpu_contour in gpu_contours[gui.draw_contour_min:gui.draw_contour_min]:
                gpu_hull = cv2.cuda.convexHull(gpu_contour)
                cv2.cuda.fillConvexPoly(gpu_contour_output, gpu_hull, 255)
            gpu_output = gpu_contour_output
            monitor.add_gpu("Contours traced", gpu_output)

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
