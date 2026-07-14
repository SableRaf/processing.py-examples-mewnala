# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Transparency.

Move the pointer left and right across the image to change
its position. This program overlays one image over another
by modifying the alpha value of the image with the tint() function.
"""
from mewnala import *

offset = 0
easing = 0.05


def setup():
    size(640, 360)
    global img
    img = load_image("moonwalk.jpg")    # Load an image into the program


def draw():
    global offset
    image(img, 0, 0)    # Display at full opacity
    dx = (mouse_x - img.width / 2) - offset
    offset += dx * easing
    tint(255, 127)    # Display at half opacity
    image(img, offset, 0)
run()
