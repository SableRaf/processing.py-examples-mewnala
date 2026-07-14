# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
from mewnala import *
# Gravitational Attraction (3D)
# Daniel Shiffman <http://www.shiffman.net>
# A class for(object): an attractive body in our world


class Sun(object):

    def __init__(self):
        self.location = PVector(0, 0)
        # Mass, tied to size
        self.mass = 20
        # Universal gravitational constant (arbitrary value).
        self.G = 0.4

    def attract(self, m):
        # Calculate direction of force.
        force = PVector.sub(self.location, m.location)
        d = force.mag()  # Distance between objects
        # Limiting the distance to eliminate "extreme" results for very close
        # or very far objects.
        d = constrain(d, 5.0, 25.0)
        # Calculate gravitional force magnitude.
        strength = (self.G * self.mass * m.mass) / (d * d)
        force.set_mag(strength)  # Get force vector --> magnitude * direction
        return force

    # Draw Sun.
    def display(self):
        stroke(255)
        no_fill()
        with push_matrix():
            translate(self.location.x, self.location.y, self.location.z)
            sphere(self.mass * 2)

