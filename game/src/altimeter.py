import pyxel
import numpy as np
from .animation import Animation
from .frame import Frame


class Altimeter:
    def __init__(self):
        self.x = 105
        self.y = 98
        self.anime = Animation("assets/images/altimeter.png", 20, 20)
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
        r = 7
        rad = -self.ratio * 2 * np.pi
        self.anime.draw(self.x, self.y, colKey=4)
        self.img.cls(0)
        self.img.line(
            10,
            10,
            10 + r * np.cos(rad),
            10 + r * np.sin(rad),
            3,
        )
        pyxel.blt(self.x, self.y, self.img, 0, 0, 20, 20, colkey=0)
