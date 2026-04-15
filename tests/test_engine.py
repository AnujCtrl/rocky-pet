from unittest.mock import MagicMock
from rocky_pet.engine import PetEngine, State


def test_initial_state_is_roaming():
    engine = PetEngine(screen_width=1920, screen_height=1080)
    assert engine.state == State.ROAMING


def test_set_state_emits_signal(qapp):
    engine = PetEngine(screen_width=1920, screen_height=1080)
    callback = MagicMock()
    engine.state_changed.connect(callback)
    engine.set_state(State.IDLE)
    assert engine.state == State.IDLE
    callback.assert_called_once_with(State.IDLE)


def test_movement_updates_position():
    engine = PetEngine(screen_width=1920, screen_height=1080)
    old_x, old_y = engine.x, engine.y
    engine.tick()
    assert (engine.x, engine.y) != (old_x, old_y)


def test_bounce_off_right_edge():
    engine = PetEngine(screen_width=1920, screen_height=1080)
    engine.x = 1919
    engine.vx = 5
    engine.tick()
    assert engine.vx < 0


def test_bounce_off_left_edge():
    engine = PetEngine(screen_width=1920, screen_height=1080)
    engine.x = 1
    engine.vx = -5
    engine.tick()
    assert engine.vx > 0


def test_bounce_off_bottom_edge():
    engine = PetEngine(screen_width=1920, screen_height=1080)
    engine.y = 1079
    engine.vy = 5
    engine.tick()
    assert engine.vy < 0


def test_bounce_off_top_edge():
    engine = PetEngine(screen_width=1920, screen_height=1080)
    engine.y = 1
    engine.vy = -5
    engine.tick()
    assert engine.vy > 0


def test_no_movement_when_asking():
    engine = PetEngine(screen_width=1920, screen_height=1080)
    engine.set_state(State.ASKING)
    old_x, old_y = engine.x, engine.y
    engine.tick()
    assert engine.x == old_x and engine.y == old_y


def test_hidden_state():
    engine = PetEngine(screen_width=1920, screen_height=1080)
    engine.set_state(State.HIDDEN)
    assert engine.state == State.HIDDEN


def test_idle_transition():
    engine = PetEngine(screen_width=1920, screen_height=1080)
    engine.set_state(State.ROAMING)
    engine._idle_counter = engine._idle_threshold
    engine.tick()
    assert engine.state == State.IDLE
