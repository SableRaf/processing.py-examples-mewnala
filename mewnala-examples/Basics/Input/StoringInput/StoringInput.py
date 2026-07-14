# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Storing Input. 
  
Move the mouse across the screen to change the position
of the circles. The positions of the mouse are recorded
into a deque and played back every frame. Between each
frame, the newest value are added to the end of each array
and the oldest value is deleted. 
"""
from mewnala import *

from collections import deque

history = deque(maxlen=60)


def setup():
    size(640, 360)
    no_stroke()
    fill(255, 153)


def draw():
    background(51)
    history.append((mouse_x, mouse_y))
    for i, (x, y) in enumerate(history):
        ellipse(x, y, i, i)

run()
