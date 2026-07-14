# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Scale
by Denis Grutze.

Paramenters for the scale() function are values specified
as decimal percentages. For example, the method call scale(2.0)
will increase the dimension of the shape by 200 percent.
"""
from mewnala import *

a = 0.0


def setup():
    size(640, 360)
    no_stroke()
    rect_mode(CENTER)
    frame_rate(30)


def draw():
    global a
    background(102)
    a = a + 0.04
    s = cos(a) * 2

    translate(width / 2, height / 2)
    scale(s)
    fill(51)
    rect(0, 0, 50, 50)

    translate(75, 0)
    fill(255)
    scale(s)
    rect(0, 0, 50, 50)

run()
