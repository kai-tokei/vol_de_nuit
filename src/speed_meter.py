import pyxel
import numpy as np
from animation import Animation
from frame import Frame


class SpeedMeter:
    def __init__(self):
        self.x = 35
        self.y = 98
        self.anime = Animation("assets/images/speed_meter-Sheet.png", 20, 20)
        self.anime.add(label="normal", frame=Frame(1, [0]))
        self.anime.set("normal")
        self.anime.play(loop=False)
        self.img = pyxel.Image(20, 20)

        self.ratio = 0

    def set_ratio(self, ratio):
        """割合を設定"""
        self.ratio = ratio

    def update(self):
        self.anime.update()

    def draw(self):
        self.img.cls(0)
        for i in range(100):
            w = 95
            x = (-w * self.ratio) + 10 + i * 4
            y = 12
            h = 3
            self.img.text(x - 1, y - 6, str(i * 2 if i % 4 == 0 else ""), 3)
            if i % 4 == 0:
                self.img.line(x, y + h, x, y, 3)
            else:
                self.img.line(x, y + h, x, y + h / 2, 3)
        pyxel.blt(self.x, self.y, self.img, 0, 0, 20, 20)
        self.anime.draw(self.x, self.y, colKey=4)
