# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
On/Off.    

Uses the default lights to show a simple box. The lights() function
is used to turn on the default lighting. Click the mouse to turn the
lights off.
"""
from mewnala import *

spin = 0.0


def setup():
    size(640, 360, P3D)
    no_stroke()


def draw():
    global spin
    background(51)

    if not mouse_is_pressed:
        lights()

    spin += 0.01

    with push_matrix():
        translate(width / 2, height / 2, 0)
        rotate_x(PI / 9)
        rotate_y(PI / 5 + spin)
        box(150)

run()
