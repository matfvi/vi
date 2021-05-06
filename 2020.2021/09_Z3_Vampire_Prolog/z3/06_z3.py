# Dve nemimoilazne prave se seku ili su paralelene.
# Prave koje se seku leže u istoj ravni.
# Prave koje su paralelene leže u istoj ravni.
# Dve nemimoilazne prave leže u istoj ravni.

from z3 import *

B = BoolSort()
P = DeclareSort('Prave')
m = Function('m', P, P, B)
s = Function('s', P, P, B)
p = Function('p', P, P, B)
r = Function('r', P, P, B)

x,y = Consts('x y', P)
solver = Solver()
axioms = [
ForAll([x,y], Implies(m(x,y), Or(s(x,y), p(x,y)))),
ForAll([x,y], Implies(s(x,y), r(x,y))),
ForAll([x,y], Implies(p(x,y), r(x,y)))]

solver.add(ForAll([x,y], Implies(m(x,y), r(x,y))))

if solver.check(axioms) == sat:
    print(solver.model())









