import numpy as np
import cv2

class Cam(object):
    vid = cv2.VideoCapture(2)

    def __int__(self):
        print("Init cam")
        # define a video capture object
        self.vid = cv2.VideoCapture(0)
        self.vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        # self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
        # self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 2048)
        # self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        # self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        # self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        # self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

    def picture(self):
        while True:
            ret, frame = self.vid.read()
            if ret:
                break
        return frame
