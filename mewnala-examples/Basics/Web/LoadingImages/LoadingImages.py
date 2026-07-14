# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Loading Images. 
"""
from mewnala import *

def setup():
    size(640, 360)
    global img
    img = load_image("http://processing.org/img/processing-web.png")
    no_loop()


def draw():
    background(0)
    for i in range(5):
        image(img, 0, img.height * i)

run()
