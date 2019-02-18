#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time, os

class ProgressBar():
    """ Klasa predstavlja implementaciju kontrole za prikazivanje progresa. """
    def __init__(self, width=50):
        """
        pointer - Celobrojna vrednost iz intervala [0, 100] koja oznacava koliki je progress postignut.
        width - Sirina kontrole koja ce biti iscrtana.
        """
        self.pointer = 0
        self.width = width

    def __call__(self, current_progress):
        """
        Funkcija predstavlja implementaciju operatora () koji se moze pozvati nad objektom klase 'ProgressBar'.
        Operator () vraca stringovnu reprezentaciju trenutnog progresa (current_progress)
        """
        self.pointer = int(self.width*(current_progress/100.0))
        return "|" + "#"*self.pointer + "-"*(self.width-self.pointer)+ "| %d%% done" % int(current_progress)


def main():
    pb = ProgressBar()
    for i in range(101):
        os.system("clear")
        print(pb(i))
        time.sleep(0.1)

if __name__ == "__main__":
    main()
