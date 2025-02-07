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
