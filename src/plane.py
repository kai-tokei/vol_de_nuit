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
        self.pos = np.array([0, -10, 0])
        self.direction = np.array([0, 0, 0])
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
        self.roll *= 0.999
        self.pitch *= 0.999

    def cal_angle(self):
        """角度を計算"""
        R_pitch = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, np.cos(self.pitch), -np.sin(self.pitch)],
                [-np.sin(self.pitch), 0, np.cos(self.pitch)],
            ]
        )
        R_yaw = np.array(
            [
                [np.cos(self.yaw), 0.0, np.sin(self.yaw)],
                [0.0, 1.0, 0.0],
                [-np.sin(self.yaw), 0.0, np.cos(self.yaw)],
            ]
        )
        R_roll = np.array(
            [
                [np.cos(self.roll), -np.sin(self.roll), 0.0],
                [np.sin(self.roll), np.cos(self.roll), 0.0],
                [0.0, 0.0, 1.0],
            ]
        )

    def update_angle(self):
        """角度を調整"""
        self.yaw += self.yaw_v
        self.pitch += self.pitch_v
        self.roll += self.roll_v

    def update(self):
        self.decrease_params()
        self.update_angle()

    def draw(self, camera: Camera):
        pass
