# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
List Objects.

Demonstrates the syntax for creating a list of custom objects.
"""
from mewnala import *

from module import MovingBall

unit = 40

balls = []


def setup():
    size(640, 360)
    no_stroke()
    for y in range(height / unit):
        for x in range(width / unit):
            balls.append(MovingBall(x * unit, y * unit, unit / 2, unit / 2, random(0.05, 0.8), unit))


def draw():
    background(0)
    for b in balls:
        b.update()
        b.draw()
run()
