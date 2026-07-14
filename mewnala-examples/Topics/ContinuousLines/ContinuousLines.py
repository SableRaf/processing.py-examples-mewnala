# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Continuous Lines. 

Click and drag the mouse to draw a line. 
"""
from mewnala import *


def setup():
    size(640, 360)
    background(102)


def draw():
    stroke(255)
    if mouse_is_pressed == True:
        line(mouse_x, mouse_y, pmouse_x, pmouse_y)

run()
