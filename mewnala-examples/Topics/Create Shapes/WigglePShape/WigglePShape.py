# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
WigglePShape. 

How to move the individual vertices of a PShape.
"""
from mewnala import *
from wiggler import Wiggler

def setup():
    size(640, 360, P2D)
    smooth()
    global w
    w = Wiggler()


def draw():
    background(255)
    w.display()
    w.wiggle()

run()
