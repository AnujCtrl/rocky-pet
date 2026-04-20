import random

from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QApplication

from rocky_pet.audio import AudioEngine
from rocky_pet.bubble_widget import BubbleWidget
from rocky_pet.content import ContentManager, Question
from rocky_pet.engine import PetEngine, State
from rocky_pet.panel_widget import PanelWidget
from rocky_pet.rocky_widget import RockyWidget
from rocky_pet.settings import SettingsManager
from rocky_pet.sprites import AnimState, Direction
from rocky_pet.tray import SettingsDialog, TrayManager


RUN_FPS = 10
IDLE_FPS = 6

EMOTION_FPS = {
    "happy": 10,
    "excited": 12,
    "curious": 6,
    "sad": 3,
}


class RockyApp:
    def __init__(self):
        self.settings = SettingsManager()
        self.content = ContentManager()
        self.audio = AudioEngine()

        screen = QGuiApplication.primaryScreen()
        geom = screen.availableGeometry()
        self.engine = PetEngine(screen_width=geom.width(), screen_height=geom.height())

        self.rocky = RockyWidget()
        self.bubble = BubbleWidget()
        self.panel = PanelWidget()
        self.tray = TrayManager()

        self._current_direction = Direction.SE
        self._current_question: Question | None = None
        self._sound_effect = None
        self._setup_timers()
        self._connect_signals()

    def _setup_timers(self):
        self._tick_timer = QTimer()
        self._tick_timer.setInterval(33)  # ~30fps
        self._tick_timer.timeout.connect(self._on_tick)

        self._interaction_timer = QTimer()
        self._interaction_timer.setInterval(self.settings.interaction_interval * 1000)
        self._interaction_timer.timeout.connect(self._on_interaction_timer)

    def _connect_signals(self):
        self.engine.state_changed.connect(self._on_state_changed)
        self.engine.position_changed.connect(self._on_position_changed)
        self.rocky.clicked.connect(self._on_rocky_clicked)
        self.rocky.item_dropped.connect(self._on_item_dropped)
        self.tray.toggle_requested.connect(self._toggle_visibility)
        self.tray.quit_requested.connect(self._quit)
        self.tray.settings_requested.connect(self._show_settings)

    def start(self):
        self.tray.show()
        self.rocky.show()
        if self.settings.first_run:
            self._start_intro()
        else:
            self._current_direction = self._direction_from_velocity(
                self.engine.vx, self.engine.vy
            )
            self.rocky.set_anim(AnimState.RUNNING, self._current_direction, RUN_FPS)
            self.engine.set_state(State.ROAMING)
            self._tick_timer.start()
            self._interaction_timer.start()

    def _start_intro(self):
        self.engine.set_state(State.INTRO)
        self.rocky.set_anim(AnimState.IDLE, self._current_direction, EMOTION_FPS["happy"])
        self.rocky.move_to(self.engine.x, self.engine.y)
        self.bubble.show_near(
            self.engine.x, self.engine.y - 40,
            "Hello! I am Rocky! I am friend!\nYou help me, I help you!\nGood good good!",
            duration_ms=5000,
        )
        self._play_emotion_sound("excited")
        QTimer.singleShot(5500, self._end_intro)

    def _end_intro(self):
        self.settings.mark_first_run_complete()
        self.engine.set_state(State.ROAMING)
        self._tick_timer.start()
        self._interaction_timer.start()

    def _on_tick(self):
        self.engine.tick()
        if self.engine.state == State.ROAMING:
            new_dir = self._direction_from_velocity(self.engine.vx, self.engine.vy)
            if new_dir != self._current_direction:
                self._current_direction = new_dir
                self.rocky.set_anim(AnimState.RUNNING, new_dir, RUN_FPS)
        self.rocky.advance_frame()
        self.rocky.move_to(self.engine.x, self.engine.y)

    def _direction_from_velocity(self, vx: int, vy: int) -> Direction:
        if vx >= 0 and vy < 0:
            return Direction.NE
        if vx >= 0 and vy > 0:
            return Direction.SE
        if vx < 0 and vy > 0:
            return Direction.SW
        return Direction.NW

    def _on_state_changed(self, state: State):
        if state == State.ROAMING:
            self._current_direction = self._direction_from_velocity(
                self.engine.vx, self.engine.vy
            )
            self.rocky.set_anim(AnimState.RUNNING, self._current_direction, RUN_FPS)
        elif state in (State.IDLE, State.ASKING):
            self.rocky.set_anim(AnimState.IDLE, self._current_direction, IDLE_FPS)
        elif state == State.INTRO:
            self.rocky.set_anim(AnimState.IDLE, self._current_direction, EMOTION_FPS["happy"])
        if state not in (State.ASKING, State.REACTING):
            self.panel.hide()

    def _on_position_changed(self, x: int, y: int):
        self.rocky.move_to(x, y)
        if self.panel.isVisible():
            self.panel.show_near(x, y)

    def _on_interaction_timer(self):
        if self.engine.state not in (State.ROAMING, State.IDLE):
            return
        if random.random() < 0.6:
            self._ask_question()
        else:
            self._show_quote()

    def _on_rocky_clicked(self):
        if self.engine.state in (State.ROAMING, State.IDLE):
            if random.random() < 0.5:
                self._ask_question()
            else:
                self._show_gift_panel()
        elif self.engine.state == State.ASKING:
            self.panel.hide()
            self.bubble.hide()
            self.engine.set_state(State.ROAMING)

    def _ask_question(self):
        self._current_question = self.content.get_random_question()
        self.engine.set_state(State.ASKING)
        self._play_emotion_sound("curious")
        self.bubble.show_near(
            self.engine.x, self.engine.y - 40,
            self._current_question.text, duration_ms=0,
        )
        self.panel.show_question(
            "Drag your answer to Rocky!",
            self._current_question.choices,
        )
        self.panel.show_near(self.engine.x, self.engine.y)
        QTimer.singleShot(30000, self._dismiss_if_asking)

    def _show_gift_panel(self):
        self.engine.set_state(State.ASKING)
        gift_names = [g.name for g in self.content.gift_items]
        random.shuffle(gift_names)
        self.panel.show_gifts(gift_names[:4])
        self.panel.show_near(self.engine.x, self.engine.y)
        self.bubble.show_near(
            self.engine.x, self.engine.y - 40,
            "You have gift for Rocky?!", duration_ms=0,
        )
        self._current_question = None
        self._play_emotion_sound("curious")
        QTimer.singleShot(30000, self._dismiss_if_asking)

    def _show_quote(self):
        quote = self.content.get_random_quote()
        self.engine.set_state(State.QUOTING)
        fps = EMOTION_FPS.get(quote.emotion, IDLE_FPS)
        self.rocky.set_anim(AnimState.IDLE, self._current_direction, fps)
        self._play_emotion_sound(quote.emotion)
        self.bubble.show_near(
            self.engine.x, self.engine.y - 40, quote.text, duration_ms=5000,
        )
        QTimer.singleShot(5500, lambda: self.engine.set_state(State.ROAMING))

    def _on_item_dropped(self, item_name: str):
        self.panel.hide()
        self.bubble.hide()

        gift = next((g for g in self.content.gift_items if g.name == item_name), None)
        if gift:
            self._react(gift.reaction_emotion, gift.reaction_text)
            return

        if self._current_question:
            q = self._current_question
            self._current_question = None
            if q.correct_index == -1:
                self._react("happy", random.choice([
                    "Good good good! Rocky like that answer!",
                    "Interesting! Rocky learn new thing!",
                    "Amaze! You are so interesting!",
                ]))
            elif item_name == q.choices[q.correct_index]:
                self._react("excited", random.choice([
                    "YES! Correct! You so smart!",
                    "Good good good! You know this!",
                    "AMAZE! Perfect answer!",
                ]))
            else:
                correct = q.choices[q.correct_index]
                self._react("sad",
                    f"Hmm, not quite! Answer is {correct}. But is okay! Now you know!")

    def _react(self, emotion: str, text: str):
        self.engine.set_state(State.REACTING)
        fps = EMOTION_FPS.get(emotion, IDLE_FPS)
        self.rocky.set_anim(AnimState.IDLE, self._current_direction, fps)
        self._play_emotion_sound(emotion)
        self.bubble.show_near(
            self.engine.x, self.engine.y - 40, text, duration_ms=4000,
        )
        QTimer.singleShot(4500, lambda: self.engine.set_state(State.ROAMING))

    def _dismiss_if_asking(self):
        if self.engine.state == State.ASKING:
            self.panel.hide()
            self.bubble.hide()
            self.engine.set_state(State.ROAMING)

    def _play_emotion_sound(self, emotion: str):
        try:
            from PyQt6.QtMultimedia import QSoundEffect
            path = self.audio.get_emotion_wav_path(emotion)
            if self._sound_effect is None:
                self._sound_effect = QSoundEffect()
            self._sound_effect.setSource(QUrl.fromLocalFile(str(path)))
            self._sound_effect.setVolume(self.settings.volume)
            self._sound_effect.play()
        except ImportError:
            pass

    def _toggle_visibility(self):
        if self.engine.state == State.HIDDEN:
            self.engine.set_state(State.ROAMING)
            self.rocky.show()
        else:
            self.engine.set_state(State.HIDDEN)
            self.rocky.hide()
            self.bubble.hide()
            self.panel.hide()

    def _show_settings(self):
        dialog = SettingsDialog(
            current_hotkey=self.settings.hotkey,
            current_volume=self.settings.volume,
        )
        dialog.hotkey_changed.connect(self._update_hotkey)
        dialog.volume_changed.connect(self._update_volume)
        dialog.exec()

    def _update_hotkey(self, hotkey: str):
        self.settings.hotkey = hotkey
        self.settings.save()

    def _update_volume(self, volume: float):
        self.settings.volume = volume
        self.settings.save()

    def _quit(self):
        self.audio.cleanup()
        QApplication.quit()
