"""Create looping music from the WAV samples in the sounds folder.
No extra packages. Works with the existing sound_effects.py.
"""
from pathlib import Path
from array import array
import hashlib
import sys
import wave


def render_score(bars, bpm, sound_folder):
    """Mix a 16-step-per-bar score; allow samples to sustain over bar lines."""
    if not isinstance(bpm, (int, float)) or not 60 <= bpm <= 960:
        raise ValueError("BPM must be between 60 and 960")
    if not bars:
        raise ValueError("Add at least one bar to breakbeat_score")

    sound_folder = Path(sound_folder)
    samples = {}
    sample_rate = None

    for bar in bars:
        for name, pattern in bar.items():
            steps = pattern.replace(" ", "").replace("|", "")
            if len(steps) != 16 or any(c not in "Xx-." for c in steps):
                raise ValueError(name + ": write exactly 16 X or - steps")
            if not name.replace("_", "").isalnum():
                raise ValueError("Invalid sample name: " + name)
            if name in samples:
                continue
            path = sound_folder / (name + ".wav")
            if not path.is_file():
                raise FileNotFoundError("Missing WAV sample: " + str(path))
            with wave.open(str(path), "rb") as wav:
                if wav.getnchannels() != 1 or wav.getsampwidth() != 2:
                    raise ValueError(name + " must be a mono 16-bit WAV")
                rate = wav.getframerate()
                if sample_rate is None:
                    sample_rate = rate
                if rate != sample_rate:
                    raise ValueError("All samples must have the same sample rate")
                values = array("h")
                values.frombytes(wav.readframes(wav.getnframes()))
                if sys.byteorder != "little":
                    values.byteswap()
                samples[name] = values

    step_frames = sample_rate * 60 / (bpm * 4)
    loop_frames = round(len(bars) * 16 * step_frames)
    mix = [0] * loop_frames

    for bar_number, bar in enumerate(bars):
        for name, pattern in bar.items():
            steps = pattern.replace(" ", "").replace("|", "")
            for step_number, mark in enumerate(steps):
                if mark not in "Xx":
                    continue
                start = round((bar_number * 16 + step_number) * step_frames)

                # Allow samples to continue across bar boundaries.
                for offset, sample in enumerate(samples[name]):
                    mix[(start + offset) % loop_frames] += sample

    peak = max((abs(value) for value in mix), default=0)
    volume = min(1.0, 30000 / peak) if peak else 1.0

    output = array(
        "h",
        (max(-32768, min(32767, round(v * volume))) for v in mix)
    )
    if sys.byteorder != "little":
        output.byteswap()

    cache = sound_folder / "tempo_cache"
    cache.mkdir(exist_ok=True)
    fingerprint = hashlib.sha256(
        repr((bars, bpm, "sustain-v2")).encode()
    ).hexdigest()[:12]
    destination = cache / (
        "coded_breakbeat_" + fingerprint + ".wav"
    )

    if not destination.exists():
        with wave.open(str(destination), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            wav.writeframes(output.tobytes())

    return destination