TURTLE CLASSROOM — NEW SHAPE LIBRARY + BACKGROUNDS

1. Open student_images.py. Set background = "beach", "space", "forest", "city", "classroom", or "none".
2. Use functions from turtle_shapes.py; each returns a list of drawing instructions.
   Example: blinds = venetian_blind(x=-4, y=-3, width=8, slats=7)
   Add ("Blinds", blinds) to image_sequence.
3. Run student_sequence.py (F5) in Thonny on Windows.
4. For your own background, put a PNG or GIF in backgrounds/ and use its filename.
   JPEG is supported only if Pillow is installed.
5. All shapes are drawn by the existing teacher engine; speed and music remain separate.

IMPORTANT: grid coordinates are approximately -5..5. Large shapes may leave the grid.
The old Pattern() and *_shape() functions are still available for existing lessons.
The new library functions return instructions; they do not draw until placed in image_sequence.
