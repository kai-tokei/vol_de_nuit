import numpy as np
import pyxel


class Camera:
    def __init__(
        self,
        pos: np.array,
        h_angle: float,
        v_angle: float,
        z_angle: float,
        screen_d: float,
        screen_w: int,
        screen_h: int,
    ):
        self.camera_pos = np.array(pos, dtype=float)
        self.camera_h_angle: float = h_angle  # 水平角度
        self.camera_v_angle: float = v_angle  # 垂直角度
        self.camera_z_angle: float = z_angle  # z角度
        self.screen_d: int = screen_d
        self.screen_w: int = screen_w
        self.screen_h: int = screen_h
        self.z_prime_handler: int = 4
        self.draw_limit: int = 850
        self.rotate(0, 0, 0)

    def cal_pos_on_screen(self, pos: np.array) -> tuple[int, int, int] | None:
        """
        三次元の世界座標をカメラ視点のスクリーン座標に変換する。
        """
        # カメラ座標系への変換
        relative_pos = pos - self.camera_pos
        x, y, z = relative_pos
        d = np.linalg.norm(relative_pos)  # 距離計算

        # 描画距離制限をかける
        if d > self.draw_limit:
            return None

        # 回転行列を適用
        yaw_matrix = np.array(
            [[self._cos_h, 0, -self._sin_h], [0, 1, 0], [self._sin_h, 0, self._cos_h]]
        )

        pitch_matrix = np.array(
            [[1, 0, 0], [0, self._cos_v, -self._sin_v], [0, self._sin_v, self._cos_v]]
        )

        # Yaw -> Pitch の順に適用
        rotated_pos = pitch_matrix @ (yaw_matrix @ relative_pos)
        x_prime, y_prime, z_prime = rotated_pos

        z_prime /= self.z_prime_handler

        # 透視投影
        if z_prime <= 0.0001:
            return None  # カメラの後ろにある場合は描画しない

        screen_x = (x_prime / z_prime) * self.screen_d + self.screen_w / 2
        screen_y = (y_prime / z_prime) * self.screen_d + self.screen_h / 2

        # 2D回転（Roll）
        roll_matrix = np.array(
            [[self._cos_z, -self._sin_z], [self._sin_z, self._cos_z]]
        )

        screen_coords = np.array(
            [screen_x - self.screen_w / 2, screen_y - self.screen_h / 2]
        )
        rotated_screen_coords = roll_matrix @ screen_coords

        screen_x, screen_y = rotated_screen_coords + np.array(
            [self.screen_w / 2, self.screen_h / 2]
        )

        return int(screen_x), int(screen_y), d

    def move(self, dx: float, dy: float, dz: float):
        """カメラの位置を変更する"""
        self.camera_pos += np.array([dx, dy, dz])

    def set_pos(self, x: float, y: float, z: float):
        """カメラの位置を設定する"""
        self.camera_pos = np.array([x, y, z])

    def set_angle(self, h: float, v: float, z: float):
        """カメラの角度を設定する"""
        self.camera_h_angle = h
        self.camera_v_angle = v
        self.camera_z_angle = z
        self.cal_rotation()

    def rotate(self, dh: float, dv: float, dz: float):
        """カメラの向きを変更する"""
        self.camera_h_angle += dh
        self.camera_v_angle += dv
        self.camera_z_angle += dz
        self.cal_rotation()

    def cal_rotation(self):
        # カメラの回転
        self._cos_h = np.cos(self.camera_h_angle)
        self._sin_h = np.sin(self.camera_h_angle)
        self._cos_v = np.cos(self.camera_v_angle)
        self._sin_v = np.sin(self.camera_v_angle)
        self._cos_z = np.cos(self.camera_z_angle)
        self._sin_z = np.sin(self.camera_z_angle)
