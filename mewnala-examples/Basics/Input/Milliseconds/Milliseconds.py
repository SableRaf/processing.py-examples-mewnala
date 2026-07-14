# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Milliseconds. 

A millisecond is 1/1000 of a second. 
Processing keeps track of the number of milliseconds a program has run.
By modifying this number with the modulo(%) operator, 
different patterns in time are created.  
"""
from mewnala import *


def setup():
    global scale
    size(640, 360)
    no_stroke()
    scale = width / 20


def draw():
    for i in range(0, scale, 1):
        color_mode(RGB, (i + 1) * scale * 10)
        fill(millis() % ((i + 1) * scale * 10))
        rect(i * scale, 0, scale, height)

run()
