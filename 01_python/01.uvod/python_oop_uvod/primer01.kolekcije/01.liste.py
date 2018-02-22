#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Dokumentacija - pogledati dostupne metode
# https://docs.python.org/3/tutorial/datastructures.html
#
# U interpreteru dokumentaciju mozete dobiti sa:
# help([])      <- help(x) vraca dokumentaciju o tipu objekta x (sto je ovde prazna lista tj lista)

def main():
    # Pravljenje liste sa inicijalizacijom
    xs = [1, 2, 3, 4, 5, 6]

    # Dodavanje u listu
    xs.append(7)
    xs.append(7)
    xs.append(7)

    # Iteriranje kroz listu
    print("Sadrzaj liste:")
    for x in xs:
        x += 1
        print(x - 1)

    # Primetite, foreach petlja vraca kopije elemenata, i dalje imamo originalnu listu.
    print(xs)

    # Broj elemenata liste.
    n = len(xs)
    print("Duzina liste je " + str(n))

    # Obrtanje liste.
    xs.reverse()
    print("Obrnuta lista: " + str(xs))  # str vrsi konverziju objekta u string

    # Prebrojavanje elementa u listi.
    print("Broj pojavljivanja broja %d u listi %s je %d" % (7, str(xs), xs.count(7)))

    # Konstrukcija gore se naziva interpolacija stringa, slicno je formatiranju stringa u C-u koristeci printf.
    names = ["Alan Turing", "Edsger W. Dijkstra", "Tony Hoare"]
    born = [1912, 1930, 1934]
    # range nam vraca objekat kroz koji mozemo iterirati i dobiti indekse 0, 1, ..., n-1.
    for i in range(len(names)):
        s = "%s je rodjen %d godine." % (names[i], born[i])     # mozemo indeksirati kao u C-u
        print(s)

    # Sortiranje
    xs = [5, 1, 4, 3, 2, 6, 8, 7, 0]
    xs.sort()
    print("Sortirana lista: %s" % str(xs))
    xs.sort(reverse=True)
    print("Obrnuto sortirana lista: %s" % str(xs))

    # Mozemo uzeti podlistu liste - takozvani 'slicing'.
    print("Prvih 5 elemenata iz liste %s je %s" % (xs, xs[0:5]))

    # Poslednjih 5
    # Poslednji element je na indeksu -5, tako da smo rekli:
    # "Pocevsi od 5og elementa sa kraja pa do kraja, daj mi podlistu..."
    print("Poslednjih 5 elemenata iz liste %s je %s" % (xs, xs[-5:]))   # poslednji element je na indeksu -1...

    # Liste mozemo i elegantno generisati u jednon liniji
    kvadrati = [x*x for x in range(10)]
    print("Kvadrati brojeva %s su %s " % ([x for x in range(10)], kvadrati))

if __name__ == "__main__":
    main()

