IMAGE SPEED PER ITEM

Edit student_images.py and add ("speed", NUMBER) inside each image.
NUMBER is an integer from 1 (slow) to 100 (very fast).
Example: letter_A = [("speed", 80), ("color", "red"), ...]
For a Pattern, put ("speed", 20) in its shape instructions.
Each image resets to speed 100 unless overridden.
Speed +/- buttons change the current image speed while running; the next image resets to its own speed.

Music in student_sounds.py has independent per-chord BPM and is NOT affected by image speed.
