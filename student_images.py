# Student file: press F5 to run your drawings.
# Helper Python files are stored in program_files/.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / "program_files"))

# Choose a background: "none", "beach", "space", "forest", "city", or "classroom".
# To use your own PNG/GIF, put it in backgrounds/ and write its filename.
background = "beach"

# New simple shape library: triangle(), star(), rectangle(), venetian_blind(), etc.
from turtle_shapes import *
# Keep the rectangle function available even if a drawing list is named rectangle.
shape_rectangle = rectangle
# OPTIONAL EASTER EGG GALLERY — remove # from both marked lines to enable.
# from easter_egg_gallery import easter_egg_sequence

"""STUDENT IMAGES: create pictures independently of sounds."""
from teacher_sequence import Pattern, triangle_shape, square_shape, pentagon_shape, hexagon_shape, star_shape, rectangle_shape




#___make stuff_____________________________________________________________________

colors = ["blue","pink"]

my_blinds = []

for i in range(10):
    y = 8 - i * 0.5

    my_blinds += [
        ("speed", 0),
        ("color", "blue"),
        ("up", -8, y),
        ("heading", 0),
        ("down",),
        ("forward", 5),
    ]

my_blinds2 = []

for i in range(10):
    y = 8 - i * 0.5

    my_blinds += [
        ("speed", 0),
        ("color", "yellow"),
        ("up", -7, y),
        ("heading", 0),
        ("down",),
        ("forward", 5),
    ]




#____play stuff in order top to bottom______________________________________________________________

image_sequence = [
    ("Scene 1 - Space", [
        ("background", "space"),
        ("speed", 0),
        ("up", -4, 0),
        ("color", "yellow"),
        ("width", 5),
        ("heading", 0),
        ("down",),
        ("forward", 8),
    ]),
    ("Scene 2 - Beach", [
        ("background", "beach"),
        # The yellow line stays visible.
        ("up", -4, -2),
        ("color", "blue"),
        ("heading", 0),
        ("down",),
        ("forward", 8),
    ]),
    ("Scene 3 - Forest", [
        ("clear",),
        ("background", "forest"),
        ("up", 0, -3),
        ("color", "red"),
        ("heading", 90),
        ("down",),
        ("forward", 6),
    ]),
]






#___________________________________________________________________________________

# EASY SHAPE LIBRARY EXAMPLES — uncomment one or more below in image_sequence.
# beach_sun = circle(x=3, y=3, radius=0.7, color="orange", fill="yellow")

# one_triangle = triangle(x=-2, y=-2, size=2, angle=45, color="green")
# blinds = venetian_blind(x=-4, y=-3, width=8, slats=7, slat_height=0.5)
# image_sequence.append(("Venetian blinds", blinds))

# OPTIONAL EASTER EGG GALLERY — uncomment this line AND the import above.
# image_sequence.extend(easter_egg_sequence)


# REPEAT A SHAPE (OPTIONAL)
# Remove the # from the next lines to make five rectangles in a row.
# my_rectangles = repeat_shape(
#     rectangle, count=5, x=-8, y=0, spacing=4,
#     width=3, height=2, color="blue"
# )
# image_sequence.append(("5 Rectangles", my_rectangles))

# REPEAT YOUR OWN DRAWING (OPTIONAL)
# Works with any drawing list that uses ("up", x, y) to position itself.
# my_repeated_lines = repeat_shape(my_blinds, count=3, spacing=3)
# image_sequence.append(("Repeated Drawing", my_repeated_lines))

# ROTATE AND FILL (OPTIONAL EXAMPLES)
# Eight coloured rectangles, each turned another 45 degrees:
# spinning_colours = repeat_shape(
#     shape_rectangle, count=8, x=0, y=0, dx=0, dy=0,
#     rotate=45, width=3, height=1, random_fill=True
# )
# image_sequence.append(("Spinning Colours", spinning_colours))
# One fill colour, repeated upwards:
# rising_stars = repeat_shape(
#     star, count=4, x=0, y=-5, dx=0, dy=3,
#     rotate=20, size=2, fill="yellow"
# )
# image_sequence.append(("Rising Stars", rising_stars))
# For a custom command list, use: repeat_shape(letter_A, count=3, rotate=30)


# VERTICAL PATTERNS (OPTIONAL)
# Set dx=0. Positive dy goes up; negative dy goes down.
# Uncomment a drawing definition, then put its name INSIDE image_sequence.
# vertical_circles = repeat_shape(
#     circle, count=5, x=-5, y=-8, dx=0, dy=3,
#     radius=1, fill="yellow"
# )
# rising_stars = repeat_shape(
#     star, count=4, x=-5, y=-6, dx=0, dy=3,
#     rotate=20, size=2, fill="yellow"
# )
# vertical_rectangles = repeat_shape(
#     rectangle, count=4, x=3, y=-7, dx=0, dy=4,
#     width=3, height=2, fill="lightblue"
# )
# vertical_spinning_colours = repeat_shape(
#     rectangle, count=4, x=3, y=-6, dx=0, dy=3,
#     rotate=30, width=3, height=1, random_fill=True,
#     palette=["red", "blue", "green", "orange"]
# )
# Example entries to add BEFORE the closing ] of image_sequence:
#     ("Vertical Circles", vertical_circles),
#     ("Rising Stars", rising_stars),
#     ("Vertical Rectangles", vertical_rectangles),
#     ("Vertical Spinning Colours", vertical_spinning_colours),


# VERTICAL TRIANGLES AND LINES (OPTIONAL)
# Uncomment the definitions and add the names inside image_sequence.
# vertical_triangles = repeat_shape(
#     triangle, count=5, x=-4, y=-8, dx=0, dy=3,
#     size=2, fill="yellow", rotate=15
# )
# one_line = [
#     ("up", 0, 0), ("heading", 0), ("down",),
#     ("color", "blue"), ("width", 4), ("forward", 3),
# ]
# vertical_lines = repeat_shape(
#     one_line, count=5, x=-2, y=-6, dx=0, dy=3
# )
# Add these INSIDE image_sequence, before its closing ]:
#     ("Vertical Triangles", vertical_triangles),
#     ("Vertical Lines", vertical_lines),


# --------------------------------------------------------------
# RUN YOUR DRAWINGS! Open student_images.py in Thonny and press F5.
# This runs the image_sequence above with your sounds and background.
# Keep these lines at the bottom of this file.
if __name__ == "__main__":
    from student_sequence import play_sequence
    play_sequence(image_sequence, colors, background)
