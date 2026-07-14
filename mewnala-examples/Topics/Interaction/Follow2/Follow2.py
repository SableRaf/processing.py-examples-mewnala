# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Follow 2    
based on code from Keith Peters. 

A two-segmented arm follows the cursor position. The relative
angle between the segments is calculated with atan2() and the
position calculated with sin() and cos().
"""
from mewnala import *
x = [0.0] * 2
y = [0.0] * 2
seg_length = 50


def setup():
    size(640, 360)
    stroke_weight(20.0)
    stroke(255, 100)


def draw():
    background(0)
    drag_segment(0, mouse_x, mouse_y)
    drag_segment(1, x[0], y[0])


def drag_segment(i, xin, yin):
    dx = xin - x[i]
    dy = yin - y[i]
    angle = atan2(dy, dx)
    x[i] = xin - cos(angle) * seg_length
    y[i] = yin - sin(angle) * seg_length
    segment(x[i], y[i], angle)


def segment(x, y, a):
    with push_matrix():
        translate(x, y)
        rotate(a)
        line(0, 0, seg_length, 0)

run()
