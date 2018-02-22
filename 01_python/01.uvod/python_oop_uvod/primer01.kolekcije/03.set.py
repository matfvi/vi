#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Dokumentacija
# https://docs.python.org/3.6/tutorial/datastructures.html#sets

def write_set(name, s): print("%s = %s" % (name, s))

def main():
    # Skup pravimo pozivom konstruktora 'set' kojem prosledjujemo listu na osnovu
    # koje zelimo da se konstruise skup.
    # Primetite, ignorisace se duplikati.
    A = set([1, 2, 3, 1, 1, 1, 2, 4, 1, 2, 3, 1, 1, 1])
    write_set("A", A)

    B = set(range(0, 10))
    write_set("B", B)

    print("A ∪ B = %s" % (A | B))
    print("A ∩ B = %s" % (A & B))
    print("A ∖ B = %s" % (A ^ B))
    print("A ⊆  B = %s" % (A < B))
    print("B ⊆  A = %s" % (B < A))

    # Dodavanje u skup
    A.add(4)
    print("Dodato 4 u A")
    write_set("A", A)

    A.remove(4)
    write_set("A", A)

if __name__ == "__main__":
    main()
