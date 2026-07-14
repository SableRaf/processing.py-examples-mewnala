# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Noise Sphere
by David Pena.

Uniform random distribution on the surface of a sphere.
"""
from mewnala import *
from hair import Hair

quantity = 4000
rx = 0
ry = 0

def setup():
    size(640, 360, P3D)
    global half_width, half_height, radius, hairs
    half_width = width / 2
    half_height = height / 2
    radius = height / 3
    hairs = [Hair(radius) for _ in range(quantity)]
    noise_detail(3)

def draw():
    background(0)
    translate(half_width, half_height)
    rxp = ((mouse_x - (half_width)) * 0.005)
    ryp = ((mouse_y - (half_height)) * 0.005)
    global rx, ry
    rx = (rx * 0.9) + (rxp * 0.1)
    ry = (ry * 0.9) + (ryp * 0.1)
    rotate_y(rx)
    rotate_x(ry)
    fill(0)
    no_stroke()
    sphere(radius)

    for hair in hairs:
        hair.render()
run()
