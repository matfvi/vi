'''
    Uporediti formulaciju uslova problema preko klase Formula i klase CNF.
    Za malo veci broj promenljivih i uslova klasa Formula zbog ugnjezdenih
    Or i And komponenti postane neprakticna.


    Ovaj primer treba da dostigne maksimalan broj rekruzivnih poziva
    za svodjenje na KNF rekruzivnih pozivima funkcije KNF.

'''

from itertools import product
import formula as f
import os
import sys


sys.setrecursionlimit(10000)

def same_subsquare(r1, c1, r2, c2, n):
    block_size = int(n**.5)
    block_1 = (r1 // block_size, c1 // block_size)
    block_2 = (r2 // block_size, c2 // block_size)
    return block_1 == block_2


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
        | ((row1, col1) != (row2, col2) and same_subsquare(row1, col1, row2, col2, n)):
            # S_i_j_n => ~S_i`_j`_n <=> ~S_i_j_n | ~S_i`_j`_n
            formula &= ~f.Var(f'S_{row1}_{col1}_{number}') | ~f.Var(f'S_{row2}_{col2}_{number}')

    problem_knf = f.KNF(formula)
    problem_dimacs = f.DIMACS(formula)
    minisat_solve(f'sudoku', problem_dimacs.encoding, problem_dimacs.number_to_varname)

    # formula je vec u KNF.
    # 

    # Dostize maksimalna broj rekruzivnih poziva zbog mnogo ugenjezedenih komponenti
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

if __name__ == '__main__':
    hardest_sudoku = [
        [8,0,0,0,0,0,0,0,0],
        [0,0,3,6,0,0,0,0,0],
        [0,7,0,0,9,0,2,0,0],
        [0,5,0,0,0,7,0,0,0],
        [0,0,0,0,4,5,7,0,0],
        [0,0,0,1,0,0,0,3,0],
        [0,0,1,0,0,0,0,6,8],
        [0,0,8,5,0,0,0,1,0],
        [0,9,0,0,0,0,4,0,0]
    ]
    sudoku(hardest_sudoku)