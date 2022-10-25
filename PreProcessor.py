import cv2

class PreProcessor:
    def process(self, frame, gui, monitor):
        output = frame.copy()

        if gui.enable_remove_color:
            # Completely remove {color_to_remove} from the source image
            output[..., [gui.color_to_remove]] = 0
            monitor.add("Color removed", output)


        # OR
        output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        # monitor.add("GRAY", output)
        # OR

        if gui.canny_enable:
            output = cv2.Canny(output, gui.canny1, gui.canny2)
            monitor.add("Canny", output)
        #
        # input_preprocessed = cv2.dilate(input_preprocessed, None)
        # input_preprocessed = cv2.erode(input_preprocessed, None)

        if gui.blur_enable:
            output = cv2.blur(output, (gui.blur1, gui.blur2))
            monitor.add("Blur", output)

        if gui.threshold_enable:
            ret, output = cv2.threshold(output, gui.threshold, 255, 0)
            monitor.add("Threshold", output)

        return output
