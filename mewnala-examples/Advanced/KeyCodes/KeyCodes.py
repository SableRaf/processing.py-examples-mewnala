# AUTO-CONVERTED from Processing Python Mode to mewnala by convert_to_mewnala.py.
# This is a first-pass mechanical conversion and has NOT been tested — review and run before relying on it.
from mewnala import *
from collections import defaultdict
from java.awt.event import KeyEvent
from java.lang.reflect import Modifier

key_names = defaultdict(lambda: 'UNKNOWN')
for f in KeyEvent.get_declared_fields():
    if Modifier.is_static(f.get_modifiers()):
        name = f.get_name()
        if name.startswith("VK_"):
            key_names[f.get_int(None)] = name[3:]


def draw():
    pass


def key_pressed():
    if key == CODED:
        print key_names[key_code]
    else:
        print "key " + key

run()
