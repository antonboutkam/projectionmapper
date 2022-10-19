import numpy as np
import cv2

class Cam(object):
    vid = None

    def __int__(self):
        # define a video capture object
        self.vid = cv2.VideoCapture(0)
        self.vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 2048)

    def picture(self):
        ret, frame = self.vid.read()
        return frame
