import cnf as f
from itertools import product
import os
import sys

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
            var_number = int(var)
            var_name = number_to_var[abs(var_number)]
            var_values[var_name] = var_number > 0
        true_vars = list(filter(lambda v: v[1] == 1, var_values.items()))
        true_vars.sort()
        for var in true_vars:
            print(var)
    else:
        print('UNSAT')

def same_subsquare(r1, c1, r2, c2, n):
    block_size = int(n**.5)
    block_1 = (r1 // block_size, c1 // block_size)
    block_2 = (r2 // block_size, c2 // block_size)
    return block_1 == block_2

def sudoku_cnf(initial_board):
    n = len(initial_board)
    print(n)
    cnf = f.CNF()
    # S_i_j_k polje i,j sadrzi broj k

    for row, col in product(range(n), repeat=2):
        number = initial_board[row][col]
        if number != 0:
            cnf.add_clause([f'S_{row}_{col}_{number}'])

    # Svako polje mora imati broj između 1 i 9
    for row, col in product(range(n), repeat=2):
        clause = [f'S_{row}_{col}_{number}' for number in range(1, n+1)]
        cnf.add_clause(clause)
    
    # jedno polje ne moze sadrzati dva razlicita polja
    for row, col in product(range(n), repeat=2):
        for num1, num2 in product(range(1, n+1), repeat=2):
            if num1 != num2:
                # ~(S_i_j_k & S_i_j_k`)
                clause = [f'-S_{row}_{col}_{num1}', f'-S_{row}_{col}_{num2}']
                cnf.add_clause(clause)

    # S_i_j_k => -S_i`_j`_k gde (i,j)!=(i`,j`) ali je u istom redu, koloni, ili bloku kao i,j
    for row1, col1, row2, col2, number in product(range(n), repeat=5):
        number += 1
        if (row1 == row2 and col1 < col2) \
        | (col1 == col2 and row1 < row2) \
        | ((row1, col1) != (row2, col2) and same_subsquare(row1, col1, row2, col2, n)):
            # S_i_j_n => ~S_i`_j`_n <=> ~S_i_j_n | ~S_i`_j`_n
            cnf.add_clause([f'-S_{row1}_{col1}_{number}', f'-S_{row2}_{col2}_{number}'])

    minisat_solve('sudoku', cnf.dimacs(), cnf.number_to_var_name)

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

    sudoku_cnf(hardest_sudoku)