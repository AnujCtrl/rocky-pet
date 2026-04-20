from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPainter, QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import QWidget

from rocky_pet.sprites import AnimState, Direction, SpriteSheet, SPRITE_SIZE


TICK_HZ = 30


class RockyWidget(QWidget):
    clicked = pyqtSignal()
    item_dropped = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._sheet = SpriteSheet()
        self._sheet.load()
        self._state = AnimState.IDLE
        self._direction = Direction.SE
        self._frame = 0
        self._ticks_per_frame = max(1, round(TICK_HZ / 6))
        self._tick_accum = 0

        self.setFixedSize(SPRITE_SIZE, SPRITE_SIZE)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAcceptDrops(True)

    def set_anim(self, state: AnimState, direction: Direction, fps: int):
        if state == self._state and direction == self._direction:
            new_tpf = max(1, round(TICK_HZ / fps))
            self._ticks_per_frame = new_tpf
            return
        self._state = state
        self._direction = direction
        self._frame = 0
        self._tick_accum = 0
        self._ticks_per_frame = max(1, round(TICK_HZ / fps))
        self.update()

    def advance_frame(self):
        self._tick_accum += 1
        if self._tick_accum >= self._ticks_per_frame:
            self._tick_accum = 0
            self._frame += 1
            self.update()

    def move_to(self, x: int, y: int):
        self.move(x - SPRITE_SIZE // 2, y - SPRITE_SIZE // 2)

    def paintEvent(self, event):
        pixmap = self._sheet.get(self._state, self._direction, self._frame)
        painter = QPainter(self)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        self.item_dropped.emit(event.mimeData().text())
        event.acceptProposedAction()
