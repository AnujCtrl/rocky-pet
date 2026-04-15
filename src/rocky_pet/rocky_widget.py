from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPainter, QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import QWidget

from rocky_pet.sprites import AnimState, SpriteRenderer, SPRITE_SIZE


class RockyWidget(QWidget):
    clicked = pyqtSignal()
    item_dropped = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._renderer = SpriteRenderer()
        self._anim_state = AnimState.IDLE
        self._frame = 0

        self.setFixedSize(SPRITE_SIZE, SPRITE_SIZE)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAcceptDrops(True)

    def set_anim_state(self, state: AnimState):
        if state != self._anim_state:
            self._anim_state = state
            self._frame = 0
            self.update()

    def advance_frame(self):
        self._frame += 1
        self.update()

    def move_to(self, x: int, y: int):
        self.move(x - SPRITE_SIZE // 2, y - SPRITE_SIZE // 2)

    def paintEvent(self, event):
        pixmap = self._renderer.get_frame(self._anim_state, self._frame)
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
