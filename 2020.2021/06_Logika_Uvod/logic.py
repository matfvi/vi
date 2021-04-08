import copy
from itertools import combinations
# x y z q
# 

def all_valuations(variables):
    for r in range(len(variables) + 1):
        for true_vars in combinations(variables, r):
            result = {x:False for x in variables}
            result.update({x: True for x in true_vars})
            yield result



class Formula:
    def __init__(self):
        self.components = []

    def __repr__(self):
        return str(self)

    def interpret(self, valuation):
        pass

    def __and__(self, rhs): # self & rhs => self.__and__(rhs)
        return And([self.copy(), rhs.copy()])
    
    def __or__(self, rhs): # self | rhs
        return Or([self.copy(), rhs.copy()])

    def __invert__(self): # ~self
        return Not([self.copy()])

    def __eq__(self, rhs):
        return Eq([self.copy(), rhs.copy()])

    def __rshift__(self, rhs):
        return Impl([self.copy(), rhs.copy()])

    def copy(self):
        return copy.deepcopy(self) 

    def get_all_varaibles(self):
        result = set()
        for c in self.components:
            result.update(c.get_all_varaibles())
        return result

    def is_tautology(self):
        variables = list(self.get_all_varaibles())
        for valuation in all_valuations(variables):
            if self.interpret(valuation) == False:
                return (False, valuation)
        return (True, None)

    def is_satisfiable(self):
        variables = list(self.get_all_varaibles())
        for valuation in all_valuations(variables):
            if self.interpret(valuation) == True:
                return True, valuation
        return False, None
    
    def is_valid(self):
        return self.is_tautology()
    
    def is_unsatisfiable(self):
        variables = list(self.get_all_varaibles())
        for valuation in all_valuations(variables):
            if self.interpret(valuation) == True:
                return False, valuation
        return True, None
    
    def is_falsifiable(self):
        variables = list(self.get_all_varaibles())
        for valuation in all_valuations(variables):
            if self.interpret(valuation) == False:
                return True, valuation
        return False, None



class Const(Formula):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def interpret(self, valuation):
        return self.value
    
    def get_all_varaibles(self):
        return set()

    def __str__(self):
        return "{}".format(1 if self.value == True else 0)

class And(Formula):
    def __init__(self, components):
        super().__init__()
        self.components = components # lhs == components[0], rhs == components[1]
    
    def interpret(self, valuation):
        return self.components[0].interpret(valuation) and self.components[1].interpret(valuation)

    def __str__(self):
        return f"({str(self.components[0])}) & ({str(self.components[1])})"

class Or(Formula):
    def __init__(self, components):
        super().__init__()
        self.components = components # lhs == components[0], rhs == components[1]

    def interpret(self, valuation):
        return self.components[0].interpret(valuation) or self.components[1].interpret(valuation)

    def __str__(self):
        return f"({str(self.components[0])}) | ({str(self.components[1])})"

class Impl(Formula):
    def __init__(self, components):
        super().__init__()
        self.components = components # lhs == components[0], rhs == components[1]

    def interpret(self, valuation):
        # A => B <=> ~A | B
        return not self.components[0].interpret(valuation) or self.components[1].interpret(valuation)

    def __str__(self):
        return f"({str(self.components[0])}) >> ({str(self.components[1])})"

class Eq(Formula):
    def __init__(self, components):
        super().__init__()
        self.components = components # lhs == components[0], rhs == components[1]

    def interpret(self, valuation):
        return self.components[0].interpret(valuation) == self.components[1].interpret(valuation)

    def __str__(self):
        return f"({str(self.components[0])}) == ({str(self.components[1])})"

class Not(Formula):
    def __init__(self, components):
        super().__init__()
        self.components = components # lhs == components[0]

    def interpret(self, valuation):
        return not self.components[0].interpret(valuation)

    def __str__(self):
        return f"~({str(self.components[0])})"

class Var(Formula):
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def interpret(self, valuation):
        return valuation[self.name]

    def get_all_varaibles(self):
        return set([self.name])

    def __str__(self):
        return self.name

def vars(names):
    names = [name.strip() for name in names.split(',')]
    return [Var(name) for name in names]

def primer_1():
    p,q,w,r,t = vars("p,q,w,r,t")
    formula = (p >> q) | ((w == r) & (r & ~t))
    valuation = {
        "p": True,
        "q": False,
        "w": True,
        "r": True,
        "t": False
    }
    print(formula)
    print(formula.interpret(valuation))

def primer_2():
    print('primer2')
    ana_je_zubar = Var("ana_je_zubar")
    formula = ana_je_zubar | ~ana_je_zubar
    print(formula)
    print("Tautology: ", formula.is_tautology())
    print("Satisfiable: ", formula.is_satisfiable())
    print("Falsifiable: ", formula.is_falsifiable())
    print("Unsatisfiable: ", formula.is_unsatisfiable())
    print('---------------------')

def primer_3():
    print('primer3')
    ana_je_zubar = Var("p,q")
    formula = p >> q
    print(formula)
    print("Tautology: ", formula.is_tautology())
    print("Satisfiable: ", formula.is_satisfiable())
    print("Falsifiable: ", formula.is_falsifiable())
    print("Unsatisfiable: ", formula.is_unsatisfiable())
    print('---------------------')

def primer_4():
    '''
    U igri mines dimenzija 2x3 dobijena je sledeca konfiguracija
    |1|A|C|
    |1|B|2|
    A,B,C su neotvorena polja, a brojevi oznacavaju broj mina u okolnim poljima.
    Zapisati u iskaznoj logici uslove koji moraju da vaze.
    '''
    print('primer4')
    A,B,C = vars("A,B,C")
    formula = (A | B) & (A | B) & ~(A & B) & ~(A & B) & (~A | ~B | ~C)\
    & ~(A & B) & (~A | ~B | ~C)\
    & ~(~A & ~B)\
    & ~(~A & ~C)\
    & ~(~B & ~C)
    print("Tautology: ", formula.is_tautology())
    print("Satisfiable: ", formula.is_satisfiable())
    print("Falsifiable: ", formula.is_falsifiable())
    print("Unsatisfiable: ", formula.is_unsatisfiable())
    print('---------------------')


def primer_5():
    '''
    Date su dve kutije A,B robot mora da stavi objekat u tacno jednu od njih.
    '''
    A,B = vars("A,B")
    formula = ~(A & B) & ~(~A & ~B) & (A | B)
    print(primer_5.__doc__)
    print(formula)
    print("Tautology: ", formula.is_tautology())
    print("Satisfiable: ", formula.is_satisfiable())
    print("Falsifiable: ", formula.is_falsifiable())
    print("Unsatisfiable: ", formula.is_unsatisfiable())
    print('---------------------')


def primer_6():
    ''' 
    |A|B|
    |C|D|
    Zapisati uslov da se u tabeli 2x2 sa poljima A,B,C,D moze postaviti tacno jedan zeton u 
    svakom redu
    '''
    A,B,C,D = vars("A,B,C,D")
    formula = (A | B) & (C | D) & ~(A & B) & ~(C & D)
    print(primer_6.__doc__)
    print(formula)
    print("Tautology: ", formula.is_tautology())
    print("Satisfiable: ", formula.is_satisfiable())
    print("Falsifiable: ", formula.is_falsifiable())
    print("Unsatisfiable: ", formula.is_unsatisfiable())
    print('---------------------')

def primer_7():
    '''
    U iskaznoj logici zapisati uslov da bitovi 3-bitnog polja moraju biti jednaki
    '''
    A,B,C = vars("A,B,C")
    formula = (A == B) & (B == C) & (A == C)
    print(primer_7.__doc__)

    print(formula)
    print("Tautology: ", formula.is_tautology())
    print("Satisfiable: ", formula.is_satisfiable())
    print("Falsifiable: ", formula.is_falsifiable())
    print("Unsatisfiable: ", formula.is_unsatisfiable())
    print('---------------------')

def primer_8():
    '''
    Dva dvobitna broja se sabiraju i daju rezultat 3.
    1+2
    2+1
    3+0
    0+3
        A B
        C D
        ---
        1 1
    '''
    A,B,C,D = vars("A,B,C,D")
    formula = (B | D) & ~(B & D) & (A | C) & ~(A & C)
    print(primer_8.__doc__)

    print(formula)
    print("Tautology: ", formula.is_tautology())
    print("Satisfiable: ", formula.is_satisfiable())
    print("Falsifiable: ", formula.is_falsifiable())
    print("Unsatisfiable: ", formula.is_unsatisfiable())
    print('---------------------')


def primer_9():
    '''
    U iskoznoj logici zapisati da je 4 bitna reprezentacija broja palindrom ali da 
    bitovi nisu jednaki
    '''
    A,B,C,D = vars("A,B,C,D")
    formula = (A == D) & (B == C) & ~(A == B & B == C & C == D)
    print(primer_9.__doc__)

    print(formula)
    print("Tautology: ", formula.is_tautology())
    print("Satisfiable: ", formula.is_satisfiable())
    print("Falsifiable: ", formula.is_falsifiable())
    print("Unsatisfiable: ", formula.is_unsatisfiable())
    print('---------------------')

def primer_10():
    '''
    Tri polja se boje crvenom ili plavom. 
    Ukoliko je prvo crveno, druga dva moraju biti iste boje.
    Ukoliko je drugo crveno, trece mora biti plavo.
    '''
    A,B,C = vars("A,B,C")
    formula = (A >> (B == C)) & (B >> ~C)
    print(primer_10.__doc__)

    print(formula)
    print("Tautology: ", formula.is_tautology())
    print("Satisfiable: ", formula.is_satisfiable())
    print("Falsifiable: ", formula.is_falsifiable())
    print("Unsatisfiable: ", formula.is_unsatisfiable())
    print('---------------------')

def primer_11():
    '''
        A
       / \\
      B - C
    Temana trougla A,B,C se boje sa dve boje, pri tome ni jedan par temena ne moze imati istu boju.
    '''

    A,B,C = vars("A,B,C")
    formula = ~(A == B) & ~(B == C) & ~(A == C)
    print(primer_11.__doc__)

    print(formula)
    print("Tautology: ", formula.is_tautology())
    print("Satisfiable: ", formula.is_satisfiable())
    print("Falsifiable: ", formula.is_falsifiable())
    print("Unsatisfiable: ", formula.is_unsatisfiable())
    print('---------------------')

def primer_12():
    '''
    |A|B|
    |C|D|
    Tabela 2x2 se boji crvenom ili plavom bojom.
    Ako je polje A ofarbano crvenom onda barem jedno od ostalih polja mora biti plavo.
    Ako je polje D ofarabno plavom onda barem dva ostala moraju biti crvena.
    Ne smeju sva polja biti ofarabana istom bojom.
    '''
    A,B,C,D = vars("A,B,C,D")
    formula = (A >> (~B | ~C | ~D)) & (~D >> ((A & B) | (B & C) | (A & C))) \
        & (A == B & B == C & C == D) 

    print(primer_12.__doc__)

    print(formula)
    print("Tautology: ", formula.is_tautology())
    print("Satisfiable: ", formula.is_satisfiable())
    print("Falsifiable: ", formula.is_falsifiable())
    print("Unsatisfiable: ", formula.is_unsatisfiable())
    print('---------------------')

if __name__ == '__main__':
    primer_8()
