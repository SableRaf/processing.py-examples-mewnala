# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
"""
Conditionals 2. 
 
We extend the language of conditionals from the previous
example by adding the keyword "else". This allows conditionals 
to ask two or more sequential questions, each with a different
action. 
"""
from mewnala import *

size(640, 360)
background(0)

for i in range(2, width - 2, 2):
    # If 'i' divides by 20 with no remainder
    if i % 20 == 0:
        stroke(255)
        line(i, 80, i, height / 2)
    # If 'i' divides by 10 with no remainder
    elif i % 10 == 0:
        stroke(153)
        line(i, 20, i, 180)
    # If neither of the above two conditions are met
    # then draw this line
    else:
        stroke(102)
        line(i, height / 2, i, height - 20)

run()
