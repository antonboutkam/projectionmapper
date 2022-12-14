import cv2
import math
import numpy as np
import math


class Monitor:
    frames = []
    desired_width = 250
    desired_size = None
    desired_ratio = None
    column_count = 4
    gui = False

    def start(self, gui, aspect_ratio):
        self.gui = gui
        self.desired_ratio = aspect_ratio
        height = math.ceil(self.desired_width / aspect_ratio)
        self.desired_size = (self.desired_width, height)

    def add_gpu(self, title, frame):
        if not self.gui.main_show_monitor:
            return None
        self.add(title, frame.download())

    def add(self, title, frame):
        # print(title)
        if not self.gui.main_show_monitor:
            return None
        # print("Add to monitor: " + title + " ", frame.shape)
        # print("Desired", self.desired_size)
        # print("Aspect", self.desired_ratio)
        curr_w = frame.shape[1]
        curr_h = frame.shape[0]
        curr_r = curr_w / curr_h

        desired_width = self.desired_size[0]
        desired_height = self.desired_size[1]

        # print("curr_r:", curr_r, " curr_w: ", curr_w, " curr_h: ", curr_h)
        # print("desired_width:", desired_width, " desired_height: ", desired_height)

        if curr_r == self.desired_ratio:
            resized_frame = cv2.resize(frame, (desired_width, desired_height))
            # print("resize method 1:", (desired_width, desired_height))
        elif curr_r < self.desired_ratio:
            resize_width = desired_width
            resize_factor = desired_width / curr_w
            # print("resize factor 1", resize_factor)
            resize_height = math.ceil(curr_h * resize_factor)
            dsize = (resize_height, resize_width)
            # print("resize method 2:", dsize)
            # print("Resize 1", dsize)
            intermediate_frame = cv2.resize(frame, dsize)
            # print("Crop 1 ", desired_width, ":", desired_height)
            resized_frame = intermediate_frame[0:desired_height, 0:desired_width]
        elif curr_r > self.desired_ratio:
            resize_height = desired_height
            resize_factor = desired_height / curr_h
            # print("resize factor 2", resize_factor)
            resize_width = math.ceil(curr_w * resize_factor)
            dsize = (resize_height, resize_width)
            # print("resize method 3:", dsize)
            # print("Resize 2", dsize)
            intermediate_frame = cv2.resize(frame, dsize)
            # print("Crop 2 ", desired_width, ":", desired_height)
            resized_frame = intermediate_frame[0:desired_height, 0:desired_width]
        else:
            raise Exception("Cannot resize, this situation should never occur")

        # cv2.imwrite("preview.jpg", resized_frame)

        resized_frame = self.add_text(title, resized_frame, curr_w, curr_h, curr_r)
        self.frames.append(resized_frame)

    def add_text(self, text, resized_frame, curr_w, curr_h, curr_r):
        # return False
        font = cv2.FONT_HERSHEY_SIMPLEX

        fontScale = 1
        fontColor = (255, 255, 255)
        thickness = 1
        lineType = 2

        cv2.putText(resized_frame, text,
                    (20, 20),
                    font,
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)

        w = str(curr_w)
        h = str(curr_h)
        r = str(curr_r)
        cv2.putText(resized_frame, "w:" + w + ", h:" + h + ", r" + r, (20, 40),
                    font,
                    .6,
                    fontColor,
                    thickness,
                    lineType)
        return resized_frame

    def display(self):
        if not self.gui.main_show_monitor:
            return None
        # return False
        x = 0
        y = 0
        total_width = (self.desired_size[0] * self.column_count) + 1
        total_height = self.desired_size[1]
        frame_count = len(self.frames)
        # print("Frame count ", len(self.frames), "Column count", self.column_count)
        if frame_count > self.column_count:
            row_count = math.ceil(frame_count / self.column_count)
            total_height = (self.desired_size[1] * row_count) + 1

        shape = [total_height, total_width]
        # print("Preview container shape ", shape)
        preview_container = np.zeros(shape, np.uint8)
        preview_container = cv2.cvtColor(preview_container, cv2.COLOR_GRAY2BGR)
        # print(preview_container)

        horizontal_move = 0
        vertical_move = 0
        index = 0
        for frame in self.frames:
            # # print(frame)
            h = frame.shape[0]
            w = frame.shape[1]

            if len(frame.shape) == 2:
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

            # print("Add: ", index, " fc:", len(self.frames), " cc:", self.column_count, " image: ", y, ":", h, ",", x, ":", w)

            if (index % self.column_count) == 0 and index != 0:
                horizontal_move = 0
                vertical_move = vertical_move + h
            # print("Index:", index, "Horizontal", (w + horizontal_move), "vertical: ", (h + vertical_move))
            # print("Frame shape", frame.shape)
            # print((y + vertical_move), ':', (h + vertical_move), ',', (x + horizontal_move), ':', (w + horizontal_move))

            # l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
            preview_container[vertical_move: vertical_move + h, horizontal_move: horizontal_move + w] = frame
            horizontal_move = horizontal_move + w
            index = index + 1

        self.frames.clear()
        cv2.imshow("Monitor", preview_container)


if __name__ == "__main__":
    monitor = Monitor()
    monitor.add('Een', cv2.imread('./assets/testbeeld.jpg'))
    monitor.add('Twee', cv2.imread('./assets/testbeeld.jpg'))
    monitor.add('Drie', cv2.imread('./assets/testbeeld.jpg'))
    monitor.add('Vier', cv2.imread('./assets/testbeeld.jpg'))
    monitor.add('Vijf', cv2.imread('./assets/testbeeld.jpg'))
    monitor.add('Zes', cv2.imread('./assets/testbeeld.jpg'))
    monitor.add('Zeven', cv2.imread('./assets/testbeeld.jpg'))
    monitor.add('Acht', cv2.imread('./assets/testbeeld.jpg'))
    monitor.add('Negen', cv2.imread('./assets/testbeeld.jpg'))
    monitor.add('Tien', cv2.imread('./assets/testbeeld.jpg'))
    monitor.add('Elf', cv2.imread('./assets/testbeeld.jpg'))
    monitor.add('Twaalf', cv2.imread('./assets/testbeeld.jpg'))
    monitor.display()
