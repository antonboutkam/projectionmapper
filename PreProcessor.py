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
        # OR
        output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        monitor.add("PreProc GRAY", output)
        # OR

        if gui.canny_enable:
            output = cv2.Canny(output, gui.canny1, gui.canny2)
            monitor.add("PreProc Canny", output)
        #
        # input_preprocessed = cv2.dilate(input_preprocessed, None)
        output = cv2.erode(output, None)
        kernel = np.ones((9, 9), np.uint8)

        if gui.enable_dilate:
            output = cv2.erode(output, kernel, iterations=2)
            monitor.add("PreProc Erode", output)

        if gui.enable_erode:
            output = cv2.dilate(output, kernel, iterations=2)
            monitor.add("PreProc Dilate", output)

        if gui.blur_enable:
            output = cv2.blur(output, (gui.blur1, gui.blur2))
            monitor.add("PreProc Blur", output)

        if gui.threshold_enable:
            # ret, output = cv2.threshold(output, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            ret, output = cv2.threshold(output, gui.threshold, 255, cv2.THRESH_BINARY)
            monitor.add("PreProc Threshold", output)
            #
            # monitor.add("Threshold", output)

        monitor.add("PreProc Result", output)

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
                output_underlay[resize_offset_y:resize_offset_y + new_height, resize_offset_x:resize_offset_x  + new_width] = output_resized
            output = output_underlay
            monitor.add("PreProc Resized", output)

        # Correct offset
        # M = np.float32([
        #     [1, 0, math.ceil(gui.max_offset_x/2) - gui.offset_x],
        #     [0, 1, math.ceil(gui.max_offset_y/2) - gui.offset_y]
        # ])
        # output = cv2.warpAffine(output, M, (output.shape[1], output.shape[0]))
        # monitor.add("PreProc Resized", output)

        return output