import io
import wave
from rocky_pet.audio import AudioEngine


def test_generate_chord_returns_bytes():
    engine = AudioEngine()
    data = engine.generate_chord_wav([440.0])
    assert isinstance(data, bytes)
    assert len(data) > 0


def test_generated_wav_is_valid():
    engine = AudioEngine()
    data = engine.generate_chord_wav([440.0])
    buf = io.BytesIO(data)
    with wave.open(buf, "rb") as wf:
        assert wf.getnchannels() == 1
        assert wf.getsampwidth() == 2
        assert wf.getframerate() == 44100
        assert wf.getnframes() > 0


def test_emotion_chords_exist():
    engine = AudioEngine()
    for emotion in ("happy", "sad", "curious", "excited"):
        assert emotion in engine.emotion_chords


def test_chord_frequencies_are_valid():
    engine = AudioEngine()
    for emotion, freqs in engine.emotion_chords.items():
        assert len(freqs) >= 2, f"{emotion} needs at least 2 frequencies"
        for f in freqs:
            assert 100 < f < 2000, f"{emotion} freq {f} out of range"


def test_different_emotions_sound_different():
    engine = AudioEngine()
    wavs = {}
    for emotion in ("happy", "sad", "curious", "excited"):
        wavs[emotion] = engine.generate_chord_wav(engine.emotion_chords[emotion])
    assert wavs["happy"] != wavs["sad"]
    assert wavs["curious"] != wavs["excited"]


def test_generate_with_custom_duration():
    engine = AudioEngine()
    data = engine.generate_chord_wav([440.0, 554.37, 659.25], duration=0.3)
    buf = io.BytesIO(data)
    with wave.open(buf, "rb") as wf:
        expected_frames = int(44100 * 0.3)
        assert abs(wf.getnframes() - expected_frames) < 10
