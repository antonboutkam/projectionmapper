import cv2
import numpy as np

class Source:
    vidcap = None
    try_count = None
    clips = [
        # 'littleboxes.mp4',
        # 'network.mp4',
        'spinning.mp4',
        'glytchghost.mov',
        'twisted hall.mov',
        'twirlers.mov'
        # 'plugs slower.mov'
    ]
    current_clip = 0
    gui = None

    def start(self, gui):
        # self.vidcap = cv2.VideoCapture('../loops/littleboxes.mp4')
        self.vidcap = cv2.VideoCapture('../loops/' + self.clips[self.current_clip])
        self.gui = gui

    def frame(self):
        if self.gui.video_source == 0:
            white_image = np.zeros([1024, 1024, 1], dtype=np.uint8)
            white_image.fill(self.gui.video_source_brightness)
            return white_image

        success = False
        self.try_count = 0;
        while not success:
            success, image = self.vidcap.read()
            self.try_count = self.try_count + 1
            if self.try_count > 5:
                self.try_count = 0
                self.current_clip = self.current_clip + 1
                if self.current_clip == len(self.clips):
                    self.current_clip = 0
                self.start(self.gui)
            if success:
                return cv2.resize(self.adjust_brightness(image, self.gui.video_source_brightness),(768, 1024))

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
