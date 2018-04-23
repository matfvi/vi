
valuation = {}

def getClauses(formulaCNF, clauses):
	if not isinstance(formulaCNF, And):
		clauses.append(formulaCNF)
		return clauses
	else:
		getClauses(formulaCNF.op1, clauses)
		getClauses(formulaCNF.op2, clauses)
		return clauses

def getLiterals(clause, literals):
	if not isinstance(clause, Or):
		if isinstance(clause, Not):
			literals.append(-(ord(clause.op1.letter) - ord('o')))
		else:
			literals.append(ord(clause.letter) - ord('o'))
	else:
		getLiterals(clause.op1, literals)
		getLiterals(clause.op2, literals)
		return literals


def dimacs(formulaCNF):
	
	clauses = getClauses(formulaCNF, [])

	body = ""

	usedLiterals = {}

	for clause in clauses:
		literals = getLiterals(clause, [])
		for literal in literals:
			usedLiterals[abs(literal)] = 1
			body += str(literal) + " "
		body += "0\n"

	numClauses = len(clauses)
	numLiterals = len(usedLiterals)

	header = "p cnf %d %d\n" % (numLiterals, numClauses)

	return header + body

def CNF(formula):
	if isinstance(formula, T) or isinstance(formula, F) or isinstance(formula, Letter):
		return formula

	if isinstance(formula, Eq):
		return And(
			   CNF(Imp(formula.op1, formula.op2)),
			   CNF(Imp(formula.op2, formula.op1))
			  )

	if isinstance(formula, Imp):
		return CNF(Or(CNF(Not(formula.op1)), CNF(formula.op2)))

	
	if isinstance(formula, Not):
		op = CNF(formula.op1)

		if isinstance(op, Or):
			return CNF(And(CNF(Not(op.op1)),CNF(Not(op.op2))))

		if isinstance(op, And):
			return CNF(Or(CNF(Not(op.op1)),CNF(Not(op.op2))))

		if isinstance(op, Not):
			return CNF(op.op1)		

		return Not(op)

	if isinstance(formula, Or):
		A = CNF(formula.op1)
		B = CNF(formula.op2)

		if isinstance(A, And):
			return CNF(And(Or(A.op1, B),Or(A.op2, B)))
		
		if isinstance(B, And):
			return CNF(And(Or(A, B.op1),Or(A, B.op2)))

		return Or(A,B)

	if isinstance(formula, And):
		return And(CNF(formula.op1), CNF(formula.op2))

class Formula:
	def __init__(self):
		pass


class T(Formula):
	def __str__(self):
		return 'T'

	def interpretation(self):
		return True


class F(Formula):
	def __str__(self):
		return 'F'

	def interpretation(self):
		return False

class Letter(Formula):
	def __init__(self, letter):
		self.letter = letter

	def __str__(self):
		return str(self.letter)

	def interpretation(self):
		return valuation[self.letter]

class Not(Formula):
	def __init__(self, op1):
		self.op1 = op1

	def __str__(self):
		return "~(%s)" % self.op1.__str__()

	def interpretation(self):
		return not self.op1.interpretation()

class And(Formula):
	def __init__(self, op1, op2):
		self.op1 = op1
		self.op2 = op2

	def __str__(self):
		return "(%s & %s)" % (self.op1.__str__(), self.op2.__str__())

	def interpretation(self):
		return self.op1.interpretation() and self.op2.interpretation()

class Or(Formula):
	def __init__(self, op1, op2):
		self.op1 = op1
		self.op2 = op2

	def __str__(self):
		return "(%s | %s)" % (self.op1.__str__(), self.op2.__str__())

	def interpretation(self):
		return self.op1.interpretation() or self.op2.interpretation()

class Imp(Formula):
	def __init__(self, op1, op2):
		self.op1 = op1
		self.op2 = op2
	
	def __str__(self):
		return "(%s => %s)" % (self.op1.__str__(), self.op2.__str__())

	
	def interpretation(self):
		return not self.op1.interpretation() or self.op2.interpretation()


class Eq(Formula):
	def __init__(self, op1, op2):
		self.op1 = op1
		self.op2 = op2

	def __str__(self):
		return "(%s <=> %s)" % (self.op1.__str__(), self.op2.__str__())

	
	def interpretation(self):
		return self.op1.interpretation() == self.op2.interpretation()


def SAT(formula, letters, i):
	if i == len(letters):
		if formula.interpretation() == True:
			return valuation
		else:
			return None

	valuation[letters[i]] = False
	res = SAT(formula, letters, i + 1)

	if res != None:
		return res

	valuation[letters[i]] = True
	res = SAT(formula, letters, i + 1)

	if res != None:
		return res


def CreateTable(formula, letters, i):
	if i == len(letters):
		row = ""
		for (k,v) in valuation.items():
			row += str(int(v)) + " " 
		print("%s %s" % (row, str(int(formula.interpretation()))))
		return

	valuation[letters[i]] = False
	CreateTable(formula, letters, i + 1)

	valuation[letters[i]] = True
	CreateTable(formula, letters, i + 1)


F00 = T()
F01 = F()
F02 = Letter('p')
F0 = And(Letter('p'),Not(Letter('p')))
F1 = Or(Letter('p'),Not(Letter('p')))
F2 = Imp(Not(Letter('p')),And(Letter('q'),Letter('r')))
F3 = Eq(And(Not(Letter('q')),Letter('r')),Or(Imp(T(),Letter('s')), Letter('p')))
F5 = Not(Eq(Letter('p'), Letter('q')))
F4 = Eq(Eq(F0,F1),F5)
F6 = Eq(Letter('p'),Letter('q'))
F7 = Eq(Letter('q'),Letter('r'))
F8 = Eq(Letter('p'),Letter('r'))
F9 = And(And(F6, F7),F8)
# print(F4)
# print(CNF(F4))

print(F9)
F9CNF = CNF(F9)

print(SAT(F9CNF, ['p','q','r'], 0))

print('p q r  f')
CreateTable(F9CNF,['p','q','r'], 0)

izlaz = open('input.cnf','w')
izlaz.write(dimacs(F9CNF))

#print(F4)
#F4CNF = CNF(F4)
#print(F4CNF)
#print(getClauses(F4CNF, []))

# print(SAT(F5, ['p','q'], 0))
# print(CNF(F5))

