import math
from enum import Enum, auto

from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtGui import QColor, QPainter, QPen, QPixmap


class AnimState(Enum):
    IDLE = auto()
    WALK_RIGHT = auto()
    WALK_LEFT = auto()
    HAPPY = auto()
    SAD = auto()
    CURIOUS = auto()
    EXCITED = auto()


BODY_COLOR = QColor(139, 115, 85)
BODY_HIGHLIGHT = QColor(160, 137, 108)
BODY_SHADOW = QColor(107, 91, 69)
ARM_COLOR = QColor(120, 100, 75)
EYE_COLOR = QColor(180, 220, 255)

SPRITE_SIZE = 64


class SpriteRenderer:
    def __init__(self):
        self._cache: dict[tuple[AnimState, int], QPixmap] = {}
        self._frame_counts = {
            AnimState.IDLE: 2,
            AnimState.WALK_RIGHT: 4,
            AnimState.WALK_LEFT: 4,
            AnimState.HAPPY: 4,
            AnimState.SAD: 2,
            AnimState.CURIOUS: 2,
            AnimState.EXCITED: 4,
        }

    def frame_count(self, state: AnimState) -> int:
        return self._frame_counts.get(state, 2)

    def get_frame(self, state: AnimState, frame: int) -> QPixmap:
        key = (state, frame % self.frame_count(state))
        if key not in self._cache:
            self._cache[key] = self._render_frame(key[0], key[1])
        return self._cache[key]

    def _render_frame(self, state: AnimState, frame: int) -> QPixmap:
        pixmap = QPixmap(SPRITE_SIZE, SPRITE_SIZE)
        pixmap.fill(Qt.GlobalColor.transparent)
        p = QPainter(pixmap)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        cx, cy = SPRITE_SIZE // 2, SPRITE_SIZE // 2 + 4
        body_w, body_h = 22, 18

        bounce = 0
        if state in (AnimState.HAPPY, AnimState.EXCITED):
            bounce = int(3 * math.sin(frame * math.pi / 2))
        elif state in (AnimState.WALK_RIGHT, AnimState.WALK_LEFT):
            bounce = int(1.5 * math.sin(frame * math.pi / 2))

        by = cy - bounce

        # Draw 5 arms
        arm_angles_base = [-120, -60, 0, 60, 120]
        for i, angle_deg in enumerate(arm_angles_base):
            angle = math.radians(angle_deg - 90)
            arm_len = 16
            wave = 0

            if state == AnimState.HAPPY:
                wave = 5 * math.sin(frame * math.pi / 2 + i)
            elif state == AnimState.SAD:
                wave = -4
                angle += math.radians(20)
            elif state == AnimState.EXCITED:
                wave = 7 * math.sin(frame * math.pi + i * 1.2)
            elif state == AnimState.CURIOUS and i == 2:
                wave = 8
                arm_len = 20
            elif state in (AnimState.WALK_RIGHT, AnimState.WALK_LEFT):
                wave = 3 * math.sin(frame * math.pi / 2 + i * 0.8)

            if state == AnimState.WALK_LEFT:
                angle = math.pi - angle  # mirror

            ax = cx + int((body_w * 0.6) * math.cos(angle))
            ay = by + int((body_h * 0.6) * math.sin(angle))
            ex = ax + int(arm_len * math.cos(angle + math.radians(wave)))
            ey = ay + int(arm_len * math.sin(angle + math.radians(wave)))

            p.setPen(QPen(ARM_COLOR, 2))
            p.drawLine(ax, ay, ex, ey)

            for finger_angle in [-25, 25]:
                fa = angle + math.radians(wave + finger_angle)
                fx = ex + int(4 * math.cos(fa))
                fy = ey + int(4 * math.sin(fa))
                p.drawLine(ex, ey, fx, fy)

        # Body oval
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(BODY_COLOR)
        body_rect = QRect(cx - body_w // 2, by - body_h // 2, body_w, body_h)
        p.drawEllipse(body_rect)

        # Rocky texture bumps
        p.setBrush(BODY_HIGHLIGHT)
        for bx, by_off in [(cx - 5, by - 4), (cx + 3, by - 6), (cx + 6, by + 1)]:
            p.drawEllipse(QPoint(bx, by_off), 2, 2)
        p.setBrush(BODY_SHADOW)
        for bx, by_off in [(cx - 3, by + 3), (cx + 2, by + 5)]:
            p.drawEllipse(QPoint(bx, by_off), 2, 1)

        # "Eye" glow
        glow_alpha = 140
        if state in (AnimState.HAPPY, AnimState.EXCITED):
            glow_alpha = 200
        elif state == AnimState.SAD:
            glow_alpha = 80
        glow = QColor(EYE_COLOR)
        glow.setAlpha(glow_alpha)
        p.setBrush(glow)
        p.drawEllipse(QPoint(cx, by - 2), 3, 3)

        p.end()
        return pixmap
