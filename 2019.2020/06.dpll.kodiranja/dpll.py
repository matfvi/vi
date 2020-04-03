import copy

def zameni_literal(D, literal, value):
	n = len(D)

	D_copy = copy.copy(D)

	for i in range(n):
		D_copy[i] = [value if l == literal else l for l in D_copy[i]]
		D_copy[i] = ['-{}'.format(value) if l == -literal else l for l in D_copy[i]]

	return D_copy

# D = [[1, 2, -1], [1, 3, 2], [-1, 2, 3]]
# print(zameni_literal(D, 1, 'T'))

def DPLL(dimacs_formula):
	print('START:')
	print(D)
	return _DPLL(D, {})

def _DPLL(D, valuation):
	broj_klauza = len(D)

	if broj_klauza == 0:
		return True, valuation

	newD = []
	ima_promena = False
	for i in range(broj_klauza):
		klauza = D[i]
		m = len(klauza)

		if m == 0:
			return False, None

		for j in range(m):
			if klauza[j] == '-T':
				klauza[j] = 'F'
				ima_promena = True

			elif klauza[j] == '-F':
				klauza[j] = 'T'
				ima_promena = True

		newD.append(klauza)

	if ima_promena:
		D = copy.copy(newD)
		print('NEGATION SUBSTITUTION:')
		print(D)

	newD = []
	ima_promena = False
	for klauza in D:
		nova_klauza = []
		for l in klauza:
			if l != 'F':
				nova_klauza.append(l)
			else:
				ima_promena = True
		newD.append(nova_klauza)

	if ima_promena:
		D = copy.copy(newD)
		print('DELETE F')
		print(D)

		for klauza in D:
			if len(klauza) == 0:
				return False, None


	newD = []
	ima_promena = False
	for klauza in D:
		keep_klauza = True

		for l in klauza:
			if l == 'T':
				keep_klauza = False
				ima_promena = True
				break

			if -l in klauza:
				keep_klauza = False
				ima_promena = True
				break

		if keep_klauza:
			newD.append(klauza)


	if ima_promena:
		D = copy.copy(newD)
		print('TAUTOLOGY')
		print(D)
		return _DPLL(D, valuation)


	#-------
	newD = []
	ima_promena = False
	for klauza in D:
		m = len(klauza)

		if m == 1:
			ima_promena = True
			l = klauza[0]

			if l > 0:
				valuation[l] = True
				newD = zameni_literal(D, l, 'T')
			else:
				valuation[l] = False
				newD = zameni_literal(D, -l, 'F')

			break

	if ima_promena:
		D = copy.copy(newD)
		print('UNIT PROPAGATION')
		print(D)
		return _DPLL(D, valuation)


	#-----------
	newD = []
	ima_promena = False
	svi_literali = []
	for klauza in D:
		svi_literali += klauza

	razliciti_literali = list(set(svi_literali))
	for l in razliciti_literali:
		if -l not in svi_literali:
			ima_promena = True
			if l > 0:
				valuation[l] = True
				newD = zameni_literal(D, l, 'T')
			else:
				valuation[l] = False
				newD = zameni_literal(D, -l, 'F')
			break

	if ima_promena:
		D = copy.copy(newD)
		print('PURE LITERAL')
		print(D)
		return _DPLL(D, valuation)


	#-----------
	newD = []
	izabrani = razliciti_literali[0]
	valuation[izabrani] = True
	newD = zameni_literal(D, l, 'T')
	print('SPLIT[{}-->T]'.format(izabrani))
	print(newD)
	res, val = _DPLL(newD, valuation)

	if res:
		return True, val

	valuation[izabrani] = False
	newD = zameni_literal(D, l, 'F')
	print('SPLIT[{} --> F]'.format(izabrani))
	res, val = _DPLL(newD, valuation)

	if res:
		return True, val
	else:
		return False, None


D = [[1, 2], [-1, 2], [1, -2], [-1, -2]]
res, val = DPLL(D)
print(res, val)
