#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Dokumentacija
# https://docs.python.org/3.6/tutorial/datastructures.html#dictionaries

def main():
    computer_scientists = {
        "Alan Turing": 1912,
        "Alonzo Church": 1903,
        "Tony Hoare": 1934,
        "Edsger W. Dijkstra": 2019,
        "John Doe": 2019
    }

    # Dodavanje elementa u mapu
    computer_scientists["Donald Knuth"] = 1938

    # -------->
    # Domaci -> kako azurirati element samo ako postoji? (Kod iznad dodaje element ako ne postoji)
    # -------->

    # Azuriranje vrednosti
    computer_scientists["Edsger W. Dijkstra"] = 1930

    # Brisanje vrednosti
    del computer_scientists["John Doe"]

    for name, born_age in computer_scientists.items():
        s = "%s je rodjen %g godine." % (name, born_age)
        print(s)

    # Provera da li mapa poseduje kljuc
    if "Alan Turing" in computer_scientists:
        print("Alan Turing: %d" % computer_scientists["Alan Turing"])

    if "John Doe" not in computer_scientists:
        print("John Doe ne postoji u mapi!")

    # Kako dobiti listu uredjenih parova iz mape,
    # gde je prvi element kljuc, drugi element vrednost?
    # .items() ne vraca novu listu, vec 'pogled' na mapu apstrahovan listom.
    # To znaci da ako bi neko promenio originalnu mapu, i pogled kroz listu bi se azurirao.
    # Zbog toga konstruktoru za listu ('list') prosledjujemo pogled da napravi novu listu
    xs = list(computer_scientists.items())
    print(xs)

if __name__ == "__main__":
    main()
