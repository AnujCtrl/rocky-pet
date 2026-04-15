from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QFontMetrics, QPainter, QPainterPath
from PyQt6.QtWidgets import QWidget


class BubbleWidget(QWidget):
    PADDING = 12
    MAX_WIDTH = 280
    TAIL_SIZE = 10

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text = ""
        self._auto_hide_timer = QTimer(self)
        self._auto_hide_timer.setSingleShot(True)
        self._auto_hide_timer.timeout.connect(self.hide)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.hide()

    def show_text(self, text: str, duration_ms: int = 4000):
        self._text = text
        self._resize_to_fit()
        self.show()
        self.update()
        if duration_ms > 0:
            self._auto_hide_timer.start(duration_ms)

    def show_near(self, x: int, y: int, text: str, duration_ms: int = 4000):
        self.show_text(text, duration_ms)
        bx = max(10, x - self.width() // 2)
        by = max(10, y - self.height() - 10)
        self.move(bx, by)

    def _resize_to_fit(self):
        font = QFont("Segoe UI", 11)
        fm = QFontMetrics(font)
        text_rect = fm.boundingRect(
            0, 0, self.MAX_WIDTH - 2 * self.PADDING, 1000,
            Qt.TextFlag.TextWordWrap, self._text,
        )
        w = text_rect.width() + 2 * self.PADDING + 4
        h = text_rect.height() + 2 * self.PADDING + self.TAIL_SIZE + 4
        self.setFixedSize(max(w, 60), max(h, 40))

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        bubble_h = h - self.TAIL_SIZE

        # Bubble background
        path = QPainterPath()
        path.addRoundedRect(0, 0, w, bubble_h, 10, 10)
        bg = QColor(255, 255, 240, 230)
        p.fillPath(path, bg)
        p.setPen(QColor(180, 160, 120))
        p.drawPath(path)

        # Tail
        tail_x = w // 2
        tail = QPainterPath()
        tail.moveTo(tail_x - 6, bubble_h)
        tail.lineTo(tail_x, h)
        tail.lineTo(tail_x + 6, bubble_h)
        tail.closeSubpath()
        p.fillPath(tail, bg)
        p.drawPath(tail)

        # Text
        p.setPen(QColor(60, 50, 30))
        p.setFont(QFont("Segoe UI", 11))
        p.drawText(
            self.PADDING, self.PADDING,
            w - 2 * self.PADDING, bubble_h - 2 * self.PADDING,
            Qt.TextFlag.TextWordWrap | Qt.AlignmentFlag.AlignLeft,
            self._text,
        )
        p.end()
