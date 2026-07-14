# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
from mewnala import *
class Hair(object):
    def __init__(self, radius):
        self.radius = radius
        self.phi = random(TAU)
        self.slow = random(1.15, 1.2)
        self.theta = asin(random(-self.radius, self.radius) / self.radius)
        self.z = self.radius * sin(self.theta)

    def render(self):
        o_f_f = (noise(millis() * 0.0005, sin(self.phi)) - 0.5) * 0.3
        o_f_fb = (noise(millis() * 0.0007, sin(self.z) * 0.01) - 0.5) * 0.3

        self.theta_f_f = self.theta + o_f_f
        phi_f_f = self.phi + o_f_fb
        x = self.radius * cos(self.theta) * cos(self.phi)
        y = self.radius * cos(self.theta) * sin(self.phi)
        self.z = self.radius * sin(self.theta)

        xo = self.radius * cos(self.theta_f_f) * cos(phi_f_f)
        yo = self.radius * cos(self.theta_f_f) * sin(phi_f_f)
        zo = self.radius * sin(self.theta_f_f)

        xb = xo * self.slow
        yb = yo * self.slow
        zb = zo * self.slow

        with begin_shape(LINES):
            stroke(0)
            vertex(x, y, self.z)
            stroke(200, 150)
            vertex(xb, yb, zb)
