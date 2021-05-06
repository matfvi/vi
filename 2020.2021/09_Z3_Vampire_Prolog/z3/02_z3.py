from z3 import *

x = Real('x')
y = Real('y')
z = Real('z')

s = Solver()
s.add(x + 5*y - 3*z == 4,
      -x + y + z == 3,
      2*x + y - z == 1)

if s.check() == sat:
    print(s.model())