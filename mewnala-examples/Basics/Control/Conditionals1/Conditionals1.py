# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Conditionals 1.

Conditions are like questions.
They allow a program to decide to take one action if 
the answer to a question is true or to do another action
if the answer to the question is false. 
The questions asked within a program are always logical
or relational statements. For example, if the variable 'i' is 
equal to zero then draw a line. 
"""
from mewnala import *

size(640, 360)
background(0)

for i in range(10, width, 10):
    # If 'i' divides by 20 with no remainder draw the first line
    # else draw the second line
    if i % 20 == 0:
        stroke(255)
        line(i, 80, i, height / 2)
    else:
        stroke(153)
        line(i, 20, i, 180)

run()
