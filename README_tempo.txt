TEMPO CONTROLS (Windows / Thonny)

Run student_sequence.py (F5).

In student_sounds.py, set tempo_bpm = 60 (slow), 120 (medium),
240 (fast), 480 (very fast), or 960 (extremely fast).
Any number between 60 and 960 works. One chord plays per beat.

Students can edit sound_sequence independently of student_images.py.
The soundtrack repeats throughout drawing. Sound ON/OFF and M key remain.

Shortened chord WAVs are generated in sounds/tempo_cache automatically.
Chord pitches are unchanged. Windows winsound plays only one WAV at once.
Very high tempos may have tiny gaps or timing jitter due to Windows/Tk scheduling.
