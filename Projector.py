import numpy as np
import cv2

class Projector(object):
    name = 'canvas_window'

    def __int__(self):
        print("Projector init")
        cv2.startWindowThread()


    def white(self):
        print('white')
        white_image = np.zeros([768, 1024, 1], dtype=np.uint8)
        white_image.fill(255)
        cv2.namedWindow(self.name, flags=cv2.WINDOW_GUI_NORMAL)
        cv2.moveWindow(self.name, 3841, 0)
        cv2.imshow(self.name, white_image)
        cv2.setWindowProperty(self.name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def black(self):
        print('black')
        black_image = np.zeros([768, 1024, 1], dtype=np.uint8)
        black_image.fill(1)
        cv2.imshow(self.name, black_image)

    def red(self):
        print('black')
        red = np.zeros([768, 1024, 1], dtype=np.uint8)
        image[:] = (0, 0, 125)
        cv2.imshow(self.name, red)
