# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
""" 
Penrose Tile L-System 
by Geraldine Sarmiento.

This code was based on Patrick Dwyer's L-System class. 
"""
from mewnala import *

from l_system import LSystem
from penrose_l_system import PenroseLSystem

def setup():
    size(640, 360)
    global ds
    ds = PenroseLSystem()
    ds.simulate(4)

def draw():
    background(0)
    ds.render()

run()
