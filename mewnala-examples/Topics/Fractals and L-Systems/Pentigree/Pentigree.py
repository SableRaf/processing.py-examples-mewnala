# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
""" 
Pentigree L-System 
by Geraldine Sarmiento. 

This code was based on Patrick Dwyer's L-System class. 
"""
from mewnala import *

from l_system import LSystem
from pentigree_l_system import PentigreeLSystem

def setup():
    size(640, 360)
    global ps
    ps = PentigreeLSystem()
    ps.simulate(3)


def draw():
    background(0)
    ps.render()

run()
