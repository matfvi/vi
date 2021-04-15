import cnf as f
from itertools import product
from utils import mini_sat_solve

def n_dama_cnf(n):
    cnf = f.CNF()

    # U svakoj vrsti mora biti makar jedna dama
    for j in range(n):
        clause = ["p{}{}".format(j,i) for i in range(n)]
        cnf.add_clause(clause)

    # U svakoj vrsto najvise jedna dama
    for k in range(n):
        for i in range(n-1):
            for j in range(i+1, n):
                cnf.add_clause(["-p{}{}".format(k,i), "-p{}{}".format(k,j)])

    # U svakoj koloni najvise jedna dama
    for k in range(n):
        for i in range(n-1):
            for j in range(i+1, n):
                cnf.add_clause(["-p{}{}".format(i,k), "-p{}{}".format(j,k)])

    # Dame se ne napadaju po dijagonali
    for i,j,k,l in product(range(n), repeat=4):
        if k > i and abs(k - i) == abs(l - j):
            cnf.add_clause(["-p{}{}".format(i,j),"-p{}{}".format(k,l)])

    true_vars = mini_sat_solve("n_dama", cnf.dimacs(), cnf.number_to_var)

    board = [["." for i in range(n)] for j in range(n)]

    # Prikaz resenja
    for true_var in true_vars:
        (i, j) = (int(true_var[1]), int(true_var[2]))
        board[i][j] = "D"

    for row in board:
        print(row)

def main():
    n_dama_cnf(8)

if __name__ == "__main__":
    main()
