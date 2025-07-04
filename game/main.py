import pyxel
import numpy as np

from src.camera import Camera
from src.plane import Plane
from src.kyes import InputDetector as Input
from src.animation import Animation
from src.frame import Frame
from src.altimeter import Altimeter
from src.attitude_indicator import AttitudeIndicator
from src.speed_meter import SpeedMeter
from src.utils import cal_pitch_rot, cal_roll_rot, cal_yaw_rot


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Vol de nuit", fps=60)
        pyxel.screen_mode(2)

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
        self.attitude_indicator = AttitudeIndicator()

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

        # 計器類の計算
        self.speed_meter.update()
        self.altimeter.update()
        self.attitude_indicator.update()
        self.speed_meter.set_ratio(
            np.linalg.norm(self.plane.vec) / self.plane.SPEED_MAX
        )
        self.altimeter.set_ratio(max(self.plane.pos[1], -500) / (-500))
        self.attitude_indicator.set_ratio(
            np.rad2deg(self.plane.pitch) / 90, np.rad2deg(-self.plane.roll) / 90
        )

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
        for z in range(150):
            for x in range(150):
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
        self.attitude_indicator.draw()


App()
