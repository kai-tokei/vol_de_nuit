import pyxel
import numpy as np
from src.camera import Camera


class Plane:
    R_AILERON_LIMIT: float = np.pi / 6  # 右舷エルロンの最大角度
    L_AILERON_LIMIT: float = np.pi / 6  # 左舷エルロンの最大角度
    RE_AILERON_LIMIT: float = np.pi / 6  # 尾翼エレベーターの最大角度
    V_STAB_LIMIT: float = np.pi / 6  # 垂直尾翼の最大角度
    ACCELERATION_LIMIT: float = 100  # 加速度の最大値

    def __init__(self):
        """
        飛行機の基本状態を定義
        """
        self.pos = np.array([0.0, 0.0, 1000.0])  # 初期座標 (高度1000m)
        self.gravity = np.array([0, 0, -9.8])  # 重力加速度 (m/s^2)
        self.weight = 3000  # 機体の重量 (kg)
        self.thrust = np.array([0.0, 0.0, 0.0])  # 推力 (N)
        self.acceleration = np.array([0.0, 0.0, 0.0])  # 加速度 (m/s^2)
        self.velocity = np.array([50.0, 0.0, 0.0])  # 初期速度 (m/s)
        self.direction = np.array([1.0, 0.0, 0.0])  # 初期進行方向

        # 操縦桿の情報
        self.roll: float = 0  # 操縦桿の横割合
        self.elevation: float = 0  # 操縦桿の縦割合
        self.pedal: float = 0  # ラダーペダルの割合

        # 動翼の初期方向 (単位ベクトル)
        self.r_aileron = np.array([1.0, 0.0, 0.0])  # 右舷エルロン
        self.l_aileron = np.array([-1.0, 0.0, 0.0])  # 左舷エルロン
        self.re_aileron = np.array([0.0, 0.0, -1.0])  # 尾翼エレベーター
        self.v_stab = np.array([0.0, 1.0, 0.0])  # 垂直尾翼

        self.angular = np.array([0.0, 0.0, 0.0])  # 角速度 (rad/s)

    def controll_roll(self, d: float):
        """
        操縦桿の割合を制御
        """
        self.roll += d
        if abs(self.roll) > 1.0:
            self.roll = 1.0 * np.sign(self.roll)

    def controll_elevation(self, d: float):
        """
        操縦桿の縦割合を制御
        """
        self.elevation += d
        if abs(self.elevation) > 1.0:
            self.elevation = 1.0 * np.sign(self.elevation)


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
