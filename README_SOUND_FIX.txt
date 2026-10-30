SOUND FIX — Independent music scheduler

Run student_sequence.py in Thonny on Windows.

The chord playlist now runs in a dedicated daemon thread rather than
Tkinter after() timers. This keeps music independent from fast image
animation and allows chords to continue after drawing finishes.

Default image speed is now Medium (50). Each image can override it with
("speed", 1..100). Student chord BPM is unchanged.

Press M or use SOUND ON/OFF to mute and unmute. Restart restarts the
playlist. Exit closes the app and stops the music.

Keep the sounds folder next to sound_effects.py.

Note: winsound plays only one WAV at a time. Very fast BPM may sound
choppy, and Windows playback has not been tested in this environment.
