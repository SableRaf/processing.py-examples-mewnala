# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Multiple Particle Systems
by Daniel Shiffman.

Click the mouse to generate a burst of particles
at mouse location.

Each burst is one instance of a particle system
with Particles and CrazyParticles (a subclass of Particle).
Note use of Inheritance and Polymorphism here.
"""
from mewnala import *

from crazy_particle import CrazyParticle
from particle import Particle
from particle_system import ParticleSystem

systems = None

def setup():
    global systems
    size(640, 360)
    systems = []


def draw():
    background(0)
    for ps in systems:
        ps.run()
        ps.add_particle()

    if not systems:
        fill(255)
        text_align(CENTER)
        text("click mouse to add particle systems", width / 2, height / 2)


def mouse_pressed():
    systems.append(ParticleSystem(1, PVector(mouse_x, mouse_y)))
run()
