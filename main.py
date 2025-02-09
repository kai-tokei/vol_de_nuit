import pyxel
import numpy as np

from src.camera import Camera
from src.plane import Plane
from src.kyes import InputDetector as Input


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
        self.move_velo = 0.1

        pyxel.run(self.update, self.draw)

    def update(self):
        self.camera.set_pos(self.plane.pos[0], self.plane.pos[1], self.plane.pos[2])
        self.camera.set_angle(
            np.radians(self.plane.direction[0]),
            np.radians(self.plane.direction[1]),
            np.radians(self.plane.direction[2]),
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

    def draw_debug(self):
        """
        デバッグ情報を出力
        """
        pyxel.text(0, 0, "camera_pos: " + str(self.camera.camera_pos), 7)
        pyxel.text(0, 8, "h_angle: " + str(np.rad2deg(self.camera.camera_h_angle)), 7)
        pyxel.text(0, 16, "w_angle: " + str(np.rad2deg(self.camera.camera_v_angle)), 7)
        pyxel.text(0, 24, "z_angle: " + str(np.rad2deg(self.camera.camera_z_angle)), 7)
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


App()
