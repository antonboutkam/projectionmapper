import numpy as np
import cv2


class Cam(object):
    width = 1280
    height = 720
    video_channel = 0
    # gphoto2 - -stdout - -capture - movie | gst - launch - 0.10 fdsrc ! decodebin2 name = dec ! queue ! ffmpegcolorspace ! v4l2sink device = /dev/video2
    vid = cv2.VideoCapture(video_channel)
    last_frame = None
    gui = None

    # vid = cv2.VideoCapture(2)

    def start(self, gui):
        #        print('x')
        # self.vid = cv2.VideoCapture(3)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.gui = gui
        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        # self.vid.set(6, codec)
        # self.vid.set(5, 15)
        # self.vid.set(3, 1280)
        # self.vid.set(4, 720)
        # self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 8000)
        # self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 8000)
        # self.vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        # self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
        # self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 2048)
        # self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        # self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        # self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        # self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        # self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        # self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def picture(self):
        while True:
            ret, frame = self.vid.read()
            if not ret and self.last_frame is None:
                print('wait cam')
                self.video_channel = self.video_channel + 1
                if self.video_channel > 3:
                    self.video_channel = 0
                # print('try channel' + str(self.video_channel))
                self.vid = cv2.VideoCapture(self.video_channel)
                self.start(self.gui)
                continue
            elif not ret:
                # print('cam fail')
                return self.last_frame
            else:
                if self.gui.main_vertical_flip_cam:
                    frame = cv2.flip(frame, 0)

                self.last_frame = self.area_of_interest(frame)
                return frame

    def area_of_interest(self, frame):
        if self.gui.cut_left > 0 or self.gui.cut_right > 0 or self.gui.cut_top > 0 or self.gui.cut_bottom > 0:
            frame_black = np.zeros_like(frame)
            s = frame_black.shape

            y_t = self.gui.cut_top
            y_b = s[0] - self.gui.cut_bottom
            x_l = self.gui.cut_left
            x_r = s[1] - self.gui.cut_right

            frame_black[y_t:y_b, x_l:x_r] = frame[y_t:y_b, x_l:x_r]
            return frame_black
        return frame
