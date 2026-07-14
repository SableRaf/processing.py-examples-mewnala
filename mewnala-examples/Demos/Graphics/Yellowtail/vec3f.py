# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
from mewnala import *
class Vec3f(object):

    def __init__(self):
        self.set(0, 0, 0)

    def __repr__(self):
        return '<Vec3f x:%f y:%f p:%f>' % (self.x, self.y, self.p)

    def set(self, ix, iy, ip):
        self.x = ix
        self.y = iy
        self.p = ip

