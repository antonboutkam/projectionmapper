import cv2
import numpy as np
import os

class Source:
    vidcap = None
    try_count = None
    clips = None
    current_clip = None
    gui = None

    def start(self, gui):
        self.gui = gui
        self.load_playlist()
        self.current_clip = 0
        self.try_count = 0
        self.vidcap = cv2.VideoCapture('../loops/' + self.clips[self.current_clip])

    def load_playlist(self):
        self.clips = []
        for filename in os.scandir('../loops/'):
            if filename.is_file():
                self.clips.append(filename.path)
                print("Add " + filename.path + " to the playlist")

    def frame(self):
        if self.gui.video_source == 0:
            white_image = np.zeros([768, 1024, 1], dtype=np.uint8)
            white_image.fill(self.gui.video_source_brightness)
            return white_image

        success = False
        self.try_count = 0
        while not success:
            success, image = self.vidcap.read()
            self.try_count = self.try_count + 1
            if self.try_count > 2:
                self.current_clip = self.current_clip + 1
                if self.current_clip == len(self.clips):
                    self.start(self.gui)

            if success:
                image = self.make_square(image)
                image = self.adjust_brightness(image, self.gui.video_source_brightness)
                return image

    def make_square(self, image):
        shape = image.shape
        h = shape[1]
        w = shape[2]
        smallest = None
        if h > w:
            wh = w
            y = h / 2 - wh / 2
            return self.crop(image, 0, y, wh, wh)
        else:
            wh = h
            x = w / 2 - wh / 2
            return self.crop(image, y, 0, wh, wh)

    def crop(self, image, x, y, w, h):
        return image[int(y):int(y + h), int(x):int(x + w)]

    def adjust_brightness(self, image, value):
        value = 127 - value
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.add(v, value)
        v[v > 255] = 255
        v[v < 0] = 0
        final_hsv = cv2.merge((h, s, v))
        out = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return out
