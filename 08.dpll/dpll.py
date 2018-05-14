#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import copy

valuation = {}

def DPLL(D):
    # Ako je D prazan onda vrati DA.
    if len(D) == 0: return True

    # zameni sve literale ¬⊥ sa ⊤ i zameni sve literale ¬⊤ sa ⊥ ;
    # obriši sve literale jednake ⊥ ;
    # ako 𝐷  sadrži praznu klauzu onda vrati NE;
    new_D = []
    for clause in D:
        new_clause = []
        for i in range(len(clause)):
            keep_literal = True
            if clause[i] == '-T': clause[i] = 'F'
            if clause[i] == '-F': clause[i] = 'T'
            if clause[i] == 'F': keep_literal = False
            if keep_literal: new_clause.append(clause[i])

        # ako je klauza iz D prazna onda vrati NE
        if len(new_clause) == 0: return False
        new_D.append(new_clause)
    D = new_D
    new_D = []

    print("{PREPROCESSING}")
    print(D)

    # -------------------------------------------------------------------------
    # {Korak tautology:}
    # ako neka klauza 𝐶 𝑖 sadrži ⊤ ili sadrži neki literal i njegovu negaciju onda
    # vrati vrednost koju vraća DPLL(𝐷 ∖ 𝐶 𝑖);
    # -------------------------------------------------------------------------
    has_changes = False
    for i in range(len(D)):
        keep_clause = True

        if 'T' in D[i]:
            has_changes = True
            continue

        for literal in D[i]:
            if -literal in D[i]:
                keep_clause = False
                has_changes = True

        if keep_clause:
            new_D.append(D[i])

    D = new_D
    if has_changes:
        print("{TAUTHOLOGY}")
        print(D)
        res = DPLL(D)
        if res: return True


    # -------------------------------------------------------------------------
    # {Korak unit propagation:}
    # -------------------------------------------------------------------------
    has_changes = False

    for i in range(len(D)):
        # ako neka klauza je jedinična
        if len(D[i]) == 1:
            lit = D[i][0]   # uzimamo njen literal

            # ako je klauza jednaka nekom iskaznom slovu 𝑝 onda
            # vrati vrednost koju vraća DPLL(𝐷 [𝑝 ↦→ ⊤ ]);
            if lit > 0:
                for clause in D:
                    for j in range(len(clause)):
                        if clause[j] == lit:
                            has_changes = True
                            valuation[abs(lit)] = True
                            clause[j] = 'T'
                        elif clause[j] == -lit:
                            has_changes = True
                            clause[j] = 'F'
            # ako neka klauza jednaka ¬𝑝 , za neko iskazno slovo 𝑝 onda
            # vrati vrednost koju vraća DPLL(𝐷 [𝑝 ↦→⊥ ]);
            elif lit < 0:
                for clause in D:
                    for j in range(len(clause)):
                        if clause[j] == lit:
                            has_changes = True
                            valuation[abs(lit)] = False
                            clause[j] = 'T'
                        elif clause[j] == -lit:
                            has_changes = True
                            clause[j] = 'F'

    if has_changes:
        print("{UNIT PROPAGATION}")
        print(D)
        res = DPLL(D)
        if res: return True


    # -------------------------------------------------------------------------
    # {Korak pure literal:}
    # ako 𝐷  sadrži literal 𝑝 (gde je 𝑝 neko iskazno slovo), ali ne i ¬𝑝 onda
    # vrati vrednost koju vraća DPLL(𝐷 [𝑝 ↦→ ]⊤ ) ;
    #
    # ako 𝐷 sadrži literal ¬𝑝 (gde je 𝑝 neko iskazno slovo), ali ne i 𝑝 onda
    # vrati vrednost koju vraća DPLL(𝐷 [𝑝 ↦→⊥ ]);
    # -------------------------------------------------------------------------
    has_changes = False
    literals = {}

    # Trazimo literal p za koji ne postoji literal ~p, i slicno,
    # trazimo literal ~p za koji ne postoji literal p.
    # Pamtimo ih u mapi za dalji rad.
    for i in range(len(D)):
        for literal in D[i]:
            if literal != 'T' and literal != 'F':
                if literal not in literals:
                    literals[literal] = 1
                if -literal in literals:
                    literals[-literal] = 0
                    literals[literal] = 0

    for (k, v) in literals.items():
        # Ako je v == 1 znaci da literal k jeste 'pure literal'.
        if v == 1:
            # Menjamo ga u formuli po prethodno navedenim pravilima.
            for clause in D:
                for i in range(len(clause)):
                    if clause[i] != 'T' and clause[i] != 'F' and abs(clause[i]) == abs(k):  # alex ovde ima bag: == abs(v) mu pise
                        has_changes = True
                        valuation[abs(v)] = True
                        clause[i] = 'T'

    if has_changes:
        print("{PURE LITERAL:}")
        print(D)
        res = DPLL(D)
        if res: return True

    # -------------------------------------------------------------------------
    # {Korak split:}
    # -------------------------------------------------------------------------
    literals = {}

    # Trazimo literale koji su kandidati za korak SPLIT
    for clause in D:
        for literal in clause:
            if literal != 'T' and literal != 'F':
                literals[abs(literal)] = 1

    for lit in literals:
        for clause in D:
            for i in range(len(clause)):
                if clause[i] == lit:
                    valuation[lit] = True
                    clause[i] = 'T'
                elif clause[i] == -lit:
                    # valuation[-lit] = False
                    clause[i] = 'F'
        print("{SPLIT}")
        print(D)
        res = DPLL(D)
        if res == True: return True

        for clause in D:
            for i in range(len(clause)):
                if clause[i] == lit:
                    valuation[lit] = False
                    clause[i] = 'F'
                elif clause[i] == -lit:
                    # valuation[-lit] = True
                    clause[i] = 'T'
        print("{SPLIT}")
        print(D)
        res = DPLL(D)
        if res == True: return res

    return DPLL(D)


def parseDimacs(dimacs_code):
    lines = dimacs_code.split('\n')
    D = []

    for i in range(len(lines)):
        lines[i] = lines[i].strip()
        if lines[i] == '': continue
        if lines[i].startswith("c"): continue
        if lines[i].startswith("p"): continue

        lines[i] = lines[i].split(' ')
        new_clause = []

        for literal in lines[i]:
            if int(literal) != 0:
                new_clause.append(int(literal))

        D.append(new_clause)

    return D


dimacs_code = 'c 123 sdf sdf\nc 12312\np cnf 2 3\n1 2 0\n1 -2 0\n2 -1 0'

if len(sys.argv) == 2:
    try:
        with open(sys.argv[1], "r") as f:
            dimacs_code = f.read()
    except IOError:
        sys.exit("Failed opening %s for reading..." % sys.argv[1])

D = parseDimacs(dimacs_code)

print(DPLL(D))
print(valuation)
