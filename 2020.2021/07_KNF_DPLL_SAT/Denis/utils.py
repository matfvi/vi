import os

def mini_sat_solve(problem_name, problem_dimacs, number_to_var):
    # Otvaramo fajl za pisanje, upijemo dimacs string u njega, pokrecemo minisat iz konzole
    with open("{}.cnf".format(problem_name), "w") as f:
        f.write(problem_dimacs)
    os.system("minisat {}.cnf {}_result.cnf".format(problem_name, problem_name))

    # Citamo rezultat, vracamo niz promenljivih koje u valuaciji daju tacno ukoliko je zadovoljiv problem
    # U suprotnom vracamo praznu listu
    with open("{}_result.cnf".format(problem_name), "r") as f:
        lines = f.readlines()
        if lines[0].startswith("SAT"):
            tokeni = lines[1].split(" ")
            true_vars = []
            for token in tokeni:
                if not (token.strip().startswith("-") or token == "0\n"):
                    true_vars.append(number_to_var[int(token.strip())])
            return true_vars
    return []

