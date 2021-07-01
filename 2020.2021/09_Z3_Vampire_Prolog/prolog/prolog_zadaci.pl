% =======================================================================================
% Ekstenzija BProlog fajla je .pl
% Procitati uputstvo na http://www.picat-lang.org/bprolog/download/manual.pdf o pokretanju programa, debagovanju itd...
% =======================================================================================

% =======================================================================================
% Par osnovnih napomena
%
% Konstante se pisu malim slovom. Promenljive se pisu velikim slovom.
% Operatori: 
% = (unifikabilni), \= (nisu unifikabilni), ==(identicno jednaki termovi), \== (nisu identicno jednaki termovi)
% Primeri: 
% | ?- 3 = 4
% no
% | ?- 3 = X
% X = 3
% yes
% | ?- 3 = x
% no
% | ?- 3 == 4
% no
% | ?- 3 == X
% no

% =======================================================================================
% Koriscenje negacije.
% =======================================================================================

musko(marko).
musko(tomislav).
ozenjen(tomislav).

nezenja(P):- musko(P), \+(ozenjen(P)).

% Donje resenje je neispravno. Pokrenuti sa nezenja(X). i videti razliku.
% nezenja(P):- \+(ozenjen(P)), musko(P).

% =======================================================================================
% Primer sa porodicnim stablom. (iz knjige)
% =======================================================================================

 musko(kron).
 musko(posejdon).
 musko(zevs).
 musko(jasion).
 musko(triton).
 musko(apolon).
 musko(pluton).
 zensko(reja).
 zensko(amfitrita).
 zensko(leto).
 zensko(demetra).
 zensko(artemida).
 roditelj(kron,posejdon).
 roditelj(reja,posejdon).
 roditelj(kron,zevs).
 roditelj(reja,zevs).
 roditelj(kron,demetra).
 roditelj(reja,demetra).
 roditelj(posejdon,triton).
 roditelj(amfitrita,triton).
 roditelj(zevs,apolon).
 roditelj(leto,apolon).
 roditelj(zevs,artemida).
 roditelj(leto,artemida).
 roditelj(jasion,pluton).
 roditelj(demetra,pluton).

 predak(X,Y) :- roditelj(X,Y).
 predak(X,Y) :- roditelj(X,Z), predak(Z,Y).
 majka(X,Y) :- zensko(X), roditelj(X,Y).
 otac(X,Y) :- musko(X), roditelj(X,Y).
 brat(X,Y) :- musko(X), roditelj(Z,X), roditelj(Z,Y), X\==Y.
 sestra(X,Y) :- zensko(X), roditelj(Z,X), roditelj(Z,Y), X\==Y.
 tetka(X,Y) :- sestra(X,Z), roditelj(Z,Y).
 stric(X,Y) :- brat(X,Z), otac(Z,Y).
 ujak(X,Y) :- brat(X,Z), majka(Z,Y).
 bratodstrica(X,Y) :- musko(X), otac(Z,X), stric(Z,Y).
 sestraodstrica(X,Y) :- zensko(X), otac(Z,X), stric(Z,Y).
 bratodujaka(X,Y) :- musko(X), otac(Z,X), ujak(Z,Y).
 sestraodujaka(X,Y) :- zensko(X), otac(Z,X), ujak(Z,Y).
 bratodtetke(X,Y) :- musko(X), majka(Z,X), tetka(Z,Y).
 sestraodtetke(X,Y) :- zensko(X), majka(Z,X), tetka(Z,Y).

% =======================================================================================
% Logicki zadatak
% 
% Ko laze taj krade.
% Ko krade i uhvacen je u kradi taj ide u zatvor.
% Al Kapone laze.
% Al Kapone je uhvacen u kradi.
% Laki Luciano laze.
% Napisati PROLOG program koji opisuje navedene cinjenice i pravila. Koje odgovore PROLOG daje na upite
% ”da li Al Kapone ide u zatvor” i ”da li Laki Luciano ide u zatvor”.
% =======================================================================================

krade(X):- laze(X).
zatvor(X):- krade(X), uhvacen_u_kradji(X).

laze(alKapone).
laze(lakiLuciano).
uhvacen_u_kradji(alKapone).


% =======================================================================================
% Bojenje grafa
% Posmatra se karta i na njoj Srbija i njeni susedi.
% Potrebno je naci bojenje karte takvo da svaka zemlja bude obojena zutom, zelenom ili plavom bojom,
% a da susedne zemlje budu obojene razlicitim bojama.  
% =======================================================================================

bojenje(Srb, Cg, Mak, Hrv, Slo, Bih, Madj, Bug, Rum):-
sused(Srb, Cg),
sused(Srb, Mak),
sused(Srb, Hrv),
sused(Srb, Bih),
sused(Srb, Madj),
sused(Srb, Bug),
sused(Srb, Rum),
sused(Cg, Hrv),
sused(Cg, Bih),
sused(Hrv, Slo),
sused(Hrv, Bih),
sused(Hrv, Madj),
sused(Madj, Rum),
sused(Rum, Bug).

boja(zuta).
boja(plava).
boja(crvena).

sused(X,Y):-boja(X), boja(Y), X\==Y.


% =======================================================================================
% Logicki zadatak (zapisati tvrdjenja, otkriti ko je udario macku)
%
% Ko je udario macku Tunu?
% Macka je zivotinja.
% Vlasnik psa voli zivotinje.
% Janko ima psa. Marko nema psa.
% Ne bi udario zivotinju ko voli zivotinje.
% Macku bi udario onaj koji bi je mozda udario i nije da je ne bi udario.
% =======================================================================================


macka(tuna).
vlasnikpsa(janko).
mozda_udario(marko,tuna).
mozda_udario(janko,tuna).

zivotinja(X):-macka(X). 
volizivotinje(X):-vlasnikpsa(X).
ne_bi_udario(X,Y):-volizivotinje(X),zivotinja(Y).
udario(X,Y):-mozda_udario(X,Y), \+(ne_bi_udario(X,Y)).

