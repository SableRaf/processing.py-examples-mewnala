# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
from mewnala import *
from particle import Particle


class ParticleSystem(object):

    def __init__(self, n, sprite):
        self.particle_shape = create_shape(PShape.GROUP)
        self.particles = [Particle(sprite) for _ in range(n)]
        for p in self.particles:
            self.particle_shape.add_child(p.get_shape())

    def update(self):
        for p in self.particles:
            p.update()

    def set_emitter(self, x, y):
        for p in self.particles:
            if p.is_dead():
                p.rebirth(x, y)

    def display(self):
        shape(self.particle_shape)
