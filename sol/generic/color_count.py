#!/usr/bin/python3

from PIL import Image
import sys

def help():
    print("""\
Usage: {} <path to an image>\
""".format(sys.argv[0]))
    sys.exit(0)
    return # useless isn't it?

try:
    im=Image.open(sys.argv[1])
except:
    help()

px=im.load()
w, h =im.size

colors={}
for x in range(w):
    for y in range(h):
        c=px[x,y]
        if c not in colors:
            colors[c]=1
        else:
            colors[c]+=1
print("The image {} contains {} different colors".format(sys.argv[1], len(colors)))
