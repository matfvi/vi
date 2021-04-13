import formula as f
from itertools import product
import os
import timeit
import sys

sys.setrecursionlimit(10000)

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

    print('Iscrpna provera')
    sat, solution = problem_knf.is_satisfiable()
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
    n_dama(4)