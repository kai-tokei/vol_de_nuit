import pyxel
import numpy as np

from src.camera import Camera
from src.plane import Plane
from src.kyes import InputDetector as Input
from src.animation import Animation
from src.frame import Frame


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


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Vol de nuit", fps=60)

        self.plane = Plane()
        self.camera = Camera(
            pos=np.array([5 * 25, -2.5, 5 * 25]),
            h_angle=0,
            v_angle=np.pi / 8,
            z_angle=0,
            screen_d=10,
            screen_w=160,
            screen_h=120,
        )

        # コックピット
        self.cockpit = Animation("assets/images/cockpit.png", 160, 120)
        self.cockpit.add(label="normal", frame=Frame(1, [0]))
        self.cockpit.set("normal")
        self.cockpit.play(loop=False)

        # 計器類
        self.speed_meter = SpeedMeter()
        self.altimeter = Altimeter()

        pyxel.run(self.update, self.draw)

    def update(self):
        self.camera.set_pos(self.plane.pos[0], self.plane.pos[1], self.plane.pos[2])
        self.camera.set_angle(
            np.radians(self.plane.direction_angle[0]),
            np.radians(self.plane.direction_angle[1]),
            np.radians(self.plane.direction_angle[2]),
        )

        # 機体の向きを操作
        if Input.btn(Input.LEFT):
            self.plane.roll_left()
        if Input.btn(Input.RIGHT):
            self.plane.roll_right()
        if Input.btn(Input.UP):
            self.plane.pitch_down()
        if Input.btn(Input.DOWN):
            self.plane.pitch_up()
        if Input.btn(Input.Y):
            self.plane.yaw_left()
        if Input.btn(Input.A):
            self.plane.yaw_right()
        if Input.btn(Input.X):
            self.plane.speed_up()
        if Input.btn(Input.B):
            self.plane.speed_down()

        self.plane.update()

        self.speed_meter.update()
        self.altimeter.update()
        self.speed_meter.set_ratio(self.plane.vec[2] / self.plane.SPEED_MAX)
        self.altimeter.set_ratio(max(self.plane.pos[1], -500) / (-500))

        self.cockpit.update()

    def draw_debug(self):
        """
        デバッグ情報を出力
        """
        # pyxel.text(0, 0, "camera_pos: " + str(self.camera.camera_pos), 7)
        # pyxel.text(0, 8, "h_angle: " + str(np.rad2deg(self.camera.camera_h_angle)), 7)
        # pyxel.text(0, 16, "w_angle: " + str(np.rad2deg(self.camera.camera_v_angle)), 7)
        # pyxel.text(0, 24, "z_angle: " + str(np.rad2deg(self.camera.camera_z_angle)), 7)
        # pyxel.text(0, 32, "level: " + str(self.plane.levelness), 7)
        # pyxel.text(0, 24, "z_prime: " + str(self.camera.z_prime_handler), 7)
        # pyxel.text(0, 32, "plane yaw: " + str(self.plane.yaw), 7)
        # pyxel.text(0, 40, "plane pitch: " + str(self.plane.pitch), 7)

    def draw(self):
        pyxel.cls(0)
        d = 50
        for z in range(80):
            for x in range(80):
                pos = self.camera.cal_pos_on_screen(np.array([x * 50, 0, z * 50]))
                if pos != None:
                    px, py, pd = pos
                    if pd > 400:
                        pyxel.pset(px, py, (8 if ((x + z) % d == 0) else 1))
                    elif pd > 250:
                        pyxel.pset(px, py, (8 if ((x + z) % d == 0) else 13))
                    else:
                        pyxel.pset(px, py, (8 if ((x + z) % d == 0) else 7))

        self.plane.draw(self.camera)
        self.draw_debug()

        self.cockpit.draw(0, 5, colKey=4)
        self.speed_meter.draw()
        self.altimeter.draw()


App()
