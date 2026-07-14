# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
from mewnala import *
def setup():
    size(400, 400, P3D)
    no_loop()


def draw():
    background(255, 0, 0)
    ellipse(mouse_x, mouse_y, 100, 50)
    print "draw"


def key_pressed():
    redraw()
run()
