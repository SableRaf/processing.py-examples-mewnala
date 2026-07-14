# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Performance demo using text rendering
"""
from mewnala import *


def setup():
    size(800, 600, P2D)
    fill(0)


def draw():
    background(255)
    for i in xrange(10000):
        x = random(width)
        y = random(height)
        text("HELLO", x, y)

    if frame_count % 10 == 0:
        print frame_rate
run()
