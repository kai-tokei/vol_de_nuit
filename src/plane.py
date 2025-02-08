import pyxel
import numpy as np
from src.camera import Camera


class Plane:
    ROLL_MAX = 45
    PITCH_MAX = 30
    ROLL_SPEED = 0.2
    PITCH_SPEED = 0.2
    YAW_SPEED = 0.2

    def __init__(self):
        self.pos = np.array([500.0, -30.0, 0.0])
        self.vec = np.array([0.0, 0.0, 0.0])
        self.direction = np.array([0.0, 0.0, 0.0])
        self.speed = 2.0
        self.yaw = 0
        self.yaw_v = 0
        self.pitch = 0
        self.pitch_v = 0
        self.roll = 0
        self.roll_v = 0
        self.v = 0

    def yaw_right(self):
        """右旋回"""
        self.yaw_v = self.YAW_SPEED

    def yaw_left(self):
        """左旋回"""
        self.yaw_v = -self.YAW_SPEED

    def pitch_up(self):
        """上昇"""
        self.pitch_v = -self.PITCH_SPEED

    def pitch_down(self):
        """下降"""
        self.pitch_v = self.PITCH_SPEED

    def roll_right(self):
        """右回転"""
        self.roll_v = -self.ROLL_SPEED

    def roll_left(self):
        """左回転"""
        self.roll_v = self.ROLL_SPEED

    def _decrease_params(self):
        """減衰処理"""
        self.yaw_v *= 0.95
        self.pitch_v *= 0.95
        self.roll_v *= 0.95
        # self.roll *= 0.999
        # self.pitch *= 0.999

    def _cal_yaw_rot(self):
        """yawの回転を計算"""
        yaw = np.radians(self.yaw)
        return np.array(
            [
                [np.cos(yaw), 0.0, np.sin(yaw)],
                [0.0, 1.0, 0.0],
                [-np.sin(yaw), 0.0, np.cos(yaw)],
            ]
        )

    def _cal_pitch_rot(self):
        """pitchの回転を計算"""
        pitch = np.radians(-self.pitch)  # pitchは通常、負の方向に回転
        return np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, np.cos(pitch), -np.sin(pitch)],
                [0.0, np.sin(pitch), np.cos(pitch)],  # 符号を修正
            ]
        )

    def _cal_roll_rot(self):
        """rollの回転を計算"""
        roll = np.radians(self.roll)
        return np.array(
            [
                [np.cos(roll), np.sin(roll), 0.0],
                [-np.sin(roll), np.cos(roll), 0.0],
                [0.0, 0.0, 1.0],
            ]
        )

    def _cal_rotation_matrix(self):
        """回転行列を計算"""
        R_yaw = self._cal_yaw_rot()
        R_pitch = self._cal_pitch_rot()
        R_roll = self._cal_roll_rot()
        return R_roll @ R_pitch @ R_yaw  # 回転順序は重要です

    def _update_angle(self):
        """角度を調整"""
        self.yaw += self.yaw_v
        self.pitch += self.pitch_v
        self.roll += self.roll_v

        forward = np.array([0.0, 0.0, 1.0])
        R = self._cal_rotation_matrix()
        vec = R @ forward
        self.pos += vec
        R_roll = self._cal_roll_rot()
        self.direction = R_roll @ np.array(
            [
                self.yaw,
                self.pitch,
                self.roll,
            ]
        )

    def update(self):
        self._decrease_params()
        self._update_angle()

    def draw(self, camera: Camera):
        pass
