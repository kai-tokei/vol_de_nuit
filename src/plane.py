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

    def cal_direction(self) -> np.array:
        """機体が進む方向を計算"""
        pass

    def yaw_right(self):
        """右旋回"""
        self.yaw_a = self.yaw_speed
        self.yaw_v += self.yaw_a

    def yaw_left(self):
        """左旋回"""
        self.yaw_a = -self.yaw_speed
        self.yaw_v += self.yaw_a

    def pitch_up(self):
        """上昇"""
        self.pitch -= self.pitch_speed

    def pitch_down(self):
        """下降"""
        self.pitch += self.pitch_speed

    def update(self):
        """操作処理"""

        # 角速度を更新
        self.yaw_v += self.yaw_a

        # 最大角速度制限
        self.yaw_v = np.clip(self.yaw_v, -self.max_yaw_v, self.max_yaw_v)

        # yaw角を更新（角速度で積分）
        self.yaw += self.yaw_v

        # 減衰（角速度が0に近づくように）
        self.yaw_v *= 0.99

        # 360度でループ
        self.yaw = self.yaw % 360

        # pitchが時間とともに減衰
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

        # 正規化
        direction = direction / np.linalg.norm(direction)

        # 速度の計算
        self.a_inertial = self.a * direction
        self.v_inertial += self.a_inertial

        # 速度を自然減衰させる
        self.v_inertial *= 0.98

        # 座標移動
        self.pos += self.v_inertial

        self.pos += self.v_inertial  # 位置を更新

        self.yaw_a = 0.0  # 入力がない場合は角加速度を0に

    def draw(self, camera: Camera):
        pass
        # s_pos = camera.cal_pos_on_screen(self.pos)
        # d_pos = camera.cal_pos_on_screen(self.pos + self.v_inertial * 3)

        # if s_pos is not None and d_pos is not None:
        #     sx, sy, _ = s_pos
        #     dx, dy, _ = d_pos
        #     pyxel.line(sx, sy, dx, dy, 5)
