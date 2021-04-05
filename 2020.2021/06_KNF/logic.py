from collections import defaultdict
from itertools import combinations
import copy

def all_valuations(variables):
    variables = copy.deepcopy(variables)
    for i in range(len(variables) + 1):
        for true_variables in combinations(variables, i):
            result = {x: False for x in variables}
            result.update({x: True for x in true_variables})
            yield result


class Formula:
    def __init__(self):
        self.components = []

    def get_all_variables(self):
        return set()

    def eval(self, valuation):
        pass
    
    def __repr__(self):
        return str(self)

    def __and__(self, other):
        return And([self.copy(), other.copy()])

    def __or__(self, rhs):
        return Or([self.copy(), rhs.copy()])
    
    def __invert__(self):
        return Not([self.copy()])

    def __eq__(self, rhs):
        return Eq([self.copy(), rhs.copy()])

    def __rshift__(self, rhs):
        return Impl([self.copy(), rhs.copy()])

    def is_tautology(self):
        return False

    def is_tautology(self):
        variables = list(self.get_all_variables())
        for valuation in all_valuations(variables):
            print(valuation)
            if self.eval(valuation) == False:
                return False
        return True
    
    def copy(self):
        return copy.deepcopy(self)


class Const(Formula):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def eval(self, valuation):
        return self.value

    def __str__(self):
        return "{}".format(1 if self.value == True else 0)

class Var(Formula):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def eval(self, valuation):
        return valuation[self.name]

    def get_all_variables(self):
        return set([self.name])

    def __str__(self):
        return self.name

class And(Formula):
    def __init__(self, components):
        super().__init__()
        self.components = components
    
    def eval(self, valuation):
        return self.components[0].eval(valuation) and self.components[1].eval(valuation)

    def __str__(self):
        return f"({str(self.components[0])}) & ({str(self.components[1])})"

    def get_all_variables(self):
        lhs_variables:set = self.components[0].get_all_variables()
        rhs_variables:set = self.components[1].get_all_variables()
        result = lhs_variables.union(rhs_variables)
        return result
    
class Or(Formula):
    def __init__(self, components):
        super().__init__()
        self.components = components
    
    def eval(self,valuation):
        return self.components[0].eval(valuation) or self.components[1].eval(valuation)

    def __str__(self):
        return f"({str(self.components[0])}) | ({str(self.components[1])})"

    def get_all_variables(self):
        lhs_variables:set = self.components[0].get_all_variables()
        rhs_variables:set = self.components[1].get_all_variables()
        result = lhs_variables.union(rhs_variables)
        return result

class Impl(Formula):
    def __init__(self, components):
        super().__init__()
        self.components = components
    
    def eval(self, valuation):
        return not self.components[0].eval(valuation) or self.components[1].eval(valuation)

    def __str__(self):
        return f"({str(self.components[0])}) => ({str(self.components[1])})"

    def get_all_variables(self):
        lhs_variables:set = self.components[0].get_all_variables()
        rhs_variables:set = self.components[1].get_all_variables()
        result = lhs_variables.union(rhs_variables)
        return result

class Eq(Formula):
    def __init__(self, components):
        super().__init__()
        self.components = components
    
    def eval(self, valuation):
        return self.components[0].eval(valuation) == self.components[1].eval(valuation)

    def __str__(self):
        return f"({str(self.components[0])}) == ({str(self.components[1])})"

    def get_all_variables(self):
        lhs_variables:set = self.components[0].get_all_variables()
        rhs_variables:set = self.components[1].get_all_variables()
        result = lhs_variables.union(rhs_variables)
        return result


class Not(Formula):
    def __init__(self, components):
        super().__init__()
        self.components = components

    def eval(self, valuation):
        return not self.components[0].eval(valuation)

    def __str__(self):
        return f"~({str(self.components[0])})"
    
    def get_all_variables(self):
        return self.components[0].get_all_variables()



def transform_equal(formula):
    transformed_components = [transform_equal(x) for x in formula.components]
    result = formula
    result.components = transformed_components
    if isinstance(formula,Eq):
        A = transformed_components[0]
        B = transformed_components[1]
        result = (A >> B) & (B >> A)
    return result

def transform_impl(formula):
    transformed_components = [transform_impl(x) for x in formula.components]
    result = formula
    result.components = transformed_components
    if isinstance(formula, Impl):
        A = transformed_components[0]
        B = transformed_components[1]
        result =  ~A | B
    return result

def transform_demorgan(formula):
    transformed_components = [transform_demorgan(x) for x in formula.components]
    result = formula
    result.components = transformed_components
    if isinstance(formula, Not):
        if isinstance(transformed_components[0], And):
            A = transformed_components[0]
            B = transformed_components[1]
            result = ~A | ~B
        elif isinstance(transformed_components[0], Or):
            A = transformed_components[0]
            B = transformed_components[1]
            result = ~A & ~B
    return result

def transform_double_not(formula):
    transformed_components = [transform_double_not(x) for x in formula.components]
    result = formula
    result.components = transformed_components
    if isinstance(formula, Not) and isinstance(transformed_components[0], Not):
        A = transformed_components[0].components[0]
        result = A
    return result

def transform_distribute_or(formula):
    transformed_components = [transform_distribute_or(x) for x in formula.components]
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

def vars(names):
    names = [name.strip() for name in names.split(',')]
    return [Var(name) for name in names]


if __name__ == '__main__':
    [x,y,z] = vars("x,y,z")
    formula = x | (y == z)
    
    print(KNF(formula))
    