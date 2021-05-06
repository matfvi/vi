# Sorts

# SMT-LIB2 mali skup jednostavni tipova (Sorts): Bool, Int, Real, BitVec
# Array, Index, Elem, String, Seq S

# Novi tip (Domen): DeclareSort('S') 


# f = Function('f', Z, Z) kreira funkciju 'f': Z -> Z


from z3 import *

B = BoolSort()
Z = IntSort()
f = Function('f', B, Z)
g = Function('g', Z, B)
a = Bool('a')
solve(g(1+f(a)))


