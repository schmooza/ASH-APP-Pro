"""Turtle drawing player. Students normally run student_images.py (F5)."""

def play_sequence(image_sequence, colors=None, background=None):
    """Play drawings with the existing sound playlist and Turtle engine."""
    from student_sounds import sound_sequence, tempo_bpm
    from teacher_sequence import Sequence, start

    show = Sequence()
    for title, drawing in image_sequence:
        show.add(title, drawing)
    steps = [("start_playlist", sound_sequence, tempo_bpm)] + show.build()
    start(steps, colors if colors is not None else ["red", "pink"], background=background)


if __name__ == "__main__":
    # Older projects can still run student_sequence.py directly.
    from student_images import image_sequence, colors, background
    play_sequence(image_sequence, colors, background)
