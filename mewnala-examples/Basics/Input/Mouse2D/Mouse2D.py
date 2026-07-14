# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Mouse 2D.

Moving the mouse changes the position and size of each box.
"""
from mewnala import *


def setup():
    size(640, 360)
    no_stroke()
    rect_mode(CENTER)


def draw():
    background(51)
    fill(255, 204)
    rect(mouse_x, height / 2, mouse_y / 2 + 10, mouse_y / 2 + 10)
    inverse_x = width - mouse_x
    inverse_y = height - mouse_y
    rect(inverse_x, height / 2, (inverse_y / 2) + 10, (inverse_y / 2) + 10)

run()
