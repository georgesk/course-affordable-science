# interactive game

import random, sys

n=random.randint(1,99)
OK=False

print("""\
I have chosen a random integer between 1 and 99.
Can you guess it in less than seven tries?

After each try I reply whether your guess is
accurate, or too small, or too high.
""")

for guess in range(1,8):
    m= int(input("Your guess #{}: ".format(guess)))
    if m < n:
        print("{} is too small".format(m))
    elif m > n:
        print("{} is too high".format(m))
    else:
        OK=True
        break
if OK:
    print("Right guess! congratulations.")
else:
    print("Too late: the right value was {}".format(n))
