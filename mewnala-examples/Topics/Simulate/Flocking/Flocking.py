# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Flocking 
by Daniel Shiffman.    

An implementation of Craig Reynold's Boids program to simulate
the flocking behavior of birds. Each boid steers itself based on 
rules of avoidance, alignment, and coherence.

Click the mouse to add a boid.
"""
from mewnala import *

from boid import Boid
from flock import Flock

flock = Flock()

def setup():
    size(640, 360)
    # Add an initial set of boids into the system
    for i in range(80):
        flock.add_boid(Boid(width / 2, height / 2))


def draw():
    background(50)
    flock.run()

# Add a boid into the System
def mouse_pressed():
    flock.add_boid(Boid(mouse_x, mouse_y))

run()
