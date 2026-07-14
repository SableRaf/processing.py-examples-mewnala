# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Create Image.

The createImage() function provides a fresh buffer of pixels to play with.
This example creates an image gradient.
"""
from mewnala import *


def setup():
    size(640, 360)
    global img
    img = create_image(230, 230, ARGB)
    pix_count = len(img.pixels)
    for i in range(pix_count):
        a = map(i, 0, pix_count, 255, 0)
        img.pixels[i] = color(0, 153, 204, a)


def draw():
    background(0)
    image(img, 90, 80)
    image(img, mouse_x - img.width / 2, mouse_y - img.height / 2)
run()
