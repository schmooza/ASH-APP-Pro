AUDIO REBUILD — Windows / Thonny

Run student_sequence.py (F5) from the extracted folder.

Changes:
- Music is scheduled with its own Tk after() timer on the main thread.
- No winsound calls from a background music thread.
- Chord WAVs for each BPM are prepared before playback starts.
- A 450 ms startup delay lets the window initialise first.
- Music keeps playing after images finish, until Sound OFF or Exit.
- Image speed remains a visible medium (6 units/frame, 20 ms/frame).
- Individual image speeds and chord BPM remain independent.

Note: winsound and Windows audio drivers can still behave differently across
computers. If the audio only begins after adjusting Windows volume, test
Windows audio output settings and disable audio enhancements/exclusive mode.

Files: student_images.py, student_sounds.py, student_sequence.py,
teacher_sequence.py, sound_effects.py, sounds/*.wav.
