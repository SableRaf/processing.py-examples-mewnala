# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Acceleration with Vectors
by Daniel Shiffman.

Demonstration of the basics of motion with vector.
A "Mover" object stores location, velocity, and acceleration as vectors The
motion is controlled by affecting the acceleration (in this case towards the
mouse)
For more examples of simulating motion and physics with vectors, see
Simulate/ForcesWithVectors, Simulate/GravitationalAttraction3D
"""
from mewnala import *
from mover import Mover


def setup():
    global mover
    size(640, 360)
    mover = Mover()


def draw():
    background(0)
    # Update the location
    mover.update()
    # Display the Mover
    mover.display()
run()
