# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Increment Decrement.

Writing "a += 1" is equivalent to "a = a + 1".
Writing "a -= 1" is equivalent to "a = a - 1".
"""
from mewnala import *

a = 0
b = 0
direction = True

def setup():
    size(640, 360)
    color_mode(RGB, width)
    b = width
    frame_rate(30)


def draw():
    global direction, a, b
    a += 1
    if a > width:
        a = 0
        direction = not direction
    if direction:
        stroke(a)
    else:
        stroke(width - a)
    line(a, 0, a, height / 2)
    b -= 1
    if b < 0:
        b = width

    if direction:
        stroke(width - b)
    else:
        stroke(b)

    line(b, height / 2 + 1, b, height)

run()
