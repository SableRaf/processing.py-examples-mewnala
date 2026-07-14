# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Edge Detection

Change the default shader to apply a simple, custom edge detection filter.

Press the mouse to switch between the custom and default shader.
"""
from mewnala import *
edges = None
img = None
enabled = True


def setup():
    global img, edges, enabled
    size(640, 360, P2D)
    img = load_image("leaves.jpg")
    edges = load_shader("edges.glsl")


def draw():
    if enabled:
        shader(edges)
    image(img, 0, 0)


def mouse_pressed():
    global enabled
    enabled = not enabled
    if not enabled:
        reset_shader()
run()
