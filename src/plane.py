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

    def decrease_params(self):
        """減衰処理"""
        self.yaw_v *= 0.95
        self.pitch_v *= 0.95
        self.roll_v *= 0.95
        # self.roll *= 0.999
        # self.pitch *= 0.999

    def _cal_angle(self):
        """角度を計算"""

        yaw = np.radians(self.yaw)
        pitch = np.radians(-self.pitch)
        roll = np.radians(self.roll)

        R_pitch = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, np.cos(pitch), -np.sin(pitch)],
                [-np.sin(pitch), 0, np.cos(pitch)],
            ]
        )
        R_yaw = np.array(
            [
                [np.cos(yaw), 0.0, np.sin(yaw)],
                [0.0, 1.0, 0.0],
                [-np.sin(yaw), 0.0, np.cos(yaw)],
            ]
        )
        R_roll = np.array(
            [
                [np.cos(roll), np.sin(roll), 0.0],
                [-np.sin(roll), np.cos(roll), 0.0],
                [0.0, 0.0, 1.0],
            ]
        )
        return R_roll @ R_pitch @ R_yaw

    def update_angle(self):
        """角度を調整"""
        self.yaw += self.yaw_v
        self.pitch += self.pitch_v
        self.roll += self.roll_v

        forward = np.array([0.0, 0.0, 1.0])
        R = self._cal_angle()
        vec = R @ forward
        print(vec)
        self.pos += vec
        self.vec += vec
        roll = np.radians(self.roll)
        R_roll = np.array(
            [
                [np.cos(roll), np.sin(roll), 0.0],
                [-np.sin(roll), np.cos(roll), 0.0],
                [0.0, 0.0, 1.0],
            ]
        )
        self.direction = R_roll @ np.array(
            [
                self.yaw,
                self.pitch,
                self.roll,
            ]
        )

    def update(self):
        self.decrease_params()
        self.update_angle()

    def draw(self, camera: Camera):
        pass
