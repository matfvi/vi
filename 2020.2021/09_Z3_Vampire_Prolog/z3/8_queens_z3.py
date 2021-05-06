from z3 import *


Q = [ Int('Q_%i' % (i + 1)) for i in range(8) ]

val_c = [ And(1 <= Q[i], Q[i] <= 8) for i in range(8) ]

col_c = [ Distinct(Q) ]

diag_c = [ If(i == j, 
              True, 
              And(Q[i] - Q[j] != i - j, Q[i] - Q[j] != j - i)) 
           for i in range(8) for j in range(i) ]

solve(val_c + col_c + diag_c)