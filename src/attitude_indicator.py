import pyxel
from .animation import Animation
from .frame import Frame


class AttitudeIndicator:
    def __init__(self):
        self.x = 66
        self.y = 91
        self.anime = Animation("assets/images/attitude_indicator.png", 28, 28)
        self.anime.add(label="normal", frame=Frame(1, [0]))
        self.anime.set("normal")
        self.anime.play(loop=False)
        self.horizon = pyxel.Image.from_image("assets/images/horizon.png")
        self.img = pyxel.Image(64, 64)

        self.pitch_ratio = 0
        self.roll_ratio = 0

    def set_ratio(self, pitch_ratio, roll_ratio):
        """割合を設定"""
        self.pitch_ratio = pitch_ratio
        self.roll_ratio = roll_ratio

    def update(self):
        self.anime.update()

    def draw(self):
        self.img.cls(0)
        self.img.blt(
            0,
            0,
            self.horizon,
            0,
            self.pitch_ratio * 0.5,
            64,
            64,
            rotate=self.roll_ratio,
        )
        pyxel.blt(self.x, self.y, self.img, 20, 20, 22, 24)
        self.anime.draw(self.x, self.y, colKey=4)
