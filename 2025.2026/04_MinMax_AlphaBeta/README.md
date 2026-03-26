# Vezbe 04 - MinMax i Alpha-Beta odsecanje

Ova lekcija pokriva dve centralne teme pretrage u igrama sa dva igrača:

- `MinMax` algoritam (idealna igra oba igrača),
- `Alpha-Beta pruning` (ubrzanje MinMax algoritma bez gubitka tačnosti).

## 1) Problem koji resavamo

Za igre poput iks-oks, connect-four, sah (u uproscenom modelu), igraci imaju suprotne ciljeve:

- `MAX` igrač želi da maksimizuje vrednost pozicije,
- `MIN` igrač želi da minimizuje vrednost pozicije.

Cilj algoritma je da za trenutno stanje igre pronadje **najbolji potez** pod pretpostavkom da oba igrača igraju optimalno.

## 2) MinMax detaljno

### 2.1 Osnovna ideja

Stablo igre se prolazi dubinski:

- na MAX nivou biramo dete sa največom evaluacijom,
- na MIN nivou biramo dete sa najmanjom evaluacjom,
- listovi su terminalna stanja ili stanja na granici dubine pretrage.

### 2.2 Rekurzivna definicija

Ako je stanje terminalno (ili dostignuta granica dubine), vraća se evaluacija stanja.

Inače:

- `minmax(state, depth, is_max=True)`:
  - ako `is_max`: vrati `max(minmax(child, depth-1, False))`
  - ako nije `is_max`: vrati `min(minmax(child, depth-1, True))`

### 2.3 Intuicija

MinMax simulira "najgori slucaj" za svakog igraca:

- MAX ne bira potez koji je dobar samo ako MIN pogreši,
- MIN ne bira potez koji je dobar samo ako MAX pogreši.

Zato je MinMax robustan model za protivničke igre nulte sume.

### 2.4 Složenost

Ako je faktor grananja `b`, a dubina `d`, puna MinMax pretraga je `O(b^d)`.

## 3) Alpha-Beta odsecanje

### 3.1 Sta su alpha i beta

- `alpha`: najbolja (najveća) vrednost koju MAX može sigurno da obezbedi na putu do datog čvora,
- `beta`: najbolja (najmanja) vrednost koju MIN moze sigurno da obezbedi na putu do datog cvora.

Odnosno teorijsko donje (alpha) i gornje (beta) ograničenje u kojem evaluacija optimalnog
poteza mora biti. Ukoliko je evaulacija nekog stanja van teorijskog (alpha, beta), ta pod grana se odseca.

Početno:

- `alpha = -inf`
- `beta = +inf`

### 3.2 Pravilo odsecanja

Tokom obilaska, ako u nekom trenutku važi:

- `alpha >= beta`

ostatak dece tog cvora **nema potrebu** da se obilazi, jer ne može promeniti finalnu odluku iznad.

### 3.3 Zasto je rezultat isti kao MinMax

Alpha-Beta ne menja vrednosti koje MinMax vraca, vec samo preskače grane koje su dokazano irelevantne.
Dakle, tačnost odluke ostaje ista kao kod punog MinMax-a.

### 3.4 Efekat redosleda poteza

Alpha-Beta je mnogo efikasniji kada se prvo obilaze "dobri" potezi (move ordering).

## 4) Najvazniji koncepti 

- Pobeda/poraz/remi i kako ih mapirati na evaluaciju.
- Kada nema terminalnog stanja na zadatoj dubini, ocena pozicije mora biti stabilna i smislena.
- Veća dubina daje bolju ocenu, ali značajno usporava pretragu.
- Ispravnost pretrage zavisi direktno od tačnog skupa legalnih poteza.
- Vrednost lista mora se korektno preneti do korena kroz min/max.
- U Alpha-Beta implementaciji, `alpha` i `beta` moraju se ažurirati tokom obilaska pod poteza.
- Redosled pretrage poteza je optimizacija sa velikim uticajem na brzinu.

## 5) Najcesce greske pri implementaciji

1. Pogrešno pozivanje MIN/MAX. MIN za prvog igrača, ili MAX za drugog.
- Simptom: algoritam bira očigledno loše poteze.

2. Neispravni bazni uslovi
- Nema provere terminalnog stanja ili dubine, pa rekurzija ide preduboko / nikad ne staje.

3. Mešanje semantike evaluacije
- Na primer, +10 za MIN pobedu i -10 za MAX pobedu (obrnuti znakovi).

4. Mutiranje stanja bez vraćanja/čuvanja prethodnog
- Ako menjate tablu "u mestu" bez pravilnog vraćanja, kasnije grane koriste pogrešno stanje.

5. Loše kopiranje stanja
- Plitko kopiranje umesto dubokog pri grananju.

6. Pogrešno azuriranje alpha/beta
- Na MAX nivou treba ažurirati `alpha`, na MIN nivou `beta`.

7. Pogrešan uslov odsecanja
- Treba proveravati `alpha >= beta` unutar petlje.

8. Pogrešna povratna vrednost
- Često se vrati score bez poteza, pa nije jasno šta odigrati iz korena.

9. Ignorisanje remija
- Ako remi nije eksplicitno modelovan, algoritam se ponaša nestabilno.

10. Prejaka zavisnost od dubine bez heuristike
- Fiksna dubina bez dobre evaluacije vodi ka slabim potezima.

## 6) Predlog redosleda ucenja za ovu nedelju

1. Implementirati čist MinMax bez optimizacija.
2. Proveriti tačnost na malom stablu sa poznatim rezultatima.
3. Dodati Alpha-Beta odsecanje.
4. Uvesti brojač posecenih čvorova i uporediti performanse.
5. Dodati odbari redoselda poteza i ponovo izmeriti razliku.

## 7) Zadaci za vežbu

1. MinMax na ručno zadatom stablu
- Data su vrednovanja listova; izračunati vrednost korena i najbolji potez.

2. Implementacija MinMax za iks-oks
- Terminali: pobeda, poraz, remi.
- Primer evaluacije: `+1` pobeda MAX, `0` remi, `-1` poraz MAX.

3. Dodavanje Alpha-Beta
- Izmeriti broj posećenih čvorova pre i posle optimizacije.

4. Vizuelizacija pretrage
- Ispisati redosled obilaska čvorova i mesta odsecanja.

5. Eksperiment sa redosledom poteza
- Uporediti "dobar" i "los" ordering nad istim stanjima.

## 8) Domaći zadatak

1. Iterativno produbiljivanje poteza.
2. Memoizacija stanja.
3. Poboljšan redosled poteza 