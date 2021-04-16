class CNF():
    """
    Klasa koju koristimo za cuvanje formule u knf obliku, tj. kao niz klauza
    Jedna klauza je niz stringova, gde je string promenljiva
    """
    def __init__(self):
        self.clauses = []
        self.var_name_to_number = {}
        self.number_to_var = {}
        self.number = 1

    def add_clause(self, clause):
        for literal in clause:
            var_name = literal.strip("-")
            if var_name not in self.var_name_to_number:
                self.var_name_to_number[var_name] = self.number
                self.number_to_var[self.number] = var_name
                self.number += 1
        self.clauses.append(clause)



    def dimacs(self):
        """
        Funkcija koja generise izlaz u dimacs formatu
        Svaku promenljivu slikamo u jedinstven broj
        """
        result = "p cnf {} {}\n".format(len(self.var_name_to_number), len(self.clauses))
        for clause in self.clauses:
            for literal in clause:
                var_name = literal.strip("-")
                if literal[0] == '-':
                    result += '-'
                result += "{} ".format(self.var_name_to_number[var_name])
            result += "0\n"
        return result
