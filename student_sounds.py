"""Editable music score: drums, bass and chords, all from sounds/*.wav.
Each bar has 16 steps. X = play, - = rest. Four steps per beat.
"""

tempo_bpm = 132

breakbeat_score = [
    {
        "kick":     "X--- --X- X--- X---",
        "snare":    "---- X--- ---- X---",
        "hihat":    "X-X- X-X- X-X- X-XX",
        "clap":     "---- X--- ---- X---",
        "bass":     "X--- ---- X--- --X-",
        "chord_C":  "X--- ---- ---- ----",
        "chord_G":  "---- ---- X--- ----",
    },
    {
        "kick":     "X--- ---X X-X- ----",
        "snare":    "---- X--- ---- X--X",
        "hihat":    "X-XX X-X- X-XX XXXX",
        "clap":     "---- X--- ---- X---",
        "bass":     "X--- --X- X--- ----",
        "chord_Am": "X--- ---- ---- ----",
        "chord_F":  "---- ---- X--- ----",
    },
]

# Change tempo_bpm above to speed up or slow down the music.
sound_sequence = [("score_breakbeat", tempo_bpm)]