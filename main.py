import pyxel
import numpy as np
from src.camera import Camera


class App:
    def __init__(self):
        pyxel.init(160, 120, fps=60)
        pyxel.mouse(visible=True)

        h_angle = 0
        v_angle = 0
        z_angle = 0
        distance = 10

        self.camera = Camera(
            pos=np.array([5 * 25, -10, 5 * 25]),
            h_angle=h_angle,
            v_angle=v_angle,
            z_angle=z_angle,
            screen_d=distance,
            screen_w=160,
            screen_h=120,
        )
        self.move_velo = 0.1

        pyxel.run(self.update, self.draw)

    def update(self):
        # 移動
        if pyxel.btn(pyxel.KEY_W):
            self.camera.move(
                self.move_velo * np.sin(self.camera.camera_h_angle),
                0,
                self.move_velo * np.cos(self.camera.camera_h_angle),
            )
        if pyxel.btn(pyxel.KEY_S):
            self.camera.move(
                -self.move_velo * np.sin(self.camera.camera_h_angle),
                0,
                -self.move_velo * np.cos(self.camera.camera_h_angle),
            )
        if pyxel.btn(pyxel.KEY_K):
            self.camera.move(0, -self.move_velo, 0)
        if pyxel.btn(pyxel.KEY_J):
            self.camera.move(0, self.move_velo, 0)

        # 角度調整
        v = 360
        if pyxel.btn(pyxel.KEY_LEFT):
            self.camera.rotate(-np.pi / v, 0, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.camera.rotate(np.pi / v, 0, 0)
        if pyxel.btn(pyxel.KEY_UP):
            self.camera.rotate(0, np.pi / v, 0)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.camera.rotate(0, -np.pi / v, 0)

        # 奥行スケールを調整
        if pyxel.btn(pyxel.KEY_Z):
            self.camera.z_prime_handler += 0.01
        if pyxel.btn(pyxel.KEY_X):
            self.camera.z_prime_handler -= 0.01

        if pyxel.btn(pyxel.KEY_H):
            self.camera.rotate(0, 0, np.pi / v)
        if pyxel.btn(pyxel.KEY_G):
            self.camera.rotate(0, 0, -np.pi / v)

    def draw_debug(self):
        """
        デバッグ情報を出力
        """
        pyxel.text(0, 0, "camera_pos: " + str(self.camera.camera_pos), 7)
        pyxel.text(0, 8, "h_angle: " + str(np.rad2deg(self.camera.camera_h_angle)), 7)
        pyxel.text(0, 16, "w_angle: " + str(np.rad2deg(self.camera.camera_v_angle)), 7)
        pyxel.text(0, 24, "z_prime: " + str(self.camera.z_prime_handler), 7)

    def draw(self):
        pyxel.cls(0)
        d = 20
        for z in range(50):
            for x in range(50):
                pos = self.camera.cal_pos_on_screen(np.array([x * 5, 0, z * 5]))
                if pos != None:
                    px, py, pd = pos
                    pyxel.pset(px, py, (8 if ((x + z) % d == 0) else 7))
        self.draw_debug()


App()
