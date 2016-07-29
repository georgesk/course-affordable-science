import expeyes.eyesj as ej
from pylab import *

p=ej.open()
# make more measurements, with the same time gap
# this willlast longer!
#
# t, v = p.capture(1, 1000, 2000)

t, v = p.capture(1, 1800, 2000)
plot(t, v)
show()
