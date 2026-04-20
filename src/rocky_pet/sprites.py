from enum import Enum, auto
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap


_TILE = 48
_SHADOW_TOP = 41  # rows 0..40 = character, 42..44 = ground shadow bar, 45..47 = empty
SCALE = 4
SPRITE_SIZE = _TILE * SCALE


class AnimState(Enum):
    IDLE = auto()
    RUNNING = auto()


class Direction(Enum):
    NE = 0
    SE = 1
    SW = 2
    NW = 3


_ASSETS = Path(__file__).parent / "assets"

_SHEETS = {
    AnimState.IDLE: ("idle.png", 4),
    AnimState.RUNNING: ("run.png", 6),
}


class SpriteSheet:
    def __init__(self):
        self._frames: dict[tuple[AnimState, Direction], list[QPixmap]] = {}
        self._loaded = False

    def load(self) -> None:
        if self._loaded:
            return
        for state, (filename, frame_count) in _SHEETS.items():
            pix = QPixmap(str(_ASSETS / filename))
            if pix.isNull():
                raise RuntimeError(f"Failed to load sprite sheet: {filename}")
            for direction in Direction:
                row = direction.value
                frames = [
                    self._slice_and_scale(pix, col, row)
                    for col in range(frame_count)
                ]
                self._frames[(state, direction)] = frames
        self._loaded = True

    @staticmethod
    def _slice_and_scale(sheet: QPixmap, col: int, row: int) -> QPixmap:
        tile = QPixmap(_TILE, _TILE)
        tile.fill(Qt.GlobalColor.transparent)
        p = QPainter(tile)
        p.drawPixmap(
            0, 0, sheet,
            col * _TILE, row * _TILE, _TILE, _SHADOW_TOP,
        )
        p.end()
        return tile.scaled(
            SPRITE_SIZE, SPRITE_SIZE,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.FastTransformation,
        )

    def frame_count(self, state: AnimState) -> int:
        return _SHEETS[state][1]

    def get(self, state: AnimState, direction: Direction, frame_idx: int) -> QPixmap:
        frames = self._frames[(state, direction)]
        return frames[frame_idx % len(frames)]
