import pyxel
import numpy as np
from src.camera import Camera


class Plane(Camera):
    R_WING_LIMIT: float = np.pi / 6
    L_WING_LIMIT: float = np.pi / 6
    RE_WING_LIMIT: float = np.pi / 6
    V_STAB_LIMIT: float = np.pi / 6
    ACCELERATION_LIMIT: float = 100

    def __init__(self, pos, h_angle, v_angle, z_angle, screen_d, screen_w, screen_h):
        super().__init__(pos, h_angle, v_angle, z_angle, screen_d, screen_w, screen_h)
        """
        gravity: 重力加速度(m/s^2)
        weight: 重量(kg)
        thrust: 推力(N)
        acceleration: 加速度ベクトル(m/s^2)
        velocity: 速度ベクトル(m/s)
        direction: 機体の単位方向ベクトル
        r_wing: 右舷の動翼の単位方向ベクトル
        l_wing: 左舷の動翼の単位方向ベクトル
        re_wing: 尾翼の単位方向ベクトル
        v_stab: 垂直尾翼の単位方向ベクトル
        angular: 回転モーメントベクトル
        """
        self.gravity = 9.8
        self.weight: int = 3000
        self.thrust: np.array
        self.acceleration: np.array
        self.velocity: np.array
        self.direction: np.array
        self.r_wing: np.array
        self.l_wing: np.array
        self.re_wing: np.array
        self.v_stab: np.array
        self.angular: np.array

    """
    モーメントの計算処理
    M = F x L
    """

    def update(self):
        pass


class App:
    def __init__(self):
        pyxel.init(160, 120, fps=60)
        pyxel.mouse(visible=True)

        self.camera = Plane(
            pos=np.array([5 * 25, -2.5, 5 * 25]),
            h_angle=0,
            v_angle=0,
            z_angle=0,
            screen_d=10,
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
