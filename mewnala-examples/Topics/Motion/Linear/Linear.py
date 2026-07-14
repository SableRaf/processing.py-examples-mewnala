# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Linear Motion.

Changing a variable to create a moving line. When the line moves off the edge
of the window, the variable is set to 0, which places the line back at the
bottom of the screen.
"""
from mewnala import *


def setup():
    size(640, 360)
    global a
    stroke(255)
    a = height / 2


def draw():
    global a
    background(51)
    line(0, a, width, a)
    a -= 0.5
    if a < 0:
        a = height
run()
