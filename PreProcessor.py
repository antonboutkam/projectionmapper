import cv2
import numpy as np
from Manipulation import Manipulation


class PreProcessor:
    def process(self, frame, gui, monitor):
        output = frame.copy()
        output = Manipulation.area_of_interest(output, gui.ai_left, gui.ai_right, gui.ai_top, gui.ai_bottom)
        output = Manipulation.color_reduction(output, gui.remove_red, gui.remove_green, gui.remove_blue)

        gpu_output = cv2.cuda_GpuMat()
        gpu_output.upload(output)

        gpu_output = cv2.cuda.cvtColor(gpu_output, cv2.COLOR_BGR2GRAY)
        monitor.add_gpu("GRAY", gpu_output)
        cpu_output = gpu_output.download()
        cpu_output_changed = False
        if gui.enable_dilate:
            cpu_output_changed = True
            print("Dilate: ", (gui.dilate_kernel_y, gui.dilate_kernel_x))
            kernel_values = (gui.dilate_kernel_y, gui.dilate_kernel_x)
            dilate_kernel = np.ones(kernel_values, np.uint8)
            cpu_output = cv2.dilate(cpu_output, dilate_kernel)
            monitor.add("Eroded", cpu_output)

        if gui.enable_erode:
            cpu_output_changed = True
            print("Erode: ", (gui.erode_kernel_y, gui.erode_kernel_x))
            kernel_values = (gui.erode_kernel_y, gui.erode_kernel_x)
            erode_kernel = np.ones(kernel_values, np.uint8)
            cpu_output = cv2.erode(cpu_output, erode_kernel)
            monitor.add("Dilated", cpu_output)

        if gui.blur_enable > 0:
            cpu_output_changed = True
            if gui.blur_enable == 1:
                cpu_output = cv2.blur(cpu_output, (gui.blur1, gui.blur2))
            elif gui.blur_enable == 2:
                cpu_output = cv2.GaussianBlur(cpu_output, (gui.blur1, gui.blur2))
            monitor.add("Blurred", cpu_output)

        if cpu_output_changed:
            gpu_output.upload(cpu_output)

        if gui.canny_enable:
            detector = cv2.cuda.createCannyEdgeDetector(gui.canny1, gui.canny2)
            gpu_output = detector.detect(gpu_output)
            monitor.add_gpu("Canny", gpu_output)

        if gui.threshold_enable:
            if gui.threshold_mode == 0:
                ret, gpu_output = cv2.cuda.threshold(gpu_output, gui.threshold, 255, cv2.THRESH_BINARY)
                monitor.add_gpu("Threshold", gpu_output)
            elif gui.threshold_mode == 1:
                cpu_output = gpu_output.download()
                ret, cpu_output = cv2.threshold(cpu_output, gui.threshold, 255,
                                                     cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                monitor.add("Threshold", cpu_output)
                gpu_output.upload(cpu_output)
            elif gui.threshold_mode == 2:
                cpu_output = gpu_output.download()
                ret, cpu_output = cv2.threshold(cpu_output, gui.threshold, 255, cv2.THRESH_TOZERO)
                gpu_output.upload(cpu_output)
                monitor.add("Threshold", cpu_output)

        monitor.add_gpu("PreProc Result", gpu_output)
        return gpu_output
