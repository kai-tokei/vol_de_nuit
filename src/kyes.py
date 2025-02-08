import pyxel


class InputDetector:
    UP = [
        pyxel.KEY_UP,
        pyxel.GAMEPAD1_BUTTON_DPAD_UP,
    ]

    DOWN = [
        pyxel.KEY_DOWN,
        pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,
    ]

    LEFT = [
        pyxel.KEY_LEFT,
        pyxel.GAMEPAD1_BUTTON_DPAD_LEFT,
    ]

    RIGHT = [
        pyxel.KEY_RIGHT,
        pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,
    ]

    A = [
        pyxel.KEY_A,
        pyxel.GAMEPAD1_BUTTON_A,
    ]

    B = [
        pyxel.KEY_X,
        pyxel.GAMEPAD1_BUTTON_B,
    ]

    X = [
        pyxel.KEY_Z,
        pyxel.GAMEPAD1_BUTTON_X,
    ]

    Y = [
        pyxel.KEY_S,
        pyxel.GAMEPAD1_BUTTON_Y,
    ]

    def btn(key: list[int]) -> bool:
        for k in key:
            if pyxel.btn(k):
                return True
        return False

    def btnp(key: list[int]) -> bool:
        for k in key:
            if pyxel.btnp(k):
                return True
        return False

    def btnr(key: list[int]) -> bool:
        for k in key:
            if pyxel.btnr(k):
                return True
        return False
