import pyxel
import numpy as np
from src.camera import Camera
from src.utils import cal_pitch_rot, cal_roll_rot, cal_yaw_rot


class Plane:
    ROLL_SPEED = 0.2
    PITCH_SPEED = 0.2
    YAW_SPEED = 0.2
    GROUND_Y = -3  # 地面のy座標
    GROUND_GAP = 8  # 地面効果を受ける範囲

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
        self.isGroundEffected = False  # 地面効果を受け取っているか

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
        if self.isGroundEffected:
            self.roll *= 0.95
            self.pitch *= 0.95

    def _cal_rotation_matrix(self):
        """回転行列を計算"""
        R_yaw = cal_yaw_rot(self.yaw)
        R_pitch = cal_pitch_rot(self.pitch)
        R_roll = cal_roll_rot(self.roll)
        return R_roll @ R_pitch @ R_yaw

    def _update_angle(self):
        """角度を調整"""
        self.yaw += self.yaw_v
        self.pitch += self.pitch_v
        self.roll += self.roll_v

        # 世界座標系での方向を計算
        R_roll = cal_roll_rot(self.roll)
        self.direction = R_roll @ np.array(
            [
                self.yaw,
                self.pitch,
                self.roll,
            ]
        )

    def _update_pos(self):
        """位置座標を計算"""
        forward = np.array([0.0, 0.0, 1.0])
        R = self._cal_rotation_matrix()
        vec = R @ forward
        self.pos += vec

    def update(self):
        self._decrease_params()
        self._update_angle()
        self._update_pos()

    def draw(self, camera: Camera):
        pass
