# U iskaznoj logici zapisati uslov da je 4-bitna reprezentacija broja
# palindrom, ali da nisu svi bitovi isti.

from z3 import *

A, B, C, D = Bools('A B C D')
s = Solver()
s.add(A == D, B == C, Not(And(A == B, B == C, C == D)))

print(s.check())
print(s.model())
