# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Performance demo using quad rendering
"""
from mewnala import *


def setup():
    size(800, 600, P2D)
    no_stroke()
    fill(0, 1)


def draw():
    background(255)
    for i in xrange(50000):
        x = random(width)
        y = random(height)
        rect(x, y, 30, 30)

    if frame_count % 10 == 0:
        print frame_rate
run()
