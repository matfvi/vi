# Svaka dva brata imaju zajedničkog roditelja.
# Roditelj je stariji od deteta.
# Postoje braća.
# Ni jedna osoba nije starija od druge.

from z3 import *

B = BoolSort()
O = DeclareSort('Osoba')
braca = Function('braca', O, O, B)
roditelj = Function('roditelj', O, O, B)
stariji = Function('stariji', O, O, B)

x,y,z = Consts('x y z', O)
solver = Solver()
axioms = [
ForAll([x,y], Exists([z], Implies(braca(x,y), 
And(roditelj(z,x), roditelj(z,y))))),
ForAll([x,y], Implies(roditelj(x,y), stariji(x,y))),
Exists([x,y], braca(x,y))]

solver.add(ForAll([x,y], Not(stariji(x,y))))

if solver.check(axioms) == sat:
    print(solver.model())
else:
    print('unsat')









