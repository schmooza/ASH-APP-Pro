MELODIC TURTLE: 1-SECOND CHORDS (WINDOWS / THONNY)

Open student_sequence.py in Thonny and press F5.

Students edit student_images.py for drawings and student_sounds.py for music.
Each chord WAV lasts 1 second, and the progression repeats continuously
until the drawing ends. Example: C -> D -> Em -> G.

10 chord WAVs added: chord_C, chord_D, chord_Em, chord_F, chord_G,
chord_Am, chord_Dm, chord_Bm, chord_G7, chord_Cmaj7.
The original 25 sound effects remain available in sounds/.

Change sound_sequence in student_sounds.py to choose the chord order.
SOUND ON/OFF or the M key mutes/unmutes the music.

Sound is played by winsound (built into Windows). No extra packages.
Each WAV is a softly layered, sustained chord with a gentle arpeggio onset.
The WAV files play sequentially, with potentially tiny gaps between chords.
This is not crossfaded audio, because winsound cannot mix simultaneous WAVs.
