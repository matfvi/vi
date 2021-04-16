import copy
from itertools import combinations

# x,y,z,w # 2 ^ n
def all_valuations(variables):
    # r=0,1,2,3,,,len(variables)
    for r in range(len(variables) + 1):
        for true_varibles in combinations(variables, r):
            result = {x: False for x in variables}
            result.update({x:True for x in true_varibles})
            yield result

class Formula:
    def __init__(self):
        self.components = []

    def interpret(self, valuation):
        pass

    def __repr__(self):
        return str(self)

    def __eq__(self, rhs): # self == rhs => self.__eq__(rhs)
        return Eq(self, rhs)

    def __and__(self, rhs): # self & rhs => self.__and__(rhs)
        return And(self, rhs)

    def __or__(self, rhs):
        return Or(self, rhs)

    def __rshift__(self, rhs):
        return Impl(self, rhs)

    def __invert__(self):
        return Not(self)
    
    def copy(self):
        return copy.deepcopy(self)

    def get_all_variables(self):
        result = set()
        for c in self.components:
            result.update(c.get_all_variables())
        return result

    def is_valid(self):
        variables = list(self.get_all_variables())
        for valuation in all_valuations(variables):
            if self.interpret(valuation) == False:
                return False, valuation
        return True, None

    def is_satisfiable(self):
        variables = list(self.get_all_variables())
        for valuation in all_valuations(variables):
            if self.interpret(valuation) == True:
                return True, valuation
        return False, None

    def is_contradictory(self):
        variables = list(self.get_all_variables())
        for valuation in all_valuations(variables):
            if self.interpret(valuation) == True:
                return False, valuation
        return True, None

    def is_falsifiable(self):
        variables = list(self.get_all_variables())
        for valuation in all_valuations(variables):
            if self.interpret(valuation) == False:
                return True, valuation
        return False, None

    def all_valuations_that_interpret_to_true(self):
        result = []
        variables = list(self.get_all_variables())
        for valuation in all_valuations(variables):
            if self.interpret(valuation) == True:
                result.append(valuation)
        return result


class Var(Formula):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def interpret(self, valuation):
        return valuation[self.name]

    def get_all_variables(self):
        return set([self.name]) # prom => {'p', 'r', 'o', 'm'}

    def __str__(self):
        return self.name

    def _dimacs(self, variables):
        if self.name in variables:
            return variables[self.name]
        else:
            variables[self.name] = str(len(variables) + 1)
            return variables[self.name]

class Const(Formula):
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def interpret(self, valuation):
        return self.value

    def __str__(self):
        return "{}".format(1 if self.value else 0)
    
    def _dimacs(self, variables):
        return ''

class And(Formula):
    def __init__(self, lhs, rhs):
        super().__init__()
        self.components = [lhs, rhs]

    def interpret(self, valuation):
        return self.components[0].interpret(valuation) and self.components[1].interpret(valuation)

    def __str__(self):
        return f"({self.components[0]}) & ({self.components[1]})"

    def _dimacs(self, variables):
        result = self.components[0]._dimacs(variables)
        result += f' 0\n{self.components[1]._dimacs(variables)}'
        return result


class Or(Formula):
    def __init__(self, lhs, rhs):
        super().__init__()
        self.components = [lhs, rhs]

    def interpret(self, valuation):
        return self.components[0].interpret(valuation) or self.components[1].interpret(valuation)

    def __str__(self):
        return f"({self.components[0]}) | ({self.components[1]})"

    def _dimacs(self, variables):
        result = self.components[0]._dimacs(variables)
        result += f' {self.components[1]._dimacs(variables)}'
        return result

class Impl(Formula):
    def __init__(self, lhs, rhs):
        super().__init__()
        self.components = [lhs, rhs]

    def interpret(self, valuation):
        # p => q <=> not p ili q
        return not self.components[0].interpret(valuation) or self.components[1].interpret(valuation)

    def __str__(self):
        return f"({self.components[0]}) >> ({self.components[1]})"

    def _dimacs(self, variables):
        raise ValueError('not a knf')

class Eq(Formula):
    def __init__(self, lhs, rhs):
        super().__init__()
        self.components = [lhs, rhs]
    
    def interpret(self, valuation):
        return self.components[0].interpret(valuation) == self.components[1].interpret(valuation)

    def __str__(self):
        return f"({self.components[0]}) == ({self.components[1]})"

    def _dimacs(self, variables):
        raise ValueError('Not KNF')

class Not(Formula):
    def __init__(self, op):
        super().__init__()
        self.components = [op]

    def interpret(self, valuation):
        return not self.components[0].interpret(valuation)

    def __str__(self):
        return f"~({self.components[0]})"

    def _dimacs(self, variables):
        return f'-{self.components[0]._dimacs(variables)}'



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
            A = transformed_components[0].components[0]
            B = transformed_components[0].components[1]
            result = ~A | ~B
        elif isinstance(transformed_components[0], Or):
            A = transformed_components[0].components[0]
            B = transformed_components[0].components[1]
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
    return [Var(name.strip()) for name in names.split(',')]


class DimacsFormat:
    def __init__(self, encoding, variables):
        self.encoding = encoding
        self.varname_to_number = variables
        self.number_to_varname = {int(v):k for k,v in self.varname_to_number.items()}

def DIMACS(formula):
    variables = {}
    encoding = formula._dimacs(variables)
    encoding += ' 0'
    number_of_clauses = encoding.count('\n') + 1
    header = f'p cnf {len(variables)} {number_of_clauses}\n'
    return DimacsFormat(header + encoding, variables) 




