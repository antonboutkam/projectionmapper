import math

import cv2
import numpy as np
import random as rng


class PreProcessor:
    def process(self, frame, gui, monitor):
        output = frame.copy()

        if gui.enable_remove_color:
            # Completely remove {color_to_remove} from the source image
            output[..., [gui.color_to_remove]] = 0
            monitor.add("Color removed", output)

        gpu_output = cv2.cuda_GpuMat()
        gpu_output.upload(output)

        gpu_output = cv2.cuda.cvtColor(gpu_output, cv2.COLOR_BGR2GRAY)
        monitor.add_gpu("GRAY", gpu_output)

        if gui.enable_dilate:
#            print("kernel x,y:", gui.dilate_kernel_y, ", ", gui.dilate_kernel_x)
            dilate_kernel = np.ones((gui.dilate_kernel_y, gui.dilate_kernel_x), np.uint8)
            dilated = cv2.dilate(gpu_output.download(), dilate_kernel, iterations=2)
            gpu_output.upload(dilated)
            monitor.add("Eroded", dilated)

        if gui.enable_erode:
            erode_kernel = np.ones((gui.erode_kernel_y, gui.erode_kernel_x), np.uint8)
            eroded = cv2.erode(gpu_output.download(), erode_kernel, iterations=2)
            gpu_output.upload(eroded)
            monitor.add("Dilatet", eroded)

        if gui.blur_enable:
            blurred = cv2.blur(gpu_output.download(), (gui.blur1, gui.blur2))
            gpu_output.upload(blurred)
            monitor.add("Blurred", blurred)

        if gui.canny_enable:
            detector = cv2.cuda.createCannyEdgeDetector(gui.canny1, gui.canny2)
            gpu_output = detector.detect(gpu_output)
            monitor.add_gpu("Canny", gpu_output)

        if gui.threshold_enable:
            # ret, output = cv2.threshold(output, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            ret, gpu_output = cv2.cuda.threshold(gpu_output, gui.threshold, 255, cv2.THRESH_BINARY)
            monitor.add_gpu("Threshold", gpu_output)

        monitor.add_gpu("PreProc Result", gpu_output)
        return gpu_output
