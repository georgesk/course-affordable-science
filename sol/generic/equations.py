#!/usr/bin/python3

from math import sqrt

print ("solutions of equations up to the second degree")
print ("The equation is: a*x^2 + b*x + c = 0")
print ("  if a is zero, the degree of the equation is lower than two.")
print ("  please give the coefficients:")
a=float(input("    a= "))
b=float(input("    b= "))
c=float(input("    c= "))


if a == 0: # degree one
    print("the root of {}*x + {} = 0 is: {}".format(b,c, -c/b))
else:
    delta=b**2-4*a*c
    if delta > 0:
        print ("the roots of {}*x^2 + {}*x + {} = 0 are:".format(a,b,c))
        print ("    {}".format((-b+sqrt(delta))/2/a))
        print ("    {}".format((-b-sqrt(delta))/2/a))
    elif delta==0:
        print ("the double root of {}*x^2 + {}*x + {} = 0 is:".format(a,b,c))
        print ("    {}".format(-b/2/a))
    else:
        print ("the roots of {}*x^2 + {}*x + {} = 0 are:".format(a,b,c))
        print ("    {}".format((-b+1j*sqrt(-delta))/2/a))
        print ("    {}".format((-b-1j*sqrt(-delta))/2/a))
