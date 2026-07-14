# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Blur Filter

Change the default shader to apply a simple, custom blur filter.

Press the mouse to switch between the custom and default shader.
"""
from mewnala import *
blur = None


def setup():
    global blur
    size(640, 360, P2D)
    blur = load_shader("blur.glsl")
    stroke(255, 0, 0)
    rect_mode(CENTER)


def draw():
    filter(blur)
    rect(mouse_x, mouse_y, 150, 150)
    ellipse(mouse_x, mouse_y, 100, 100)
run()
