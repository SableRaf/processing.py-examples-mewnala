# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Deform. 

A GLSL version of the oldschool 2D deformation effect, by Inigo Quilez.
Ported from the webGL version available in ShaderToy:
http://www.iquilezles.org/apps/shadertoy/
(Look for Deform under the Plane Deformations Presets)

"""
from mewnala import *

tex = None
deform = None


def setup():
    global tex, deform
    size(640, 360, P2D)
    texture_wrap(REPEAT)
    tex = load_image("tex1.jpg")
    deform = load_shader("deform.glsl")
    deform.set("resolution", float(width), float(height))


def draw():
    deform.set("time", millis() / 1000.0)
    deform.set("mouse", float(mouse_x), float(mouse_y))
    shader(deform)
    image(tex, 0, 0, width, height)
run()
