class Frame:
    """アニメーションのフレーム情報"""

    def __init__(self, wait_time: int, order: tuple[int]):
        """
        wait_time: めくり待機時間(t/60 fps)
        order: コマidを入力(画像の左上が0)
        """
        self.size: int = len(order)
        self.wait_time: int = wait_time
        self.order: tuple[int] = order
