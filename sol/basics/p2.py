import expeyes.eyesj as ej
from pylab import *

p=ej.open()
# make more measurements in the same total time
# 1000 * 2000 = 2 milions microseconds = 2 seconds
# 1600 * 1250 = the same total time
#
# t, v = p.capture(1, 1000, 2000)

t, v = p.capture(1, 1600, 1250)
plot(t, v)
show()
