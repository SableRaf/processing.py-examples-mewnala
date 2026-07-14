# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Handles.

Click and drag the white boxes to change their position.
"""
from mewnala import *
from handle import Handle

handles = []


def setup():
    size(640, 360)
    num = height / 15
    hsize = 10
    for i in range(num):
        handles.append(Handle(width / 2, 10 + i * 15,
                              50 - hsize / 2, 10, handles))


def draw():
    background(153)
    for h in handles:
        h.update()
        h.display()
    fill(0)
    rect(0, 0, width / 2, height)


def mouse_released():
    for h in handles:
        h.release_event()
run()
