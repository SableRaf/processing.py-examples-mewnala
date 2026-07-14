# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Bouncy Bubbles
based on code from Keith Peters.

Multiple-object collision.
The "bounding-box" rendering is imprecise because we've implemented springy
bodies which don't show their deformation.
"""
from mewnala import *
from ball import Ball

balls = []
NUM_BALLS = 12


def setup():
    size(640, 360, P3D)
    for i in range(NUM_BALLS):
        balls.append(Ball(random(width), random(height),
                          random(15, 45), i, balls))
    no_stroke()
    ellipse_mode(RADIUS)
    fill(255, 204)


def draw():
    background(0)
    for ball in balls:
        ball.collide()
        ball.move()
        ball.display()
run()
