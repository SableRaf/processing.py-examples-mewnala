# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Composite Objects

An object can include several other objects. Creating such composite objects 
is a good way to use the principles of modularity and build higher levels of 
abstraction within a program.
"""
from mewnala import *

from egg import Egg
from egg_ring import EggRing
from ring import Ring

def setup():
    size(640, 360)
    global er1, er2
    er1 = EggRing(width * 0.45, height * 0.5, 0.1, 120)
    er2 = EggRing(width * 0.65, height * 0.8, 0.05, 180)

def draw():
    background(0)
    er1.transmit()
    er2.transmit()
run()
