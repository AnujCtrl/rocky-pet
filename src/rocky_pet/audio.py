import io
import shutil
import tempfile
import wave
from pathlib import Path

import numpy as np


class AudioEngine:
    SAMPLE_RATE = 44100

    emotion_chords: dict[str, list[float]] = {
        "happy": [261.63, 329.63, 392.00, 523.25],   # C major + octave
        "sad": [220.00, 261.63, 311.13],              # A minor
        "curious": [293.66, 349.23, 440.00],          # D rising
        "excited": [329.63, 415.30, 493.88, 659.25],  # E major + high
    }

    def __init__(self):
        self._temp_dir = Path(tempfile.mkdtemp(prefix="rocky_audio_"))
        self._cached_files: dict[str, Path] = {}

    def generate_chord_wav(
        self, frequencies: list[float], duration: float = 0.4
    ) -> bytes:
        n_samples = int(self.SAMPLE_RATE * duration)
        t = np.linspace(0, duration, n_samples, dtype=np.float64)

        wave_data = np.zeros(n_samples, dtype=np.float64)
        for freq in frequencies:
            wave_data += np.sin(2 * np.pi * freq * t)

        wave_data = wave_data / max(len(frequencies), 1)

        # Fade-in/fade-out envelope to avoid clicks
        fade_samples = min(int(self.SAMPLE_RATE * 0.05), n_samples // 4)
        if fade_samples > 0:
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            wave_data[:fade_samples] *= fade_in
            wave_data[-fade_samples:] *= fade_out

        pcm = (wave_data * 32767).astype(np.int16)

        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.SAMPLE_RATE)
            wf.writeframes(pcm.tobytes())
        return buf.getvalue()

    def get_emotion_wav_path(self, emotion: str) -> Path:
        if emotion in self._cached_files:
            return self._cached_files[emotion]
        freqs = self.emotion_chords.get(emotion, self.emotion_chords["happy"])
        wav_data = self.generate_chord_wav(freqs)
        path = self._temp_dir / f"{emotion}.wav"
        path.write_bytes(wav_data)
        self._cached_files[emotion] = path
        return path

    def cleanup(self):
        if self._temp_dir.exists():
            shutil.rmtree(self._temp_dir, ignore_errors=True)
