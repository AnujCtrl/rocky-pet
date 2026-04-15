from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction, QColor, QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QHBoxLayout, QKeySequenceEdit, QLabel,
    QMenu, QPushButton, QSlider, QSystemTrayIcon, QVBoxLayout, QWidget,
)


def _create_rocky_icon() -> QIcon:
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.GlobalColor.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor(139, 115, 85))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(6, 6, 20, 20)
    p.setBrush(QColor(180, 220, 255))
    p.drawEllipse(13, 12, 6, 6)
    p.end()
    return QIcon(pixmap)


class SettingsDialog(QDialog):
    hotkey_changed = pyqtSignal(str)
    volume_changed = pyqtSignal(float)

    def __init__(self, current_hotkey="Ctrl+Shift+R", current_volume=0.7, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rocky Settings")
        self.setFixedSize(320, 180)

        layout = QFormLayout(self)

        self._hotkey_edit = QKeySequenceEdit(self)
        self._hotkey_edit.setKeySequence(current_hotkey)
        layout.addRow("Toggle Hotkey:", self._hotkey_edit)

        vol_layout = QHBoxLayout()
        self._volume_slider = QSlider(Qt.Orientation.Horizontal)
        self._volume_slider.setRange(0, 100)
        self._volume_slider.setValue(int(current_volume * 100))
        self._vol_label = QLabel(f"{int(current_volume * 100)}%")
        self._volume_slider.valueChanged.connect(
            lambda v: self._vol_label.setText(f"{v}%")
        )
        vol_layout.addWidget(self._volume_slider)
        vol_layout.addWidget(self._vol_label)
        layout.addRow("Volume:", vol_layout)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self._save)
        layout.addRow(save_btn)

    def _save(self):
        seq = self._hotkey_edit.keySequence().toString()
        if seq:
            self.hotkey_changed.emit(seq)
        self.volume_changed.emit(self._volume_slider.value() / 100.0)
        self.accept()


class TrayManager(QSystemTrayIcon):
    toggle_requested = pyqtSignal()
    quit_requested = pyqtSignal()
    settings_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(_create_rocky_icon(), parent)
        self.setToolTip("Rocky Desktop Pet")

        menu = QMenu()
        show_action = QAction("Show/Hide Rocky", menu)
        show_action.triggered.connect(self.toggle_requested.emit)
        menu.addAction(show_action)

        settings_action = QAction("Settings...", menu)
        settings_action.triggered.connect(self.settings_requested.emit)
        menu.addAction(settings_action)

        menu.addSeparator()

        quit_action = QAction("Quit", menu)
        quit_action.triggered.connect(self.quit_requested.emit)
        menu.addAction(quit_action)

        self.setContextMenu(menu)
        self.activated.connect(self._on_activated)

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.toggle_requested.emit()
