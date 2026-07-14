# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Brightness 
by Rusty Robison. 

Brightness is the relative lightness or darkness of a color.
Move the cursor vertically over each bar to alter its brightness. 
"""
from mewnala import *

bar_width = 20
last_bar = -1


def setup():
    size(32 * bar_width, 360)
    color_mode(HSB, width, 100, width)
    no_stroke()
    background(0)


def draw():
    global last_bar
    which_bar = mouse_x / bar_width
    if which_bar != last_bar:
        bar_x = which_bar * bar_width
        fill(bar_x, 100, height - mouse_y)
        rect(bar_x, 0, bar_width, height)
        last_bar = which_bar

run()
