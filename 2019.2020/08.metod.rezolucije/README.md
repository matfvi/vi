# Prenex normalna forma. Metod rezolucije.

### Prenex normalna forma.
- Transformisanje formule u prenex normalnu formu.

### Metod rezolucije.
- Primena metoda rezolucije na zadatke sa slajdova.

### Vampir, rezolucijski dokazivač. 
- Pokretanje sa ```./vampir primer```
- **Sintaksa**, svaku formulu zapisujemo na sledeći način:
	1. ```fof(name, role, formula).```
	2. ```fof``` označava da je u pitanju fomula u logici prvog reda (formulae in full first order form)
	3. ```name``` je ime i moće biti bilo šta
	4. ```role``` označava ulogu formule u tvrđenju i može biti: ```axiom```, ```conjecture```, ```lemma```, ```hzpothesis``` itd.
	5. Formula se zapisuje korišćenjem sledećih simbola:
	   - te, ne-te: $true, $false
	   - negacija: ~
	   - konjukcija: &
       - disjunkcija: |
       - implikacija: =>
       - ekvivalencija: <=>
       - kvantifikator za svaki: !
       - kvantifikator postoji: ?
- Više se može pronaći [ovde](http://www.vprover.org/cav2013.pdf).

