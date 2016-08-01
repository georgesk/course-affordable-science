# display "objects" made with lines of star characters
import math

aspect_ratio=3.8
maxwidth=35
height=int(maxwidth/aspect_ratio)
halfball=[]
for l in range(height+1):
    width=maxwidth*math.sqrt(1-pow(l/height,2))
    halfball.append(" "*int((maxwidth-width)/2) + "*" + " "*int(width) + "*")
for l in range(height+1):
    print(halfball[height-l])
for l in range(height+1):
    print(halfball[l])
input("a ball ... it a key\n")

def head():
    for i in range(3):
        print("    ***")
def neck():
    for i in range(2):
        print("     *")
def shoulders():
    for i in range(1):
        print ("  *******")
def body():
    for i in range(4):
        print ("  * *** *")
def hands():
    for i in range(1):
        print("** ***** **")
def legs():
    for i in range(4):
        print("   *   *")
def feet():
    for i in range(1):
        print("  **   **")
def robot():
    head()
    neck()
    shoulders()
    body()
    hands()
    legs()
    feet()
robot()
input("a robot ...hit a key\n")
