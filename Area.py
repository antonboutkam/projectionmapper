from Cam import Cam


class Area:
    top_y = None
    top_x = None
    bottom_y = None
    bottom_x = None
    cam = None

    def init(self, top_y, bottom_y, top_x, bottom_x):
        self.top_y = top_y
        self.bottom_y = bottom_y
        self.top_x = top_x
        self.bottom_x = bottom_x
        self.cam = Cam()

    def capture(self):
        picture = self.cam.picture()
        out = picture[self.top_y:self.bottom_y + 1, self.top_x:self.bottom_x + 1]
        return out
