# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Iteration.

Iteration with a "for" structure to construct repetitive forms. 
"""
from mewnala import *

num = 14

size(640, 360)
background(102)
no_stroke()

# Draw gray bars
fill(255)
y = 60
for i in range(num / 3):
    rect(50, y, 475, 10)
    y += 20

# Gray bars
fill(51)
y = 40
for i in range(num):
    rect(405, y, 30, 10)
    y += 20

y = 50
for i in range(num):
    rect(425, y, 30, 10)
    y += 20

# Thin lines
y = 45
fill(0)
for i in range(num - 1):
    rect(120, y, 40, 1)
    y += 20

run()
