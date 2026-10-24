MODULAR TURTLE: PER-CHORD TEMPO (Windows / Thonny)

Run student_sequence.py (F5). Keep all files together and sounds/ next to them.

Students edit:
  student_images.py  - images and drawing instructions
  student_sounds.py  - chords and their individual tempos

Each sound entry is ("chord_C", 120), where 120 is BPM.
Each chord lasts 60 / BPM seconds. Allowed BPM: 60 to 960.
Example: ("chord_D", 240) lasts 0.25 seconds.

The sequence repeats continuously while the turtle draws, then stops.
Sound ON/OFF (M key) still works.
The optional tempo_bpm is a fallback for old-style entries like "chord_C".

Teacher modules: teacher_sequence.py and sound_effects.py.
Uses Windows built-in winsound; no pip installation.

NOTE: At very high BPM, winsound/Windows scheduling can introduce gaps.
This is chord-duration control, not audio pitch-shifting.
