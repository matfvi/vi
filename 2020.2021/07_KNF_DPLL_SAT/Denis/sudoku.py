import cnf as f
from itertools import product
from utils import mini_sat_solve

def isti_podkvadrat(r1, c1, r2, c2, n):
    if r1 == r2 and c1==c2:
        return False
    block_size = int(n**0.5)
    block1 = (r1 // block_size, c1 // block_size)
    block2 = (r2 // block_size, c2 // block_size)
    return block1 == block2

def sudoku(board):
    # S_i_j_k = na (i,j) se nalazi broj k    
    n = len(board)
    print(n)
    cnf = f.CNF()

    # Ono sto je vec popunjeno ostaje tako, jednoclane klauze moraju se zadovoljiti
    for row, col in product(range(n), repeat=2):
        number = board[row][col]
        if number != 0:
            cnf.add_clause(["S_{}_{}_{}".format(row, col, number)])

    # Svako polje mora sadrzati neki broj izmedju 1 i 9
    for i, j in product(range(n), repeat=2):
        cnf.add_clause(["S_{}_{}_{}".format(i,j,number) for number in range(1, n+1) ])

    # Svako polje mora sadrzati najvise jedan broj
    for i, j in product(range(n), repeat=2):
        for num1, num2 in product(range(1, n+1), repeat=2):
            if num1 < num2:
                clause = ["-S_{}_{}_{}".format(i,j,num1), "-S_{}_{}_{}".format(i, j, num2)]
                cnf.add_clause(clause)

    # S_i_j_k => S_i'_j'_k za broj k, ne sme biti u istom redu ili podvkadratu
    for row1, col1, row2, col2, number in product(range(n), repeat=5):
        number += 1
        if (row1 == row2 and col1 < col2) or (col1 == col2 and row1 < row2) or isti_podkvadrat(row1, col1, row2, col2, n):
            cnf.add_clause(["-S_{}_{}_{}".format(row1, col1, number), "-S_{}_{}_{}".format(row2, col2, number)])

    true_vars = mini_sat_solve("sudoku", cnf.dimacs(), cnf.number_to_var)

    # Rekonstrukcija resenja na osnovu promenljivih
    for true_var in true_vars:
        tokens = true_var.split("_")
        i, j, number = (int(tokens[1]), int(tokens[2]), int(tokens[3]))
        board[i][j] = number
    # Prikaz resenog sudoku
    for row in board:
        print(row)

def main():
    sudoku_table = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 3, 6, 0, 0, 0, 0, 0],
                    [0, 7, 0, 0, 9, 0, 2, 0, 0],
                    [0, 5, 0, 0, 0, 7, 0, 0, 0],
                    [0, 0, 0, 0, 4, 5, 7, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 3, 0],
                    [0, 0, 1, 0, 0, 0, 0, 6, 8],
                    [0, 0, 8, 5, 0, 0, 0, 1, 0],
                    [0, 9, 0, 0, 0, 0, 4, 0, 0],
        ]
    for row in sudoku_table:
        print(row)
    sudoku(sudoku_table)
if __name__ == "__main__":
    main()
