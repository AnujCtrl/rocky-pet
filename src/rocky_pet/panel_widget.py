from PyQt6.QtCore import QMimeData, Qt
from PyQt6.QtGui import QColor, QDrag, QFont, QMouseEvent, QPainter, QPainterPath, QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget


class DraggableItem(QLabel):
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        self.item_name = name
        self.setText(name)
        self.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(32)
        self.setMinimumWidth(70)
        self.setStyleSheet(
            "QLabel {"
            "  background-color: rgba(255, 240, 200, 220);"
            "  border: 2px solid #B4A078;"
            "  border-radius: 6px;"
            "  padding: 4px 10px;"
            "  color: #3C321E;"
            "}"
            "QLabel:hover {"
            "  background-color: rgba(255, 220, 150, 240);"
            "  border-color: #8B7355;"
            "}"
        )
        self.setCursor(Qt.CursorShape.OpenHandCursor)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(self.item_name)
            drag.setMimeData(mime)
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.GlobalColor.transparent)
            self.render(pixmap)
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.position().toPoint())
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            drag.exec(Qt.DropAction.CopyAction)
            self.setCursor(Qt.CursorShape.OpenHandCursor)


class PanelWidget(QWidget):
    PANEL_WIDTH = 300

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(16, 16, 16, 16)
        self._layout.setSpacing(8)

        self._question_label = QLabel()
        self._question_label.setFont(QFont("Segoe UI", 11))
        self._question_label.setWordWrap(True)
        self._question_label.setStyleSheet("color: #3C321E;")
        self._layout.addWidget(self._question_label)

        self._items_layout = QHBoxLayout()
        self._items_layout.setSpacing(6)
        self._layout.addLayout(self._items_layout)

        self._hint_label = QLabel("Drag answer to Rocky!")
        self._hint_label.setFont(QFont("Segoe UI", 8))
        self._hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._hint_label.setStyleSheet("color: #8B7355;")
        self._layout.addWidget(self._hint_label)

        self.setFixedWidth(self.PANEL_WIDTH)
        self.hide()

    def _clear_items(self):
        while self._items_layout.count():
            child = self._items_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_question(self, text: str, choices: list[str]):
        self._question_label.setText(text)
        self._hint_label.setText("Drag answer to Rocky!")
        self._clear_items()
        for choice in choices:
            self._items_layout.addWidget(DraggableItem(choice))
        self.adjustSize()
        self.show()

    def show_gifts(self, gift_names: list[str]):
        self._question_label.setText("Give Rocky a gift!")
        self._hint_label.setText("Drag gift to Rocky!")
        self._clear_items()
        for name in gift_names:
            self._items_layout.addWidget(DraggableItem(name))
        self.adjustSize()
        self.show()

    def show_near(self, x: int, y: int):
        self.move(max(10, x - self.width() // 2), max(10, y + 40))

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 12, 12)
        p.fillPath(path, QColor(255, 250, 235, 220))
        p.setPen(QColor(180, 160, 120))
        p.drawPath(path)
        p.end()
