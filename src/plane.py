import pyxel
import numpy as np
from src.camera import Camera


class Plane:
    def __init__(self):
        self.pos = np.array([200, -10.0, 0.0])  # 初期位置
        self.gravity = np.array([0, 0.00098, 0])
        self.a_inertial = np.array([0.0, 0.0, 0.0])  # 慣性座標系の加速度
        self.v_inertial = np.array([0.0, 0.0, 0.0])  # 慣性座標系の速度
        self.v_world = np.array([0.0, 0.0, 0.0])
        self.a = 0.0
        self.a_max = 0.008
        self.a_d = 0.00001
        self.pitch = 0.0  # 上下の角度
        self.default_pitch = 90  # 空中で操作しないと下を向く
        self.roll = 0.0  # 回転の角度
        self.yaw = 0.0  # 左右の角度
        self.yaw_a = 0.0  # yaw方向の角加速度
        self.yaw_v = 0.0  # yaw方向の角速度
        self.max_yaw_v = 0.5  # 最大角速度
        self.yaw_speed = 0.005  # 旋回速度（1回の操作での最大角度変化）
        self.pitch_speed = 0.5  # 旋回速度（1回の操作での最大角度変化）
        self.roll_speed = 0.4  # 回転速度

    def get_direction(self, yaw, pitch, roll):
        yaw_rad = np.radians(yaw)
        pitch_rad = np.radians(pitch)
        roll_rad = np.radians(roll)

        # ヨー（Z軸回転）
        R_roll = np.array(
            [
                [np.cos(roll_rad), -np.sin(roll_rad), 0],
                [np.sin(roll_rad), np.cos(roll_rad), 0],
                [0, 0, 1],
            ]
        )

        # ピッチ（X軸回転）
        R_pitch = np.array(
            [
                [1, 0, 0],
                [0, np.cos(pitch_rad), np.sin(pitch_rad)],
                [0, -np.sin(pitch_rad), np.cos(pitch_rad)],
            ]
        )

        # ロール（Y軸回転）
        R_yaw = np.array(
            [
                [np.cos(yaw_rad), 0, np.sin(yaw_rad)],
                [0, 1, 0],
                [np.sin(yaw_rad), 0, np.cos(yaw_rad)],
            ]
        )

        # - まず Roll（ロール）を適用して機体を傾ける
        # - 次に Pitch（ピッチ）を適用して機首を上下させる
        # - 最後に Yaw（ヨー）を適用して左右旋回させる
        R = R_roll @ R_yaw @ R_pitch

        # 機体のデフォルト進行方向（前方 = +Z軸）
        default_direction = np.array([0, 0, 0.5])

        # 回転行列を適用
        direction = R @ default_direction

        # 正規化
        direction = direction / np.linalg.norm(direction)

        return direction

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

    def roll_right(self):
        """右回転"""
        self.roll -= self.roll_speed

    def roll_left(self):
        """左回転"""
        self.roll += self.roll_speed

    def speed_up(self):
        """速度上げる"""
        self.a = min(self.a + self.a_d, self.a_max)
        print(self.a)

    def speed_down(self):
        """速度下げる"""
        self.a = max(self.a - self.a_d, 0)
        print(self.a)

    def _attenution(self):
        """減衰処理"""
        self.yaw_v *= 0.99
        if self.a > self.a_max / 4:
            self.pitch *= 0.99
        else:
            self.pitch += (self.default_pitch - self.pitch) * 0.001
        self.v_inertial *= 0.99
        self.roll *= 0.99
        self.yaw_a = 0.0  # 入力がない場合は角加速度を0に

    def update(self):
        """操作処理"""

        self.yaw_v += self.yaw_a  # 角速度を更新
        self.yaw_v = np.clip(
            self.yaw_v, -self.max_yaw_v, self.max_yaw_v
        )  # 最大角速度制限

        # yaw角を更新
        self.yaw += self.yaw_v
        self.yaw = self.yaw % 360

        direction = self.get_direction(self.yaw, self.pitch, self.roll)

        # 速度の計算
        self.a_inertial = (self.a) * direction
        self.v_inertial += self.a_inertial + self.gravity * (
            abs(self.a_max - self.a) / self.a_max
        )

        # 座標移動
        self.pos += self.v_inertial

        # 減衰処理
        self._attenution()

    def draw(self, camera: Camera):
        s_pos = camera.cal_pos_on_screen(self.pos + 0.01)
        d_pos = camera.cal_pos_on_screen(self.pos + 0.01 + self.v_inertial * 10)

        if s_pos is not None and d_pos is not None:
            sx, sy, _ = s_pos
            dx, dy, _ = d_pos
            pyxel.line(sx, sy, dx, dy, 5)
