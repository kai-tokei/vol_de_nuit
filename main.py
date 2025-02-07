import pyxel
import numpy as np
from src.camera import Camera


class Plane:
    def __init__(self):
        self.pos = np.array([200, -100.0, 0.0])  # 初期位置
        self.a_inertial = np.array([0.0, 0.0, 0.0])  # 慣性座標系の加速度
        self.v_inertial = np.array([0.0, 0.0, 0.0])  # 慣性座標系の速度
        self.v_world = np.array([0.0, 0.0, 0.0])
        self.a = 0.01
        self.pitch = 0.0  # 上下の角度
        self.yaw = 0.0  # 左右の角度
        self.yaw_a = 0.0  # yaw方向の角加速度
        self.yaw_v = 0.0  # yaw方向の角速度
        self.max_yaw_v = 0.5  # 最大角速度
        self.yaw_speed = 0.008  # 旋回速度（1回の操作での最大角度変化）
        self.pitch_speed = 0.3  # 旋回速度（1回の操作での最大角度変化）

    def update(self):
        """操作処理"""
        # 機体の向きを操作
        if pyxel.btn(pyxel.KEY_A):
            self.yaw_a = -self.yaw_speed  # 左旋回
        elif pyxel.btn(pyxel.KEY_D):
            self.yaw_a = self.yaw_speed  # 右旋回
        else:
            self.yaw_a = 0.0  # 入力がない場合は角加速度を0に
        if pyxel.btn(pyxel.KEY_W):
            self.pitch += self.pitch_speed
        if pyxel.btn(pyxel.KEY_S):
            self.pitch -= self.pitch_speed

        # 角速度を更新
        self.yaw_v += self.yaw_a
        # 最大角速度制限
        self.yaw_v = np.clip(self.yaw_v, -self.max_yaw_v, self.max_yaw_v)

        # yaw角を更新（角速度で積分）
        self.yaw += self.yaw_v

        # 減衰（角速度が0に近づくように）
        self.yaw_v *= 0.99

        self.yaw = self.yaw % 360  # 360度でループ
        # 旋回が時間とともに減衰
        self.pitch *= 0.99

        # 機体の向きに基づいて速度を決定
        yaw_rad = np.radians(self.yaw)
        pitch_rad = np.radians(self.pitch)

        direction = np.array(
            [
                np.sin(yaw_rad),  # 左右の旋回
                np.sin(pitch_rad),  # 上下の旋回
                np.cos(yaw_rad) * np.cos(pitch_rad),  # 前方への進行
            ]
        )

        direction = direction / np.linalg.norm(direction)  # 正規化

        self.a_inertial = self.a * direction
        self.v_inertial += self.a_inertial
        self.v_inertial *= 0.98  # 減衰
        self.pos += self.v_inertial

        # 徐々に前進方向へ戻る
        # velocity = self.velocity * 0.95 + self.default_velocity * 0.05
        # velocity = self.velocity / np.linalg.norm(self.velocity)  # 正規化

        self.pos += self.v_inertial  # 位置を更新

    def draw(self, camera: Camera):
        s_pos = camera.cal_pos_on_screen(self.pos)
        d_pos = camera.cal_pos_on_screen(self.pos + self.v_inertial * 3)

        if s_pos is not None and d_pos is not None:
            sx, sy, _ = s_pos
            dx, dy, _ = d_pos
            pyxel.line(sx, sy, dx, dy, 5)


class App:
    def __init__(self):
        pyxel.init(160, 120, fps=60)
        pyxel.mouse(visible=True)

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
        self.plane.update()
        self.camera.set_pos(self.plane.pos[0], self.plane.pos[1], self.plane.pos[2])
        self.camera.set_angle(np.radians(self.plane.yaw), np.radians(self.plane.pitch))

        # 角度調整
        v = 360
        if pyxel.btn(pyxel.KEY_A):
            self.camera.rotate(-np.pi / v, 0, 0)
        if pyxel.btn(pyxel.KEY_D):
            self.camera.rotate(np.pi / v, 0, 0)
        if pyxel.btn(pyxel.KEY_UP):
            self.camera.rotate(0, -np.pi / v, 0)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.camera.rotate(0, np.pi / v, 0)

    def draw_debug(self):
        """
        デバッグ情報を出力
        """
        pyxel.text(0, 0, "camera_pos: " + str(self.camera.camera_pos), 7)
        pyxel.text(0, 8, "h_angle: " + str(np.rad2deg(self.camera.camera_h_angle)), 7)
        pyxel.text(0, 16, "w_angle: " + str(np.rad2deg(self.camera.camera_v_angle)), 7)
        pyxel.text(0, 24, "z_prime: " + str(self.camera.z_prime_handler), 7)
        pyxel.text(0, 32, "plane yaw: " + str(self.plane.yaw), 7)
        pyxel.text(0, 40, "plane pitch: " + str(self.plane.pitch), 7)

    def draw(self):
        pyxel.cls(0)
        d = 50
        for z in range(50):
            for x in range(50):
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
        # self.draw_debug()


App()
