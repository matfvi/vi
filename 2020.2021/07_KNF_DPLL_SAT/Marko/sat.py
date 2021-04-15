import logic.formula as f
from itertools import product
import os
import timeit
import sys
import math
sys.setrecursionlimit(40000)


def minisat_solve(problem_name, problem_dimacs):
    with open(f'{problem_name}.cnf', 'w') as handle:
        handle.write(problem_dimacs.encoding)
    os.system(f'minisat {problem_name}.cnf {problem_name}_result.cnf')
    
    with open(f'{problem_name}_result.cnf', 'r') as result_file:
        lines = result_file.readlines()
    
    if lines[0].startswith('SAT'):
        print('SAT')
        var_values = {}
        for var in lines[1].split(' ')[:-1]:
            var_number = var.strip('-')
            var_name = problem_dimacs.number_to_varname[var_number]
            var_values[var_name] = 0 if var.startswith('-') else 1
        true_vars = list(filter(lambda v: v[1] == 1, var_values.items()))
        true_vars.sort()
        for var in true_vars:
            print(var)
    else:
        print('UNSAT')

def formula_init():
    p = f.Var('init')
    return p & ~~p

def solve(problem_name, formula):
    problem_knf = f.KNF(formula)
    problem = f.DIMACS(formula)

    with open(f'{problem_name}.cnf', 'w') as handle:
        handle.write(problem.encoding)
    os.system(f'minisat {problem_name}.cnf {problem_name}_result.cnf')
    
    with open(f'{problem_name}_result.cnf', 'r') as result_file:
        lines = result_file.readlines()
    
    if lines[0].startswith('SAT'):
        print('SAT')
        var_values = {}
        for var in lines[1].split(' ')[:-1]:
            var_number = var.strip('-')
            var_name = problem.number_to_varname[var_number]
            var_values[var_name] = 0 if var.startswith('-') else 1
        true_vars = list(filter(lambda v: v[1] == 1, var_values.items()))
        true_vars.sort()
        for var in true_vars:
            print(var)
    else:
        print('UNSAT')
    
    
    #print('\n\nIscrpna provera')
    #print(timeit.timeit(lambda: print(problem_knf.is_satisfiable()), number=1))

def n_dama(n):
    '''
    Rasporediti n dama na sahovsku tablu dimenzija NxN tako da se nikoje dve ne napadaju
    '''
    
    # u svakoj koloni barem jedan dama
    # formula = None
    # for j in range(n):
    #     clause = None
    #     for i in range(n):
    #         if clause is not None:
    #             clause |= f.Var(f'p{j}{i}')
    #         else:
    #             clause = f.Var(f'p{j}{i}')
    #     if formula is not None:
    #         formula &= clause
    #     else:
    #         formula = clause
    
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



def same_subsquare(r1, c1, r2, c2, n):
    square_len = int(math.sqrt(n))
    return (r1 // square_len, c1 // square_len) == (r2 // square_len, c2 // square_len)

def sudoku(initial_board):
    n = len(initial_board)
    formula = f.Var(f'init')
    # S_i_j_k polje i,j sadrzi broj k

    for row, col in product(range(n), repeat=2):
        number = initial_board[row][col]
        if number != 0:
            formula &= f.Var(f'S_{row}_{col}_{initial_board[row][col]}')

    # Svaki kvadrat mora imati broj između 1 i 9
    for row, col in product(range(n), repeat=2):
        clause = f.Const(False)
        for number in range(1, n+1):
            clause |= f.Var(f'S_{row}_{col}_{number}')
        formula &= clause
    

    for row1, col1, row2, col2, number in product(range(n), repeat=5):
        number += 1
        if (row1 == row2 and col1 < col2) \
        | (col1 == col2 and row1 < row2) \
        | same_subsquare(row1, col1, row2, col2, n):
            # S_i_j_n => ~S_i`_j`_n <=> ~S_i_j_n | ~S_i`_j`_n
            formula &= ~f.Var(f'S_{row1}_{col1}_{number}') | ~f.Var(f'S_{row2}_{col2}_{number}')

    solve('sudoku', formula)


def sudoku_cnf(initial_board):
    n = len(initial_board)
    cnf = f.CNF()
    # S_i_j_k polje i,j sadrzi broj k

    for row, col in product(range(n), repeat=2):
        number = initial_board[row][col]
        if number != 0:
            cnf.add_clause(f'S_{row}_{col}_{initial_board[row][col]}')

    # Svaki kvadrat mora imati broj između 1 i 9
    for row, col in product(range(n), repeat=2):
        clause = []
        for number in range(1, n+1):
            clause.append(f'S_{row}_{col}_{number}')
        cnf.add_clause(clause)
    

    for row1, col1, row2, col2, number in product(range(n), repeat=5):
        number += 1
        if (row1 == row2 and col1 < col2) \
        | (col1 == col2 and row1 < row2) \
        | same_subsquare(row1, col1, row2, col2, n):
            # S_i_j_n => ~S_i`_j`_n <=> ~S_i_j_n | ~S_i`_j`_n
            cnf.add_clause([f'S_{row1}_{col1}_{number}', f'~S_{row2}_{col2}_{number}'])

    minisat('sudoku', cnf.dimacs())



if __name__ == '__main__':
    #n_dama(4)
    
    board = [
        [0,6,0,0,8,0,4,2,0],
        [0,1,5,0,6,0,3,7,8],
        [0,0,0,4,0,0,0,6,0],
        [1,0,0,6,0,4,8,3,0],
        [3,0,6,0,1,0,7,0,5],
        [0,8,0,3,5,0,0,0,0],
        [8,3,0,9,4,0,0,0,0],
        [0,7,2,1,3,0,9,0,0],
        [0,0,9,0,2,0,6,1,0]    
    ]
    sudoku_cnf(board)
