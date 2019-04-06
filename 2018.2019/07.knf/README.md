# Algoritam KNF i Minisat rešavač

- **Implementirana klasa za zapis formule**. Za iskaznu formulu važna je njena _interpretacija_
  (istinitosna vrednost; tačno, netačno) u datoj _valuaciji_. 
  Više o ovome pročitati u [skripti](http://poincare.matf.bg.ac.rs/~janicic//courses/vi.pdf),
  u delu "Sematika iskazne logike" (78 strana).


- Implemetiran algoritam za određivanje **konjuktivne normalne forme** za datu formulu.
  Algoritam i njegove osobine se može naći u [skripti](http://poincare.matf.bg.ac.rs/~janicic//courses/vi.pdf), 
  u delu "Normalne forme i potpuni skupovi veznika" (strana 86).

- Implementirano prevođenje forme u **DIMACS format**. 
  Opis DIMACS formata pogledati u slajdovima sa časa (151 - 160 slajd) ili [ovde](https://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html).

- **Pokretanje Minisat rešavača**:
	- Pogledati u slajdovima sa časa (144 - 167 slajd)
	- ```./minisat input.cnf output.txt```
	- [Minisat](http://minisat.se/MiniSat.html)
