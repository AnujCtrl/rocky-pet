import random
from enum import Enum, auto
from PyQt6.QtCore import QObject, pyqtSignal


class State(Enum):
    INTRO = auto()
    ROAMING = auto()
    IDLE = auto()
    ASKING = auto()
    REACTING = auto()
    QUOTING = auto()
    HIDDEN = auto()


class PetEngine(QObject):
    state_changed = pyqtSignal(object)
    position_changed = pyqtSignal(int, int)

    def __init__(self, screen_width=1920, screen_height=1080, parent=None):
        super().__init__(parent)
        self._state = State.ROAMING
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-1, 1, -2, 2])
        self._idle_counter = 0
        self._idle_threshold = random.randint(100, 300)
        self._idle_duration = 0
        self._idle_max = 60
        self.anim_frame = 0
        self._anim_tick = 0

    @property
    def state(self) -> State:
        return self._state

    def set_state(self, new_state: State):
        if new_state != self._state:
            self._state = new_state
            self.state_changed.emit(new_state)
            if new_state == State.ROAMING:
                self._idle_counter = 0
                self._idle_threshold = random.randint(100, 300)
            elif new_state == State.IDLE:
                self._idle_duration = 0
                self._idle_max = random.randint(40, 80)

    def tick(self):
        self._anim_tick += 1
        if self._anim_tick % 8 == 0:
            self.anim_frame += 1

        if self._state == State.ROAMING:
            self._move()
            self._idle_counter += 1
            if self._idle_counter >= self._idle_threshold:
                self.set_state(State.IDLE)
        elif self._state == State.IDLE:
            self._idle_duration += 1
            if self._idle_duration >= self._idle_max:
                self.set_state(State.ROAMING)

    def _move(self):
        margin = 64
        self.x += self.vx
        self.y += self.vy

        if self.x <= margin:
            self.x = margin
            self.vx = abs(self.vx)
        elif self.x >= self.screen_width - margin:
            self.x = self.screen_width - margin
            self.vx = -abs(self.vx)

        if self.y <= margin:
            self.y = margin
            self.vy = abs(self.vy)
        elif self.y >= self.screen_height - margin:
            self.y = self.screen_height - margin
            self.vy = -abs(self.vy)

        if random.random() < 0.01:
            self.vx = random.choice([-2, -1, 1, 2])
            self.vy = random.choice([-1, 1, -2, 2])

        self.position_changed.emit(self.x, self.y)
