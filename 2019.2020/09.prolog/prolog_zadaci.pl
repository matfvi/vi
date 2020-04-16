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


% =======================================================================================
% Broj dana u svakom mesecu.
% =======================================================================================

prestupna(G):- G mod 400 =:= 0.

prestupna(G):- G mod 4 =:= 0,
               G mod 100 =\= 0.     
               
broj_dana(januar, _, 31).
broj_dana(april, _, 30).
broj_dana(februar, X, 29):- prestupna(X).
broj_dana(februar, X, 28):- \+(prestupna(X)).
% itd... za ostale mesece


% =======================================================================================
% Apsolutna vrednost
% =======================================================================================
% Losa implementacija
aps1(X, X):- X >= 0.
aps1(X, Y):- Y is -X.

% Dobra implementacija
aps2(X, X):- X >= 0.
aps2(X, Y):- X < 0,
             Y is -X.


% =======================================================================================
% Nekoliko aritmetickih zadataka
% =======================================================================================

% Suma prvih N prirodnih brojeva.
suma1(1, 1).
suma1(N, S):- N > 1,
              M is N - 1,
              suma1(M, S1),
              S is S1 + N. 
              
% Suma cifara broja.
suma2(N, N):- N < 10.
suma2(N, S):- N >= 10,
              M is N // 10,
	          suma2(M, S1),
	          S is S1 + (N mod 10). 


% =======================================================================================
% Hanojeve kule
% Potrebno je prebaciti N diskova poredjanih po velicini sa stuba X na stub Z koriscenjem stuba Y.
% Pri tome nije dozvoljeno da veci disk stoji na manjem disku.
% Napisati prolog predikat koji ispisuje korake u premestanju diskova.
% =======================================================================================
hanoj(1, X, _, Z):- write('prebaci sa '),
                    write(X),
                    write(' na '),
                    write(Z),
                    nl.  

hanoj(N, X, Y, Z):- N > 1,
                    M is N - 1,
                    hanoj(M, X, Z, Y),
                    hanoj(1, X, _, Z),
                    hanoj(M, Y, X, Z).	          


        

% =======================================================================================
% =======================================================================================
% Rad sa listama
% 
% Primer liste: [1, 2, 3, 4]
% [] - prazna lista
% [1, [2, 3], 4] - lista u listi
% [G|R] [1, 2, 3, 4] G = 1 R=[2, 3, 4] (glava i rep)
% [1] G = 1 R=[]
% [[1, 2], 4] G = [1, 2] R = [4]
% =======================================================================================

% =======================================================================================
% Par osnovnih operacija sa listama
% =======================================================================================

% Dodaj element na pocetak  liste.
dodaj(X, L, [X|L]).

% Dodaj element na kraj liste.
dodaj_na_kraj(X, [], [X]).
dodaj_na_kraj(X, [G|R], [G|LR]):- dodaj_na_kraj(X, R, LR).

% Da li lista sadrzi dati element.
sadrzi(X, [X|_]).
sadrzi(X, [G|R]):- G \== X,
                   sadrzi(X, R).

% Spajanje dve liste.
% spoji(L1, L2, L)
spoji([], L, L).
spoji([G|R], L, [G|LR]):- spoji(R, L, LR).

% Zameniti dva elementa liste
zameni(X, Y, [X|R], [Y|R1]):- zameni(X, Y, R, R1).
zameni(X, Y, [G|R], [G|R1]):- G \== X,
                              zameni(X, Y, R, R1).
zameni(X, Y, [], []).


% Brisanje elemenata liste
brisi(X, [], []).
brisi(X, [X|R], R1):- brisi(X, R, R1).
brisi(X, [G|R], [G|R1]):- G \== X,
                          brisi(X, R, R1).
                          
                         

% Brisi samo prvo pojavljivanje elementa u listi.
brisi1(X, [], []).
brisi1(X, [X|R], R):- !.
brisi1(X, [G|R], [G|R1]):- G \== X,
                           brisi1(X, R, R1).

% Provera da li su tri elementa uzastopni elementi liste
uzastopni(X, Y, Z, [X, Y, Z|_]):- !.
uzastopni(X, Y, Z, [_|R]):- uzastopni(X, Y, Z, R).   

% Podeliti listu na dve liste - listu pozitivnih i listu negativnih elemenata.
podeli([], [], []).
podeli([G|R], [G|R1], LN):- G >= 0,
                            podeli(R, R1, LN).
podeli([G|R], LP, [G|R1]):- G < 0,
                            podeli(R, LP, R1).   


% Podeliti listu na sve moguce nacine.
% [1, 2, 3] 
% [] [1, 2, 3]
% [1] [2, 3]
% [1, 2] [3]
% itd....
% podeli(L, L1, L2).
% Pogledati efekat koriscenja ugradjene funkcije findall.
% Pozvati sa findall(L1, podeli1([1, 2, 3], L1, L2), Res).

podeli1([], [], []).
podeli1([G|R], [G|R1], Y):- podeli1(R, R1, Y).
podeli1([G|R], X, [G|R1]):- podeli1(R, X, R1).


% Permutacije
permutacije([], []).
permutacije(L, [X|R]):- sadrzi(X, L),
                        brisi(X, L, L1),
                        permutacije(L1, R).




% Kombinacije
kombinacije(_, 0, []).
kombinacije(L, N, [X|R]):- sadrzi(X, L),
                           brisi(X, L, L1),
                           N1 is N - 1,
                           kombinacije(L1, N1, R).


% =======================================================================================
% Zagonetke
% =======================================================================================

% =======================================================================================
% Cetiri coveka se zovu Pera, Mika, Laza i Jova, 
% a prezivaju Peric, Mikic, Lazic i Jovic.
% Oni imaju cetiri sina koji se takodje
% zovu Pera, Mika, Laza i Jova.
% Pretpostavimo sledece:
% (a) Niko od oceva se ne zove u skladu sa svojim prezimenom.
% (b) Niko od sinova se ne zove u skladu sa svojim prezimenom.
% (c) Niko od sinova se ne zove isto kao i otac.
% (d) Peric stariji se zove isto kao Mikin sin.
% (e) Lazin sin se zove Pera.
% Napisati predikat koji odredjuje imena oceva i sinova.
% =======================================================================================
% ime oca, ime sina, prezime
resi(L) :-
    L = [[laza, pera, _], [X, _, peric], [mika, X, _], _],
    % lazin sin se zove pera
    sadrzi([jova, _, _], L),
    sadrzi([pera, _, _], L),
    sadrzi([_, laza, _], L),
    sadrzi([_, jova, _], L),
    sadrzi([_, mika, _], L),
    sadrzi([_, _, mikic], L),
    sadrzi([_, _, jovic], L),
    sadrzi([_, _, lazic], L),
    \+(sadrzi([mika, _, mikic], L)),
    \+(sadrzi([pera, _, peric], L)),
    \+(sadrzi([jova, _, jovic], L)),
    \+(sadrzi([laza, _, lazic], L)),
    \+(sadrzi([_, mika, mikic], L)),
    \+(sadrzi([_, pera, peric], L)),
    \+(sadrzi([_, jova, jovic], L)),
    \+(sadrzi([_, laza, lazic], L)),
    \+(sadrzi([mika, mika, _], L)),
    \+(sadrzi([pera, pera, _], L)),
    \+(sadrzi([jova, jova, _ ], L)),
    \+(sadrzi([laza, laza, _], L)).

% =======================================================================================
%  1. There are five houses, each of a different color and inhabited by
%     people of different nationalities, with different pets, drinks, and
%     cigarette brands.
%  2. The English person lives in the red house.
%  3. The Spaniard owns a dog.
%  4. Coffee is drunk in the green house.
%  5. The Ukranian drinks tea.
%  6. The green house is immediately to the right of the ivory house.
%  7. The Old-Gold smoker has a pet snail.
%  8. Kools are being smoked in the yellow house.
%  9. Milk is drunk in the middle house.
% 10. The Norwegian lives in the first house on the left.
% 11. The Chesterfield smoker lives next to the fox owner.
% 12. Kools are smoked in the house next to the house where the horse is kept. 
% 13. The Lucky-Strike smoker drinks orange juice.
% 14. The Japanese smokes Parliament.
% 15. The Norwegian lives next to the blue house.
% 16. There is one house where drink is water.
% 17. There is one house where pet is zebra.
%
% Who owns the zebra?
% Redosled kodiranja:
% color, nationality, pets, drink, ciggarette
% =======================================================================================
desno_od(X, Y, [Y, X|R]).
desno_od(X, Y, [G|R]):- desno_od(X, Y, R).

pored(X, Y, L):- desno_od(X, Y, L).
pored(X, Y, L):- desno_od(Y, X, L).

sadrzi(X, [X|_]).
sadrzi(X, [G|R]):- sadrzi(X, R).

resi1(L):-
    L = [[_, norwegian, _, _, _], [blue, _, _, _, _], [_, _, _, milk, _], _, _],
    sadrzi([red, english, _, _, _], L),
    sadrzi([_, spaniard, dog, _, _], L),
    sadrzi([green, _, _, coffee, _], L),
    sadrzi([_, ukrainian, _, tea, _], L),
    desno_od([green, _, _, _, _], [ivory, _, _, _, _], L),
    sadrzi([_, _, snail, _, oldGold], L),
    sadrzi([yellow, _, _, _, kools], L),
    pored([_, _, _, _, chesterfield], [_, _, fox, _, _], L),
    pored([_, _, _, _, kools], [_, _, horse, _, _], L),
    sadrzi([_, _, _, orange, lickyStrike], L),
    sadrzi([_, japanese, _, _, parliament], L),
    sadrzi([_, _, _, water, _], L),
    sadrzi([_, _, zebra, _, _], L).   

% =======================================================================================
% Three friends took the first, second and third places in the Universiade competitions.
% Friends - of different nationalities, call them differently and they like different
% kinds of sports. Michael prefers basketball and plays better than the American.
% Israeli David plays better than someone who plays tennis. The cricketer took first place.
% Who is an Australian? What kind of sport does Kostya do?
% =======================================================================================
better_than(X, Y, [X|T]) :- sadrzi(Y, T).
better_than(X, Y, [H|T]) :- better_than(X, Y, T).

% Nacionalnost, ime, sport
three_friends(L) :-
    L = [[_,_,cricket],[_,_,_],[_,_,_]],
    sadrzi([_,michael,basketball],L),
    sadrzi([_,kosta,_],L),
    sadrzi([australian,_,_], L),
    better_than([_,michael,basketball],[american,_,_], L),
    better_than([israeli,david,_],[_,_,tennis], L).


% =======================================================================================
% Napisati PROLOG program koji resava sledecu zagonetku. Cetiri gospodje se sastaju
% svakog cetvrtka da igraju bridz.
% Svaki put se dogovaraju ko ce sta da donese sledeci put.
% - Gospodja Andric ce doneti cokoladnu tortu.
% - Ni gospodja Brankovic, ni Vladislava nece doneti kolacice.
% - Ruska, koja nije Davidovic, ce doneti kafu.
% - Marija ce doneti vino.
% - Ana se preziva Petrovic
% Kako se koja gospodja zove i ko sta doneti sledece nedelje?
% =======================================================================================
% ime, prezime, donosi
gospodje(L):-
    L = [_, _, _, _],
    sadrzi([_, andric, cokoladnaT], L),
    sadrzi([ruska, _, kafa], L),
    sadrzi([marija, _, vino], L),
    sadrzi([ana, petrovic, _], L),
    sadrzi([_, brankovic, _], L),
    sadrzi([vladislava, _, _], L),
    sadrzi([_, davidovic, _], L),
    sadrzi([_, _, kolacice], L),
    \+(sadrzi([ruska, davidovic, _], L)),
    \+(sadrzi([_, brankovic, kolacice], L)),
    \+(([vladislava, _, kolacice],L)).    


% =======================================================================================
% =======================================================================================
% =======================================================================================
% Primeri za razgibavanje
% =======================================================================================

% Izracunati stepen broja.
stepen(_,0,1).
stepen(X,Y,R):- Y>0,
					 Y1 is Y-1,
					 stepen(X,Y1,R1),
					 R is R1*X.

% Odrediti NZD broja Euklidovim algoritamom.
nzd(M, 0, M).
nzd(M, N, D):- N > 0,
               N1 is (M mod N),
               nzd(N, N1, D).


% Odrediti faktorijel broja.
factoriel(0, 1).

factoriel(A, B):- A > 0,
                  C is A - 1,
                  factoriel(C, D),
                  B is A*D,
                  write(A),
                  write(' ').

% Obrni cifre broja.
obrni(N, N, P):- N < 10,
                 P is 10.
obrni(N, R, P):- N >= 10,
                 N1 is N // 10, 
                 obrni(N1, R1, P1),
                 R is (R1 + (N mod 10)*P1),
                 P is (P1*10).
                    

% Provera da li je broj prost.
prost(X):- X1 is X // 2, prost_pom(X, X1).

prost_pom(_, 1):- true.
prost_pom(X, B):- B > 0,
		          X mod B =\= 0,
		          B1 is B - 1,
		          prost_pom(X, B1).	            



             
aps3(X, X):- X >= 0, !. %koriscenje operatora "cut"
aps3(X, Y):- Y is -X.

% N-ti clan Fibonacijevog niza.
fibonaci(1, 1).
fibonaci(2, 1).
fibonaci(N, R):- N > 2, 
                 N1 is N - 1,
                 N2 is N - 2,
                 fibonaci(N1, R1),
                 fibonaci(N2, R2),
                 R is R1 + R2.
                 
% N-ti clan Fibonacijevog niza, verzija II (koriscenje cut operatora)
fibonaci2(1, 1):- !.
fibonaci2(2, 1):- !.
fibonaci2(N, R):- N1 is N - 1,
                  N2 is N - 2,
                  fibonaci2(N1, R1),
                  fibonaci2(N2, R2),
                  R is R1 + R2.  	

% Napisati prolog program koji recima ispisuje cifre broja.
% Na primer: 125 -- jedan dva pet
cif(0, nula).
cif(1, jedan).
cif(2, dva).
cif(3, tri).
cif(4, cetiri).
cif(5, pet).
cif(6, sest).
cif(7, sedam).
cif(8, osam).
cif(9, devet).

ispisi_cif(B):- B < 10,
                cif(B, X),
                write(X),
                nl, !.
                
ispisi_cif(B):- B1 is (B // 10),
                ispisi_cif(B1),
                B2 is (B mod 10),    
                cif(B2, X),
                write(X),
                nl.
                
start :- write('unesi prirodan broj \''),                
         read(X),
         provera(X),
         ispisi_cif(X).
           
provera(B):- B >= 0.
provera(B):- B < 0,
             write('Broj nije prirodan'),
             nl,
             fail.                  	      


% Prema Goldbahovoj hipotezi, svaki paran broj moze se napisati kao zbir dva
% prosta broja. Napisati PROLOG predikat koji za dati paran broj X odreduje
% njegove Goldbahove sabirke.

gol_pom(X1, Y1, X1, Y1):- prost(X1),
                       prost(Y1),
                       !.
gol_pom(X, Y, X1, Y1):- X2 is (X1 + 1),
                           Y2 is (Y1 - 1),
                           gol_pom(X, Y, X2, Y2).
gol(N, X, Y):- Y1 is (N-2),
               gol_pom(X, Y, 2, Y1).  



% Izdvanje prvih N elemenata liste
izdvoji(0, _, []):-!.
izdvoji(N, [G|R], [G|R1]):- N1 is N - 1,
                            izdvoji(N1, R, R1).

% Maksimalni element liste.
maxL1([X], X).
maxL1([G|R], Y):- maxL1(R, Y),
                  G < Y.
maxL1([G|R], G):- maxL1(R, Y),
                  G >= Y.        

% Unija dve liste.
unija(L1, L2, L):- spoji(L1, L2, L3), izbaciduple(L3, L).

% Presek listi.
presek([X|R], L2, [X|R1]):- presek(R, L2, R1),
                            sadrzi(L2, X), !.
presek([_|R], L2, R1):- presek(R, L2, R1).
presek([], _, []).

% Razlika listi.
razlika([], _, []).
razlika([X|R], L2, L3):- sadrzi(L2, X), razlika(R, L2, L3), !.
razlika([X|R], L2, [X|R1]):- razlika(R, L2, R1).    

% Napisati prolog predikat
% pairsums(L1, L2) koji za zadatu listu L1 vraca listu L2 ciji svaki clan je 
% suma elemenata liste L1 na susednim pozicijama. Na primer,
% ako je L1 [1,3,6,10], onda L2 treba da bude [4,9,16].
% Ako L1 sadrzi manje od dva elementa, L2 treba postaviti na
% praznu listu.

pairsums([X, Y|R], [G|R1]):- G is X + Y, pairsums([Y|R], R1).
pairsums([X], []).
pairsums([], []).                                  

% Napisati predikat pozneg koji za datu listu brojeva izracunava koliko se podniski kontstantnog znaka javlja u toj nisci.
pozneg([], 0).
pozneg([_], 1).
pozneg([X, Y|R], N):- pozneg([Y|R], N1),
                      X * Y < 0,
                      N is N1 + 1.
pozneg([X, Y|R], N):- pozneg([Y|R], N),
                      X * Y > 0.  

% Napisati predikat rotiraj koji ciklicno pomera elemente liste ulevo za N mesta. Pretpostaviti da N nije vece
% od duzine liste.

ubaci_na_kraj(X, [], [X]).
ubaci_na_kraj(X, [G|R], [G|R1]):- ubaci_na_kraj(X, R, R1).

rotiraj(L, 0, L):-!.
rotiraj([G|R], N, L):- ubaci_na_kraj(G, R, R1),
                       N1 is N - 1,
                       rotiraj(R1, N1, L).    


% Napisati predikat koji u listi L pronalazi pojavljivanja liste A i zamenjuje ih listom B.
podeli(L, [], L).
podeli([G|R], [G|R1], L):- podeli(R, R1, L).

podlista(_, []).
podlista([G|R], [G|R1]):- podlista(R, R1).

zameni1([], _, _, []).
zameni1(L1, L2, L3, L):- podlista(L1, L2),
                        podeli(L1, L2, Ost),
                        zameni1(Ost, L2, L3, LOst),
                        spoji(L3, LOst, L).
zameni1([G1|R1], L2, L3, [G1|R]):- \+(podlista([G1|R1], L2)),
                                  zameni1(R1, L2, L3, R).  



% Napisati predikat ciji su argumenti lista brojeva i tri broja a, b i c koji proverava da li se u listi
% pojavljuje broj b izmedju brojeva a i c.

izmedju(A, B, C, [G|R]):- G \== A,
                          izmedju(A, B, C, R).
izmedju(A, B, C, [A|R]):- izmedju(B, C, R).
izmedju(B, C, [G|R]):- B \== G,
                       izmedju(B, C, R).
izmedju(B, C, [B|R]):- izmedju(C, R).
izmedju(C, [G|R]):- G \== C,
                    izmedju(C, R).
izmedju(C, [C|_]).


% Napisati PROLOG predikat koji iz liste brojeva izdvaja elemente ciji su indeksi stepeni dvojke. Pretpostaviti
% da indeksi pocinju od 1.
izdvoj(L, X):- izdvoj(L, 1, 1, X).
izdvoj([], _, _, []).
izdvoj([G|R], N, N, [G|R1]):- N1 is N + 1,
                              N2 is N * 2,
                              izdvoj(R, N1, N2, R1).
izdvoj([G|R], I, S, L):- I \== S,
                         I1 is I + 1,
                         izdvoj(R, I1, S, L).


% Napisati predikat ubaci koji izlistava sve moguce nacine ubacivanja elementa u datu listu.
ubaci(X, [], [X]):-!. %videti sta se desava kada se izostavi !
ubaci(X, L, [X|L]).
ubaci(X, [G|R], [G|R1]):- ubaci(X, R, R1).


% Napisati predikat prebroj koji za datu listu listi proizvodi listu duzina tih listi.
duzina([], 0).
duzina([G|R], N):- duzina(R, N1),
                   N is N1 + 1.
                   
prebroj([], []).
prebroj([G|R], [N|R1]):- duzina(G, N),
                         prebroj(R, R1).
                         

% Napisati predikat minmax koji racuna minimum maksimuma elemanata liste listi.
% minmax([[1,2,3],[3,4,5],[2,3,4]],X)
maxL([X], X).
maxL([X|R], X):- maxL(R, X1),
                 X1 < X.
maxL([X|R], X1):- maxL(R, X1),
                  X1 >= X.
                  
minmax([G], X):- maxL(G, X).
minmax([G|R], Y):- maxL(G, Y),
                   minmax(R, X),
                   X >= Y.
minmax([G|R], X):- maxL(G, Y),
                   minmax(R, X),
                   X < Y.



% Ispisuje prvih N redova paskalovog trougla.
ispisi_listu([X|R]):- write(X), write(' '), ispisi_listu(R).
ispisi_listu([]):- nl.

pascal(N):- pascal(N, [1]).

pascal(0, L):- ispisi_listu(L), !.
pascal(N, L):- ispisi_listu(L),
               generisi_novu(L, L1),
               N1 is N - 1,
               pascal(N1, L1).

generisi_novu([X|R], [X|R1]):- generisi_novu1([X|R], R1).
generisi_novu1([X, Y|R], [Z|R1]):- Z is X + Y,
                                   generisi_novu1([Y|R], R1).
generisi_novu1([X], [X]):-!.


% Da li je lista sortirana?
sortirana([]):-!.
sortirana([_]):-!.
sortirana([X, Y|L]):- Y >= X,
                      sortirana([Y|L]).
               
                        
% qsort sort
napravi_particiju(_, [], [], []).
napravi_particiju(X, [G|R], [G|R1], L2):- G >= X,
                                          napravi_particiju(X, R, R1, L2).
napravi_particiju(X, [G|R], L1, [G|R1]):- G < X,
                                          napravi_particiju(X, R, L1, R1).
        
        
spoji_sortirano([], L, L).
spoji_sortirano(L, [], L).
spoji_sortirano([G1|R1], [G2|R2], [G1|R3]):- G1 < G2,
                                             spoji_sortirano(R1, [G2|R2], R3).
                                             
spoji_sortirano([G1|R1], [G2|R2], [G2|R3]):- G1 >= G2,
                                             spoji_sortirano([G1|R1], R2, R3).   
                                          
qsort([], []).
qsort([G|R], L):- napravi_particiju(G, R, L1, L2),
                  qsort(L1, L1S),
                  qsort(L2, L2S),
                  spoji_sortirano(L1S, [G|L2S], L).


