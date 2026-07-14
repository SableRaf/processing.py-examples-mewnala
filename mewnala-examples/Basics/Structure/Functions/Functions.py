# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Functions.

The drawTarget() function makes it easy to draw many distinct targets.
Each call to drawTarget() specifies the position, size, and number of
rings for each target. 
"""
from mewnala import *


def setup():
    size(640, 360)
    background(51)
    no_stroke()
    no_loop()


def draw():
    draw_target(width * 0.25, height * 0.4, 200, 4)
    draw_target(width * 0.5, height * 0.5, 300, 10)
    draw_target(width * 0.75, height * 0.3, 120, 6)


def draw_target(xloc, yloc, size, num):
    grayvalues = 255 / num
    steps = size / num
    for i in range(num):
        fill(i * grayvalues)
        ellipse(xloc, yloc, size - i * steps, size - i * steps)
run()
