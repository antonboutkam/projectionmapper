import numpy as np
import cv2


class Projector(object):
    name = 'canvas_window'
    screen_res = (1024, 768)

    def __int__(self):
        # Print("Projector init")
        cv2.startWindowThread()

    def white(self):
        self.light(255)

    def light(self, luminosity):
        white_image = np.zeros([self.screen_res[1], self.screen_res[0], 1], dtype=np.uint8)
        white_image.fill(luminosity)
        # white_image = cv2.cvtColor(white_image, cv2.COLOR_GRAY2BGR)
        cv2.namedWindow(self.name, flags=cv2.WINDOW_GUI_NORMAL)
        # color = (255,0,0)
        # white_image = cv2.rectangle(white_image, (33, 33), (w-36, h-36), color, 13)

        # color = (0, 255, 0)
        # white_image = cv2.rectangle(white_image, (133, 133), (w - 136, h - 136), color, 13)

        # color = (0, 0, 255)
        # white_image = cv2.rectangle(white_image, (233, 233), (w - 236, h - 236), color, 13)

        # cv2.moveWindow(self.name, 1920, 0)
        # cv2.moveWindow(self.name, 3841, 0)
        #        cv2.moveWindow(self.name, 1024, 0)
        cv2.moveWindow(self.name, 1440, 0)
        cv2.imshow(self.name, white_image)
        cv2.setWindowProperty(self.name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def black(self):
        print('black')
        black_image = np.zeros([self.screen_res[1], self.screen_res[0], 1], dtype=np.uint8)
        black_image.fill(0)
        cv2.imshow(self.name, black_image)

    def red(self):
        # Print('red')
        # Center
        #  b, g, r: (24, 37, 39)
        #  Left top
        # b, g, r: (26, 18, 29)
        # Right bottom
        # b, g, r: (27, 26, 30)

        red = np.zeros([self.screen_res[1], self.screen_res[0], 3], dtype=np.uint8)
        # red[:] = (0, 255, 255)
        red[:] = (255, 0, 0)
        cv2.imshow(self.name, red)

    def draw(self, frame):
        # frame = cv2.resize(frame, (self.screen_res[0], self.screen_res[1]))
        cv2.imshow(self.name, frame)
