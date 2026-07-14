# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
from mewnala import *
# The Flock (a list of Boid objects)
class Flock(object):

    def __init__(self):
        self.boids = []  # Initialize a list for all the boids.

    def run(self):
        for b in self.boids:
            # Pass the entire list of boids to each boid individually.
            b.run(self.boids)

    def add_boid(self, b):
        self.boids.append(b)

