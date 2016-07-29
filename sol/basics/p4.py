import expeyes.eyesj as ej
from pylab import *

p=ej.open()
# shortest time gap between two consecutive measurements
# according to the programming guide, it is 4 µs.

t, v = p.capture(1, 1800, 4)
plot(t, v)
show()
