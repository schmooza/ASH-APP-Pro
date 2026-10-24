"""Windows built-in sound module for the Turtle animation. No pip installs.

WAV files live in the adjacent sounds/ folder. Playback is asynchronous,
so Turtle continues animating. Beep fallback uses a daemon thread.
"""
from pathlib import Path
import threading
import wave
from array import array
import sys

try:
    import winsound
except ImportError:
    winsound = None

SOUND_FOLDER = Path(__file__).resolve().parent.parent / "sounds"
sound_enabled = True
_finite_after_id = None
_finite_widget = None
_finite_generation = 0

BEEPS = {"letter": (600, 150), "triangle": (900, 200), "finish": (1200, 400)}


def is_sound_on():
    return sound_enabled


def toggle_sound():
    """Switch all sounds on/off and stop any playing sound when muted."""
    global sound_enabled
    sound_enabled = not sound_enabled
    if not sound_enabled:
        stop()
    return sound_enabled


def set_sound(enabled):
    """Explicitly enable or mute sound."""
    global sound_enabled
    sound_enabled = bool(enabled)
    if not sound_enabled:
        stop()


def play(name):
    cancel_finite_loop()
    """Play a named WAV file, or a simple tone if the file is absent."""
    if not sound_enabled:
        return
    if winsound is None:
        print("Sound is supported on Windows only (winsound).")
        return
    if not isinstance(name, str) or not name.replace("_", "").isalnum():
        print("Invalid sound name:", name)
        return
    wav_file = SOUND_FOLDER / (name + ".wav")
    try:
        if wav_file.is_file():
            winsound.PlaySound(str(wav_file),
                               winsound.SND_FILENAME | winsound.SND_ASYNC)
        elif name in BEEPS:
            pitch, duration = BEEPS[name]
            threading.Thread(target=winsound.Beep,
                             args=(pitch, duration), daemon=True).start()
        else:
            print("Sound not found:", wav_file)
    except RuntimeError as exc:
        print("Could not play sound", name, ":", exc)


def stop():
    """Stop any currently playing WAV sound."""
    cancel_finite_loop()
    if winsound is not None:
        winsound.PlaySound(None, 0)


def play_ambient(name):
    """Loop a WAV sound until stop_ambient() or another WAV plays."""
    cancel_finite_loop()
    if not sound_enabled:
        return
    if winsound is None:
        print("Ambient audio requires Windows.")
        return
    if not isinstance(name, str) or not name.replace("_", "").isalnum():
        print("Invalid sound name:", name)
        return
    wav_file = SOUND_FOLDER / (name + ".wav")
    if not wav_file.is_file():
        print("Sound not found:", wav_file)
        return
    winsound.PlaySound(str(wav_file), winsound.SND_FILENAME |
                       winsound.SND_ASYNC | winsound.SND_LOOP)


def stop_ambient():
    """Stop the current WAV sound or ambient loop."""
    stop()


def cancel_finite_loop():
    """Cancel the next scheduled repeat, if there is one."""
    global _finite_after_id, _finite_widget, _finite_generation
    _finite_generation += 1
    if _finite_after_id is not None and _finite_widget is not None:
        try:
            _finite_widget.after_cancel(_finite_after_id)
        except Exception:
            pass
    _finite_after_id = None
    _finite_widget = None


def repeat_sound(name, count, widget):
    """Play a WAV exactly count times without freezing Turtle animation.

    widget is the Turtle Tk canvas, supplied by teacher_sequence.py.
    Repeats are timed to the WAV file's duration.
    """
    global _finite_after_id, _finite_widget
    cancel_finite_loop()
    if not sound_enabled or winsound is None:
        return
    if type(count) is not int or count < 1:
        print('Sound repeat count must be a positive integer')
        return
    if not isinstance(name, str) or not name.replace('_', '').isalnum():
        print('Invalid sound name:', name)
        return
    wav_file = SOUND_FOLDER / (name + '.wav')
    if not wav_file.is_file():
        print('Sound not found:', wav_file)
        return
    try:
        with wave.open(str(wav_file), 'rb') as wav:
            duration_ms = max(
                1, round(1000 * wav.getnframes() / wav.getframerate())
            )
    except (OSError, wave.Error, ZeroDivisionError) as exc:
        print('Cannot read WAV duration:', exc)
        return

    generation = _finite_generation
    _finite_widget = widget

    def play_next(remaining):
        global _finite_after_id, _finite_widget
        _finite_after_id = None
        if generation != _finite_generation or not sound_enabled:
            return
        try:
            winsound.PlaySound(
                str(wav_file),
                winsound.SND_FILENAME | winsound.SND_ASYNC
            )
        except RuntimeError as exc:
            print('Could not play sound:', exc)
            return
        if remaining > 1:
            _finite_after_id = widget.after(
                duration_ms, play_next, remaining - 1
            )
        else:
            _finite_widget = None

    play_next(count)


# Build one WAV containing the full progression, then loop that WAV.
# This avoids repeatedly restarting the Windows sound device for every chord.
_playlist_active = False
_playlist_widget = None
_playlist_timer = None
_playlist_file = None


def start_playlist(entries, widget=None, tempo_bpm=240):
    """Loop a chord progression without changing Turtle drawing speed."""
    global _playlist_active, _playlist_widget, _playlist_timer, _playlist_file

    if widget is None:
        raise ValueError("A Turtle Tk canvas is required")
    if not 60 <= tempo_bpm <= 960:
        raise ValueError("Tempo must be 60-960 BPM")

    validated = []
    for entry in entries:
        if isinstance(entry, str):
            name, bpm = entry, tempo_bpm
        elif isinstance(entry, (tuple, list)) and len(entry) == 2:
            name, bpm = entry
        else:
            raise ValueError("Use ('chord_C', 120) for each chord")

        if not isinstance(name, str) or not name.replace('_', '').isalnum():
            raise ValueError("Invalid chord name: " + repr(name))
        if type(bpm) not in (int, float) or not 60 <= bpm <= 960:
            raise ValueError("Chord BPM must be 60-960")
        validated.append((name, bpm))

    stop_playlist()
    if not validated:
        return

    # A coded drum score is rendered from the existing sample library.
    if len(validated) == 1 and validated[0][0] == "score_breakbeat":
        from student_sounds import breakbeat_score
        from score_player import render_score

        _playlist_file = render_score(
            breakbeat_score, validated[0][1], SOUND_FOLDER
        )
        _playlist_active = True
        _playlist_widget = widget

        def begin_score():
            global _playlist_timer
            _playlist_timer = None
            if _playlist_active and sound_enabled:
                _play_playlist_file()

        _playlist_timer = widget.after(450, begin_score)
        return

    # A single drum loop/sample plays at its original full length.
    # Chord sequences still use the usual one-beat-per-entry timing.
    if len(validated) == 1 and not validated[0][0].startswith("chord_"):
        loop_path = SOUND_FOLDER / (validated[0][0] + ".wav")
        if not loop_path.is_file():
            raise FileNotFoundError("Missing WAV for " + validated[0][0])
        _playlist_file = loop_path
        _playlist_active = True
        _playlist_widget = widget

        def begin_loop():
            global _playlist_timer
            _playlist_timer = None
            if _playlist_active and sound_enabled:
                _play_playlist_file()

        _playlist_timer = widget.after(450, begin_loop)
        return

    # Each chord is trimmed to one beat at its selected BPM.
    pieces = []
    parameters = None

    for name, bpm in validated:
        path = _tempo_chord_file(name, bpm)
        if path is None:
            raise FileNotFoundError("Missing WAV for " + name)

        with wave.open(str(path), 'rb') as wav:
            params = (
                wav.getnchannels(),
                wav.getsampwidth(),
                wav.getframerate()
            )
            if parameters is None:
                parameters = params
            if params != parameters:
                raise ValueError(
                    "Chord WAV files have incompatible audio formats"
                )

            frames = wav.readframes(wav.getnframes())
            wanted = (
                max(1, round(params[2] * 60 / bpm))
                * params[0] * params[1]
            )
            pieces.append(frames[:wanted])

    cache = SOUND_FOLDER / 'tempo_cache'
    cache.mkdir(exist_ok=True)

    from hashlib import sha256
    fingerprint = sha256(repr(validated).encode()).hexdigest()[:16]
    destination = cache / ('playlist_' + fingerprint + '.wav')

    if not destination.exists():
        with wave.open(str(destination), 'wb') as wav:
            wav.setnchannels(parameters[0])
            wav.setsampwidth(parameters[1])
            wav.setframerate(parameters[2])
            wav.writeframes(b''.join(pieces))

    _playlist_file = destination
    _playlist_active = True
    _playlist_widget = widget

    def begin_audio():
        global _playlist_timer
        _playlist_timer = None
        if _playlist_active and sound_enabled:
            _play_playlist_file()

    _playlist_timer = widget.after(450, begin_audio)


def _play_playlist_file():
    if not (
        _playlist_active and sound_enabled
        and winsound and _playlist_file
    ):
        return

    try:
        winsound.PlaySound(
            str(_playlist_file),
            winsound.SND_FILENAME |
            winsound.SND_ASYNC |
            winsound.SND_LOOP |
            winsound.SND_NODEFAULT
        )
        print('Music playing:', _playlist_file.name)
    except RuntimeError as exc:
        print('Music playback error:', exc)


def _tempo_chord_file(name, bpm):
    """Create a short chord WAV for this BPM without changing its pitch."""
    source = SOUND_FOLDER / (name + '.wav')
    if not source.is_file():
        return None
    if not name.startswith('chord_'):
        return source

    target_ms = round(60000 / bpm)
    if target_ms >= 1000:
        return source

    cache = SOUND_FOLDER / 'tempo_cache'
    cache.mkdir(exist_ok=True)
    dest = cache / (name + '_' + str(target_ms) + 'ms.wav')

    if dest.exists():
        return dest

    with wave.open(str(source), 'rb') as wav:
        channels, width, rate, frames, compression, description = wav.getparams()
        if channels != 1 or width != 2 or compression != 'NONE':
            return source

        samples = array('h')
        samples.frombytes(wav.readframes(frames))

    if sys.byteorder != 'little':
        samples.byteswap()

    count = min(len(samples), max(1, round(rate * target_ms / 1000)))
    output = array('h', samples[:count])
    fade = min(count // 3, max(1, round(rate * 0.008)))

    for i in range(fade):
        output[count - fade + i] = int(
            output[count - fade + i] * (fade - i - 1) / fade
        )

    if sys.byteorder != 'little':
        output.byteswap()

    with wave.open(str(dest), 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(output.tobytes())

    return dest


def stop_playlist():
    global _playlist_active, _playlist_timer
    _playlist_active = False

    if _playlist_timer is not None and _playlist_widget is not None:
        try:
            _playlist_widget.after_cancel(_playlist_timer)
        except Exception:
            pass

    _playlist_timer = None
    if winsound is not None:
        winsound.PlaySound(None, 0)


def toggle_playlist_audio():
    global sound_enabled
    sound_enabled = not sound_enabled

    if not sound_enabled:
        if winsound is not None:
            winsound.PlaySound(None, 0)
    else:
        _play_playlist_file()

    return sound_enabled