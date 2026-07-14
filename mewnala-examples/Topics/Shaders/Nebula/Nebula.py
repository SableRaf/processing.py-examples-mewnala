# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Nebula. 

From CoffeeBreakStudios.com (CBS)
Ported from the webGL version in GLSL Sandbox:
http://glsl.heroku.com/e#3265.2
"""
from mewnala import *

nebula = None


def setup():
    global nebula
    size(640, 360, P2D)
    no_stroke()
    nebula = load_shader("nebula.glsl")
    nebula.set("resolution", float(width), float(height))


def draw():
    nebula.set("time", millis() / 500.0)
    shader(nebula)
    # This kind of raymarching effects are entirely implemented in the
    # fragment shader, they only need a quad covering the entire view
    # area so every pixel is pushed through the shader.
    rect(0, 0, width, height)
run()
