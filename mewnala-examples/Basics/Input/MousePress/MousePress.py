# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Mouse Press.

Move the mouse to position the shape.
Press the mouse button to invert the color.
"""
from mewnala import *


def setup():
    size(640, 360)
    no_smooth()
    fill(126)
    background(102)


def draw():
    if mouse_is_pressed:
        stroke(255)
    else:
        stroke(0)
    line(mouse_x - 66, mouse_y, mouse_x + 66, mouse_y)
    line(mouse_x, mouse_y - 66, mouse_x, mouse_y + 66)

run()
