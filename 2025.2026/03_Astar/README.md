# Vezbe 03 - A* pretraga

Uvod u A* (A-star) algoritam pretrage. Cilj vežbi je razumeti:

- kako A* bira sledece stanje,
- zasto je heuristika kljucna,
- kako se radi na eksplicitnim i implicitnim grafovima,
- kako se A* primenjuje na lavirint i Loydovu (8-puzzle) slagalicu.

## Ishodi ucenja

Nakon ovih vezbi umećete da:

- implementirate osnovni A* algoritam,
- objasnite razliku izmedju `open_set` i `closed_set`,
- definisete heuristiku i procenite njen kvalitet,
- primeni A* na probleme sa unapred zadatim i generisanim susedima.

## Ideja algoritma A*

A* za svako stanje `n` koristi tri vrednosti:

- `g(n)`: realna cena od početnog stanja do `n`,
- `h(n)`: procena cene od `n` do cilja (heuristika),
- `f(n) = g(n) + h(n)`: ukupna procena kvaliteta stanja.

U svakom koraku bira se stanje sa najmanjim `f(n)` iz `open_set`.

Intuicija:

- `g(n)` čuva informaciju koliko je put do sada stvarno koštao,
- `h(n)` usmerava pretragu ka cilju,
- zbir (`f`) balansira istrazivanje i usmeravanje.

Ako je `h(n) = 0` za sva stanja, A* postaje Dijkstra algoritam.

## Pseudokod (pojednostavljen)

```text

```

## Strukture podataka u svesci

U implementaciji cete videti:

- `open_set`: kandidati za dalje širenje,
- `closed_set`: već obrađeni čvorovi,
- `cheapest_paths` (mapa `g`): najmanja poznata cena do trenutnog čvora,
- `parent`: pokazivacč za rekonstrukciju putanje.

Napomena o performansama:

- u notebook verziji najbolji čvor se trazi linearnim prolaskom kroz `open_set`,
- efikasnija varijanta koristi red sa prioritetom (`heapq`).

## Heuristika: zasto je bitna

Heuristika odredjuje koliko će pretraga biti brza. Dobra heuristika:

- smanjuje broj obrađenih stanja,
- ne narušava optimalnost (ako je dopustiva),
- treba da bude jeftina za računanje.

Za Loydovu slagalicu koristi se Menhetn rastojanje:

- za svaku pločicu se meri udaljenost od ciljne pozicije,
- zbir tih rastojanja daje `h(n)`.

U praksi se ignoriše prazno polje (`0`) kada se računa heuristika. U ovoj svesci računanje uključuje sve vrednosti, što je dobro za demonstraciju, ali za strogu teorijsku analizu preporučuje se standardna varijanta bez `0`.

## Eksplicitan vs implicitan graf

### Eksplicitan graf

Graf je unapred zadat (lista čvorova i grana). A* samo čita susede.

Primer: mali graf sa zadatim granama i težinama.

### Implicitan graf

Graf se ne konstruiše u napred. Susedi se generišu dinamično, tokom pretrage, iz trenutnog stanja.

Primer: Loydova slagalica.

- stanje je 3x3 matrica,
- potez je pomeranje praznog polja (`0`) gore/dole/levo/desno,
- svaka legalna promena generiše novo stanje (suseda).

## Loydova slagalica u ovoj nedelji

Notebook `Astar.ipynb` pokriva:

1. osnovni A* algoritam,
2. uvod u heuristike (`euclid`, `manhattan`, `chebyshev`),
3. lavirint,
4. Loydovu slagalicu (osnovni primer),
5. dodatne analogne Loyd primere A, B, C i D.

Za svaki Loyd primer ispisuje se:

- broj poteza do cilja,
- kompletna putanja kroz stanja.

## Kako čitati rezultat izvršavanja algoritma A* 

Kada se dobije lista stanja:

- dužina putanje minus 1 je broj poteza,
- poslednje stanje mora biti ciljno,
- validnost putanje proveravate tako što se svako stanje razlikuje od prethodnog za tačno jedan legalan potez.

## Česte greske

- mesanje `open_set` i `closed_set` logike,
- neažuriranje roditelja kada se nadje bolji put,
- loše predstavljanje stanja (mutable tip kao kljuc),
- heuristika koja značajno usporava pretragu,

## Predlozi za samostalan rad

1. Implementirati BFS i uporediti ga sa A* na istim ulazima.
2. Zameniti linearni izbor najboljeg cvora sa `heapq` prioritetnim redom.
3. Dodati proveru resivosti 8-puzzle instance pre pretrage.
4. Uporediti vise heuristika i meriti broj prosirenih stanja.
5. Proširiti primer na 15-puzzle (4x4) i analizirati skaliranje.
