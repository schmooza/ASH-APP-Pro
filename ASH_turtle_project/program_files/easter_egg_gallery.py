"""Optional Easter egg gallery for the Turtle app.

Import easter_egg_sequence in student_images.py to enable these drawings.
"""
from easter_eggs import (
    nike_logo,
    billabong_logo,
    toyota_logo,
    nasa_logo,
    dominoes_logo,
)

# Comment out any logo you do not want to display.
easter_egg_sequence = [
    ("Nike", nike_logo()),
    ("Billabong", billabong_logo()),
    ("Toyota", toyota_logo()),
    ("NASA", nasa_logo()),
    ("Dominoes", dominoes_logo()),
]
