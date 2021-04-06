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

    def eval(self, valuation):
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
            print(valuation)
            if self.eval(valuation) == False:
                return False
        return True

class Const(Formula):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def eval(self, valuation):
        return self.value
    
    def get_all_varaibles(self):
        return set()

    def __str__(self):
        return "{}".format(1 if self.value == True else 0)

class And(Formula):
    def __init__(self, components):
        super().__init__()
        self.components = components # lhs == components[0], rhs == components[1]
    
    def eval(self, valuation):
        return self.components[0].eval(valuation) and self.components[1].eval(valuation)

    def __str__(self):
        return f"({str(self.components[0])}) & ({str(self.components[1])})"

class Or(Formula):
    def __init__(self, components):
        super().__init__()
        self.components = components # lhs == components[0], rhs == components[1]

    def eval(self, valuation):
        return self.components[0].eval(valuation) or self.components[1].eval(valuation)

    def __str__(self):
        return f"({str(self.components[0])}) | ({str(self.components[1])})"

class Impl(Formula):
    def __init__(self, components):
        super().__init__()
        self.components = components # lhs == components[0], rhs == components[1]

    def eval(self, valuation):
        # A => B <=> ~A | B
        return not self.components[0].eval(valuation) or self.components[1].eval(valuation)

    def __str__(self):
        return f"({str(self.components[0])}) >> ({str(self.components[1])})"

class Eq(Formula):
    def __init__(self, components):
        super().__init__()
        self.components = components # lhs == components[0], rhs == components[1]

    def eval(self, valuation):
        return self.components[0].eval(valuation) == self.components[1].eval(valuation)

    def __str__(self):
        return f"({str(self.components[0])}) == ({str(self.components[1])})"

class Not(Formula):
    def __init__(self, components):
        super().__init__()
        self.components = components # lhs == components[0]

    def eval(self, valuation):
        return not self.components[0].eval(valuation)

    def __str__(self):
        return f"~({str(self.components[0])})"

class Var(Formula):
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def eval(self, valuation):
        return valuation[self.name]

    def get_all_varaibles(self):
        return set([self.name])

    def __str__(self):
        return self.name

def vars(names):
    names = [name.strip() for name in names.split(',')]
    return [Var(name) for name in names]

def transform_equal(formula):
    transformed_components = [transform_equal(A) for A in formula.components]
    result = formula
    result.components = transformed_components
    if isinstance(formula, Eq):
        A = transformed_components[0]
        B = transformed_components[1]
        result = (A >> B) & (B >> A)
    return result    


def transform_impl(formula):
    transformed_components = [transform_impl(A) for A in formula.components]
    result = formula
    result.components = transformed_components
    if isinstance(formula, Impl):
        A = transformed_components[0]
        B = transformed_components[1]
        result = ~A | B
    return result

def transform_demorgan(formula):
    transformed_components = [transform_demorgan(A) for A in formula.components]
    result = formula
    result.components = transformed_components
    if isinstance(formula, Not):
        # F = ~(H)
        H = transformed_components[0]
        if isinstance(H, And):
            A = H.components[0]
            B = H.components[1]
            result = ~A | ~B
        elif isinstance(H, Or):
            A = H.components[0]
            B = H.components[1]
            result = ~A & ~B
    return result

def transform_double_not(formula):
    transformed_components = [transform_double_not(A) for A in formula.components]
    result = formula
    result.components = transformed_components

    if isinstance(formula, Not) and isinstance(transformed_components[0], Not):
        A = transformed_components[0].components[0]
        result = A
    return result

def transform_distribute_or(formula):
    transformed_components = [transform_distribute_or(A) for A in formula.components]
    result = formula
    result.components = transformed_components

    if isinstance(formula, Or):
        if isinstance(transformed_components[1], And):
            A = transformed_components[0]
            B = transformed_components[1].components[0]
            C = transformed_components[1].components[1]
            result = (A | B) & (A | C)
        elif isinstance(transformed_components[0], And):
            A = transformed_components[1]
            B = transformed_components[0].components[0]
            C = transformed_components[0].components[1]
            result = (B | A) & (C | A)

    return result

def KNF(formula):
    formula = transform_equal(formula)
    formula = transform_impl(formula)
    formula = transform_demorgan(formula)
    formula = transform_double_not(formula)
    formula = transform_distribute_or(formula)
    return formula


if __name__ == '__main__':
    x,y,z = vars("x,y,z")
    
    formula = x | (~y)
    
    print(formula.is_tautology())
