# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Alpha Mask.

Loads a "mask" for an image to specify the transparency
in different parts of the image. The two images are blended
together using the mask() method of PImage.
"""
from mewnala import *


def setup():
    size(640, 360)
    global img, img_mask
    img = load_image("moonwalk.jpg")
    img_mask = load_image("mask.jpg")
    img.mask(img_mask)
    image_mode(CENTER)


def draw():
    background(0, 102, 153)
    image(img, width / 2, height / 2)
    image(img, mouse_x, mouse_y)
run()
