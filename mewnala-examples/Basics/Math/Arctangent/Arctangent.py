# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Arctangent. 

Move the mouse to change the direction of the eyes. 
The atan2() function computes the angle from each eye 
to the cursor. 
"""
from mewnala import *

from eye import Eye

e1 = Eye(250, 16, 120)
e2 = Eye(164, 185, 80)
e3 = Eye(420, 230, 220)


def setup():
    size(640, 360)
    no_stroke()


def draw():
    background(102)

    e1.update(mouse_x, mouse_y)
    e2.update(mouse_x, mouse_y)
    e3.update(mouse_x, mouse_y)
    e1.display()
    e2.display()
    e3.display()

run()
