import formula as f
from itertools import product
import os
import timeit
import sys

# Zbog ugenjždenih Or i And i velikog broja promenljivih
# moramo povećati broj rekuriznih poziva funkcija 
sys.setrecursionlimit(10000)

def minisat_solve(problem_name, problem_dimacs, number_to_var):
    with open(f'{problem_name}.cnf', 'w') as handle:
        handle.write(problem_dimacs)
    os.system(f'minisat {problem_name}.cnf {problem_name}_result.cnf')

    with open(f'{problem_name}_result.cnf', 'r') as result_file:
        lines = result_file.readlines()

    if lines[0].startswith('SAT'):
        print('SAT')
        var_values = {}
        for var in lines[1].split(' ')[:-1]:
            var_number = int(var.strip('-'))
            var_name = number_to_var[var_number]
            var_values[var_name] = 0 if var.startswith('-') else 1
        true_vars = list(filter(lambda v: v[1] == 1, var_values.items()))
        true_vars.sort()
        for var in true_vars:
            print(var)
    else:
        print('UNSAT')

def n_dama(n):
    '''
    Rasporediti n dama na sahovsku tablu dimenzija NxN tako da se nikoje dve ne napadaju
    '''
    formula = f.Var('init')
    for j in range(n):
        clause = f.Const(False)
        for i in range(n):
            clause |= f.Var(f'p{j}{i}')   
        formula &= clause
       

    # u svakoj koloni najvise jedna dama
    for k in range(n):
        for i in range(n-1):
            for j in range(i+1, n):
                formula &= (~f.Var(f'p{k}{i}') | ~f.Var(f'p{k}{j}'))
    
    # u svakoj vrsti najvise jedna dama
    for k in range(n):
        for i in range(n-1):
            for j in range(i+1, n):
                formula &= (~f.Var(f'p{i}{k}') | ~f.Var(f'p{j}{k}'))
    
    # nema dame koje se napadaju dijagonalno
    for i,j,k,l in product(range(n), repeat=4):
        if k > i and abs(k - i) == abs(l - j):
            formula &= (~f.Var(f'p{i}{j}') | ~f.Var(f'p{k}{l}'))



    problem_knf = f.KNF(formula)
    problem_dimacs = f.DIMACS(problem_knf)

    minisat_solve(f'{n}_queens_formula_class.cnf', problem_dimacs.encoding, problem_dimacs.number_to_varname)


    print('Iscrpna provera')
    sat, solution = formula.is_satisfiable()
    if sat:
        print('SAT')
        true_vars = []
        for var, value in solution.items():
            if value == True:
                true_vars.append((var, value))
        true_vars.sort()
        for true_var in true_vars:
            print(true_var)

if __name__ == '__main__':
    n = 4 # 3,4,5,6,7,8,9... probati
    n_dama(6)