# Vezbe 05 - Uvod u iskaznu logiku

Ova nedelja uvodi osnove iskazne logike koje su neophodne za formalno modelovanje problema i kasniji rad sa SAT solverima (`minisat`) i SMT alatima (`z3`).

Cilj je da naucite kako da:

- zapisete tvrdnje kao logicke formule,
- procenite istinitost formula,
- utvrdite da li je formula tautologija, kontradikcija ili zadovoljiva,
- transformisete formule u standardne oblike (posebno CNF),
- pripremite logicki model za automatsko resavanje.

## Ishodi ucenja

Nakon ove vezbe student treba da ume da:

1. razlikuje sintaksu i semantiku iskazne logike,
2. koristi osnovne logicke konektive,
3. konstruise tablicu istinitosti za formulu,
4. proveri logicku ekvivalenciju formula,
5. prepozna posledicu (`entailment`) i zadovoljivost,
6. transformise formulu u ekvivalentan CNF oblik,
7. modeluje jednostavan problem iz realnog opisa kao skup logickih ogranicenja.

## 1) Osnovni pojmovi

### Iskazna promenljiva

Iskazna promenljiva (`p`, `q`, `r`, ...) moze imati samo dve vrednosti:

- `True` (istinito)
- `False` (neistinito)

### Formula

Formula je izraz formiran od promenljivih i konektiva.

Najvazniji konektivi:

- negacija: `¬p`
- konjunkcija: `p ∧ q`
- disjunkcija: `p ∨ q`
- implikacija: `p → q`
- ekvivalencija: `p ↔ q`

## 2) Sintaksa vs semantika

- `Sintaksa`: kako je formula napisana (pravila formiranja).
- `Semantika`: sta formula znaci, tj. kada je istinita.

Primer:

- `p -> q` i `¬p ∨ q` su sintaksno razlicite formule,
- semanticki su ekvivalentne (iste vrednosti za sva vrednovanja).

## 3) Tablice istinitosti

Tablica istinitosti je osnovni alat za proveru formula.

Za `n` promenljivih postoji `2^n` mogucih vrednovanja.

Tablice koristimo za:

- proveru tautologije,
- proveru kontradikcije,
- proveru zadovoljivosti,
- proveru ekvivalencije dve formule.

### Klasifikacija formula

- `tautologija`: istinita za svako vrednovanje,
- `kontradikcija`: neistinita za svako vrednovanje,
- `zadovoljiva`: istinita bar za jedno vrednovanje,
- `nezadovoljiva`: ne postoji nijedno vrednovanje koje je cini istinitom.

## 4) Logicka posledica i ekvivalencija

### Logicka posledica

`A |= B` znaci: u svakom modelu gde je `A` istinito, i `B` je istinito.

Prakticna provera preko nezadovoljivosti:

- `A |= B` je ekvivalentno sa tim da je `A ∧ ¬B` nezadovoljivo.

### Ekvivalencija

`A ≡ B` znaci da formule imaju iste vrednosti za sva vrednovanja.

Prakticna provera:

- proveriti da li je `(A ↔ B)` tautologija,
- ili proveriti da li su `A ⊕ B` (exclusive-or) nezadovoljive.

## 5) Vazne logicke transformacije

Najcesce korisceni zakoni:

1. Eliminacija implikacije:
- `p -> q  ≡  ¬p ∨ q`

2. Eliminacija ekvivalencije:
- `p <-> q  ≡  (p -> q) ∧ (q -> p)`

3. De Morgan:
- `¬(p ∧ q) ≡ ¬p ∨ ¬q`
- `¬(p ∨ q) ≡ ¬p ∧ ¬q`

4. Dvostruka negacija:
- `¬¬p ≡ p`

5. Distributivnost:
- `p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r)`
- `p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)`

6. Idempotentnost, komutativnost, asocijativnost (za sredjivanje formule).

## 6) CNF (Conjunctive Normal Form)

CNF je konjunkcija klauza, gde je svaka klauza disjunkcija literala.

- literal je promenljiva ili njena negacija (`p`, `¬p`),
- primer CNF: `(p ∨ ¬q) ∧ (r ∨ s ∨ ¬t)`.

### Zasto je CNF bitan

SAT solveri standardno ocekuju ulaz u CNF obliku.
Zato je ovo kljucna priprema za sledece nedelje.

### Standardni postupak pretvaranja u CNF

1. Ukloniti `->` i `<->`.
2. Spustiti negacije do literala (NNF) koristeci De Morgan + dvostruku negaciju.
3. Primeniti distributivnost da se dobije konjunkcija disjunkcija.
4. Pojednostaviti formulu (ukloniti duplikate i trivijalnosti gde je moguce).

## 7) Najcesce greske

1. Pogresno tumacenje implikacije
- `p -> q` nije isto sto i `q -> p`.

2. Pogresna primena De Morgan zakona
- Cesta greska je promena samo operatora bez negiranja oba operanda.

3. Mesanje satisfiability i validity
- "zadovoljiva" nije isto sto i "istinita za sva vrednovanja".

4. Gubitak zagrada u transformacijama
- Sitna greska u prioritetu operatora menja znacanje formule.

## 8) Preporucena metodologija rada

- Korak 1: formalizujte recenice (precizno definisite promenljive).
- Korak 2: napisite formulu bez optimizacija.
- Korak 3: proverite tablicom istinitosti na malim primerima.
- Korak 4: tek onda radite transformacije (NNF/CNF).
- Korak 5: proverite da li je transformisana formula ekvivalentna originalu.

## 9) Zadaci za vezbu (na casu)

1. Tablica istinitosti
- Za formulu `(p -> q) ∧ (q -> r) -> (p -> r)` napraviti tablicu i klasifikovati formulu.

2. Ekvivalencija
- Dokazati tablicom da je `p -> q` ekvivalentno `¬p ∨ q`.

3. Entailment
- Proveriti da li iz `p -> q` i `p` sledi `q`.

4. CNF transformacija
- Pretvoriti `¬(p -> q) ∨ (r -> p)` u CNF korak po korak.

5. Mini modelovanje
- Formalizovati: "Ako pada kisa, ulica je mokra. Pada kisa." i zakljuciti posledicu.

## 10) Domaci zadatak

### Obavezni deo

1. Za 5 datih formula:
- napraviti tablice istinitosti,
- odrediti da li su tautologija/kontradikcija/zadovoljive.

2. Za 3 para formula:
- proveriti ekvivalenciju (tablica ili formalna transformacija).

3. Za 4 formule:
- uraditi konverziju u CNF sa svim medjukoracima.

4. Za 2 tekstualna problema:
- definisati promenljive,
- napisati logicke formule,
- objasniti sta predstavlja model resenja.

### Bonus

1. Napisati Python funkciju koja evaluira formulu za zadato vrednovanje.
2. Automatski generisati tablicu istinitosti za formule sa do 5 promenljivih.
3. Uporediti rezultat manuelne analize sa SAT alatom u sledecoj nedelji.

## 11) Checklist pre predaje

- Sve promenljive su jasno definisane.
- Operatori su konzistentno korisceni (`¬, ∧, ∨, ->, <->` ili ASCII varijanta).
- CNF konverzija sadrzi sve korake, ne samo finalni oblik.
- Za svaku tvrdnju postoji dokaz (tablica ili formalna transformacija).
- Zakljucci su odvojeni od pretpostavki i jasno napisani.

## Materijal u folderu

- `Iskazna logika.ipynb` - centralna sveska za uvod, primere i vezbu.

