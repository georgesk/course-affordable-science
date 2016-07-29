import expeyes.eyesj as ej
from pylab import *

p=ej.open()
t, v = p.capture(1, 1000, 2000)

plot(t, v)
show()
