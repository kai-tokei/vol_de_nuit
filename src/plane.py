import pyxel
import numpy as np
from src.camera import Camera
from src.utils import cal_pitch_rot, cal_roll_rot, cal_yaw_rot


class Plane:
    A = 0.001
    SPEED_MAX = 0.6
    SPEED_MIN = 0.1
    SPEED_GROUND = 0.0
    ROLL_SPEED = 0.3
    PITCH_SPEED = 0.4
    YAW_SPEED = 0.2
    GROUND_Y = -3  # 地面のy座標
    GROUND_GAP = 20  # 地面効果を受ける範囲
    GRAVITY = np.array([0.0, 0.98, 0.0])

    def __init__(self):
        self.pos = np.array([500.0, -30.0, 0.0])
        self.vec = np.array([0.0, 0.0, 0.0])
        self.direction_angle = np.array([0.0, 0.0, 0.0])
        self.direction_vec = np.array([0.0, 0.0, 0.0])
        self.speed = 0.0
        self.yaw = 0
        self.yaw_v = 0
        self.pitch = 0
        self.pitch_v = 0
        self.roll = 0
        self.roll_v = 0
        self.v = 0
        self.levelness = 0
        self.isGroundEffected = False  # 地面効果を受け取っているか
        self.isCrashed = False  # 地面を突き抜けていないか

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

    def speed_up(self):
        """速度上昇"""
        self.speed = min(self.speed + self.A, self.SPEED_MAX)

    def speed_down(self):
        """速度減少"""
        if self.isGroundEffected:
            self.speed = max(self.speed - self.A, self.SPEED_GROUND)
        else:
            self.speed = max(self.speed - self.A, 0.3)

    def _cal_ground_effect(self):
        """地面効果"""
        theta = self._cal_angle_with_xz_plane(self.direction_vec)
        self.isGroundEffected = True
        self.isGroundEffected = 70 < theta < 110
        self.isGroundEffected &= self.pos[1] > self.GROUND_Y - self.GROUND_GAP

    def _decrease_params(self):
        """減衰処理"""
        self.yaw_v *= 0.95
        self.pitch_v *= 0.95
        self.roll_v *= 0.95
        if self.isGroundEffected:
            self.roll *= 0.95
            self.speed *= 0.999
            self.pitch += (-0.1 - self.pitch) * 0.04

    def _cal_rotation_matrix(self):
        """回転行列を計算"""
        R_yaw = cal_yaw_rot(self.yaw)
        R_pitch = cal_pitch_rot(self.pitch)
        R_roll = cal_roll_rot(self.roll)
        return R_roll @ R_pitch @ R_yaw

    def _cal_gravity(self):
        """重力を計算"""
        if self.isGroundEffected:
            return 0.0
        ratio = ((self.SPEED_MAX - self.speed) / self.SPEED_MAX) * self.GRAVITY
        return ratio * self.GRAVITY

    def _cal_angle_with_xz_plane(self, vec):
        """za平面とのなす角を計算する"""
        vx, vy, vz = vec
        norm = np.linalg.norm(vec)
        if vy == 0:
            return 90.0
        theta = np.arccos(vy / norm)
        return np.degrees(theta) % 180

    def _check_is_crashed(self):
        """クラッシュしていないか(地面を突き抜けていないか)確認"""
        self.isCrashed = self.pos[1] > 0

    def _chrashed(self):
        """地面にめり込んでいたらリセット"""
        if self.isCrashed:
            self.pos = np.array([500.0, -30.0, 0.0])
            self.vec = np.array([0.0, 0.0, 0.0])
            self.speed = 0.0
            self.yaw = 0.0
            self.pitch = 0.0
            self.roll = 0.0

    def _update_camera_angle(self):
        """カメラ角度を調整"""
        # 世界座標系での方向を計算
        forward = np.array([0.0, 0.0, 1.0])
        R = self._cal_rotation_matrix()
        self.direction_vec = R @ forward
        R_roll = cal_roll_rot(self.roll)
        self.direction_angle = R_roll @ np.array(
            [
                self.yaw,
                self.pitch,
                self.roll,
            ]
        )

    def _update_angle(self):
        """角度を調整"""
        self.yaw += self.yaw_v
        self.pitch += self.pitch_v
        self.roll += self.roll_v

    def _update_pos(self):
        """位置座標を計算"""
        forward = np.array([0.0, 0.0, 1.0])
        R = self._cal_rotation_matrix()
        self.vec *= 0.85
        self.vec += R @ forward
        self.vec *= self.speed
        self.vec += self._cal_gravity()
        self.pos += self.vec

    def update(self):
        self._decrease_params()
        self._update_angle()
        self._update_camera_angle()
        self._update_pos()
        self._cal_ground_effect()
        self._check_is_crashed()
        self._chrashed()
        self.levelness = self._cal_angle_with_xz_plane(self.direction_vec)

    def draw(self, camera: Camera):
        pass
