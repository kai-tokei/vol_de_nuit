import pyxel
from .frame import Frame


class Animation:
    """スプライトシートを使ってアニメーションを再生"""

    def __init__(self, path: str, w: int, h: int):
        self.img = pyxel.Image.from_image(path)
        self.w: int = w
        self.h: int = h
        self.u_i: int  # 現在のフレームのu座標
        self.v_i: int  # 現在のフレームのv座標
        self.u_i_max: int  # 最大uフレームサイズ
        self.v_i_max: int  # 最大vフレームサイズ
        self.i_max: int
        self.frame_index: int
        self.frame_index_max: int
        self.frames: dict = {}
        self.piece_index: int = 0
        self.crtFrame: Frame = None
        self.time: int = 0
        self.updating: bool = False
        self.loop: bool = False
        self.isShow: bool = True
        self._cal_frame_index()

    def _cal_frame_index(self):
        """フレームの大きさなどを計算する"""
        self.u_i_max = self.img.width // self.w
        self.v_i_max = self.img.height // self.h
        self.i_max = self.u_i_max * self.v_i_max
        # print("u_i_max: ", self.u_i_max)
        # print("v_i_max: ", self.v_i_max)
        # print("i_max: ", self.i_max)
        # print("u, v: ", self._index2uv(2))

    def _index2uv(self, index: int) -> tuple[int, int]:
        """コマのindexをuv座標系に変換する"""
        if index == 0:
            return 0, 0
        u_i = index % self.u_i_max
        v_i = index // self.u_i_max
        return u_i, v_i

    def isLoop(self):
        """ループかどうか"""
        return self.loop

    def isFin(self):
        """アニメーションが終了したか"""
        return not self.updating

    def show(self):
        """アニメーションを表示"""
        self.isShow = True

    def hide(self):
        """アニメーションを非表示"""
        self.isShow = False

    def add(self, label: str, frame: Frame):
        """アニメーションを登録する"""
        self.frames[label] = frame

    def set(self, label: str) -> bool:
        """アニメーションを切り替える"""
        self.time = 0
        self.updating = False
        if label in self.frames:
            self.crtFrame = self.frames[label]
            self.frame_index = 0
            self.frame_index_max = self.crtFrame.size
            return True
        return False

    def stop(self):
        """アニメーションの再生を停止する"""
        self.updating = False

    def play(self, loop: bool = False):
        """アニメーションを再生する"""
        if not self.updating:
            self.frame_index = 0
            self.updating = True
            self.loop = loop

    def update(self):
        """アニメーションの更新"""
        if self.crtFrame == None:
            """アニメーションがセットされていないなら、再生しない"""
            return
        if not self.updating:
            """更新終了なら、再生しない"""
            return
        if self.time < self.crtFrame.wait_time:
            """めくり時間以内なら、timerをインクリメント"""
            self.time += 1
            return
        if not self.loop and self.frame_index == self.frame_index_max - 1:
            """ループ設定がないのなら、再生停止"""
            self.stop()
            return
        self.time = 0
        self.piece_index = self.crtFrame.order[self.frame_index]
        self.frame_index = (self.frame_index + 1) % self.frame_index_max

    def draw(
        self,
        x: int,
        y: int,
        other_img: pyxel.Image = None,
        colKey=None,
        rotate=None,
        scale=None,
    ):
        u, v = self._index2uv(self.piece_index)
        if other_img == None:
            pyxel.blt(
                x,
                y,
                self.img,
                u * self.w,
                v * self.h,
                self.w,
                self.h,
                colkey=colKey,
                rotate=rotate,
                scale=scale,
            )
        else:
            other_img.blt(
                x,
                y,
                self.img,
                u * self.w,
                v * self.h,
                self.w,
                self.h,
                colkey=colKey,
                rotate=rotate,
                scale=scale,
            )
