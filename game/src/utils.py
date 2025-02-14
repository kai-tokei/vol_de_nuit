import numpy as np


def cal_yaw_rot(_yaw):
    """yawの回転を計算"""
    yaw = np.radians(_yaw)
    return np.array(
        [
            [np.cos(yaw), 0.0, np.sin(yaw)],
            [0.0, 1.0, 0.0],
            [-np.sin(yaw), 0.0, np.cos(yaw)],
        ]
    )


def cal_pitch_rot(_pitch):
    """pitchの回転を計算"""
    pitch = np.radians(-_pitch)  # pitchは通常、負の方向に回転
    return np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, np.cos(pitch), -np.sin(pitch)],
            [0.0, np.sin(pitch), np.cos(pitch)],
        ]
    )


def cal_roll_rot(_roll):
    """rollの回転を計算"""
    roll = np.radians(_roll)
    return np.array(
        [
            [np.cos(roll), np.sin(roll), 0.0],
            [-np.sin(roll), np.cos(roll), 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
