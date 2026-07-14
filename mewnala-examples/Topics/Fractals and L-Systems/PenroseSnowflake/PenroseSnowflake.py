# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
""" 
Penrose Snowflake L-System 
by Geraldine Sarmiento. 

This code was based on Patrick Dwyer's L-System class. 
"""
from mewnala import *

from l_system import LSystem
from penrose_snowflake_l_system import PenroseSnowflakeLSystem

def setup():
    size(640, 360)
    stroke(255)
    no_fill()
    global ps
    ps = PenroseSnowflakeLSystem()
    ps.simulate(4)


def draw():
    background(0)
    ps.render()

run()
