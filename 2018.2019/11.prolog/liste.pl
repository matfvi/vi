%[1, 2, 3, 4]
%[] - prazna lista
%[1, [2, 3], 4]
%[G|R] [1, 2, 3, 4] G = 1 R=[2, 3, 4]
%[1] G = 1 R=[]
%[[1, 2], 4] G = [1, 2] R = [4]

%dodaj elemnt na pocetak  liste
dodaj(X, L, [X|L]).

%dodaj element na kraj liste
%[X, Y|R] X=1 Y = 2 R=[3, 4]
dodaj_na_kraj(X, [], [X]).
dodaj_na_kraj(X, [G|R], [G|LR]):- dodaj_na_kraj(X, R, LR).

%da li lista sadrzi dati element
sadrzi1(X, [X|_]):- !.
sadrzi1(X, [G|R]):- G \== X,
                    sadrzi1(X, R).
                   
%spajanje dve liste
%spoji(L1, L2, L)
spoji([], L, L).
spoji([G|R], L, [G|LR]):- spoji(R, L, LR).

%zameniti dva elementa liste
%zameni(X, Y, L, LR) 
%zameni X sa Y u L da dobijemo LR
%X = 2, Y= 3 [1, 2, 2, 4] [1, 3, 3, 4]

zameni(X, Y, [X|R], [Y|R1]):- zameni(X, Y, R, R1).
zameni(X, Y, [G|R], [G|R1]):- G \== X,
                              zameni(X, Y, R, R1).
zameni(X, Y, [], []).


%brisanje elemenata liste
%brisi(X, L, LR) - X brise iz L da dobijemo LR

brisi(X, [], []).
brisi(X, [X|R], R1):- brisi(X, R, R1).
brisi(X, [G|R], [G|R1]):- G \== X,
                          brisi(X, R, R1).
                          
                         

%brisi samo prvo pojavljivanje

brisi1(X, [], []).
brisi1(X, [X|R], R):- !.
brisi1(X, [G|R], [G|R1]):- G \== X,
                           brisi1(X, R, R1).


%obrtanje liste
%[1, 2, 3]  [3, 2, 1]
obrni(L, LR):- obrni(L, [], LR).
obrni([], L, L).
obrni([G|R], L, LR):- obrni(R, [G|L], LR).


%provera da li su tri elemnta uzastopni elementi liste
%1 2 3 [4, 1, 2, 3] da
%uzastopni(X, Y, Z, L).

uzastopni(X, Y, Z, [X, Y, Z|_]):- !.
uzastopni(X, Y, Z, [_|R]):- uzastopni(X, Y, Z, R).

%izdvanje prvih N elemenata liste
%izdvoji(N, L, LR) LR ima N prvih elemenata

izdvoji(0, _, []):-!.
izdvoji(N, [G|R], [G|R1]):- N1 is N - 1,
                            izdvoji(N1, R, R1).
                            
%podeliti listu na dve liste - listu pozitivnih
%i listu negativnih elemenata
%podeli(L, L1, L2) - L1 lista pozitivnih
%L2 lista negativnih.

podeli([], [], []).
podeli([G|R], [G|R1], LN):- G >= 0,
                            podeli(R, R1, LN).
podeli([G|R], LP, [G|R1]):- G < 0,
                            podeli(R, LP, R1).
                            
%podeliti listu na sve moguce nacine
%[1, 2, 3] 
%[] [1, 2, 3]
%[1] [2, 3]
%[1, 2] [3]
% itd....
%podeli(L, L1, L2).

podeli1([], [], []).
podeli1([G|R], [G|R1], Y):- podeli1(R, R1, Y).
podeli1([G|R], X, [G|R1]):- podeli1(R, X, R1).

%maksimalni element liste
%maxL(L, X)

maxL([X], X).
maxL([G|R], X):- maxL(R, Y),
                 G < Y,
                 X is Y.
maxL([G|R], X):- maxL(R, Y),
                 G >= Y,
                 X is G.


maxL1([X], X).
maxL1([G|R], Y):- maxL1(R, Y),
                  G < Y.
maxL1([G|R], G):- maxL1(R, Y),
                  G >= Y.
                  
                  
%Cetiri coveka se zovu Pera, Mika, Laza i Jova, 
%a prezivaju Peric,
%Mikic, Lazic i Jovic. Oni imaju cetiri sina koji se 
%takodje
%zovu Pera, Mika, Laza i Jova. Pretpostavimo sledece:
%(a) Niko od oceva se ne zove u skladu 
%sa svojim prezimenom.
%(b) Niko od sinova se ne zove u skladu sa 
%svojim prezimenom.
%(c) Niko od sinova se ne zove isto kao i otac.
%(d) Peric stariji se zove isto kao Mikin sin.
%(e) Lazin sin se zove Pera.
%Napisati predikat koji odredjuje imena oceva i sinova.

%ime oca, ime sina, prezime
resi(L):- L= [[laza, pera, _], [X, _, peric], [mika, X, _], _],
             sadrzi([jova, _, _], L),
             sadrzi([pera, _, _], L),
             sadrzi([_,laza, _], L),
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

% Who owns the zebra?
%color, nationality, pets, drink, ciggarette - order

%desno_od(X, Y, L) - X desno od Y u listi L
desno_od(X, Y, [Y, X|R]).
desno_od(X, Y, [G|R]):- desno_od(X, Y, R).

pored(X, Y, L):- desno_od(X, Y, L).
pored(X, Y, L):- desno_od(Y, X, L).

sadrzi(X, [X|_]).
sadrzi(X, [G|R]):- sadrzi(X, R).

resi1(L):- L=[[_, norwegian, _, _, _], [blue, _, _, _, _], [_, _, _, milk, _], _, _],
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

%unija dve liste
unija(L1, L2, L):- spoji(L1, L2, L3), izbaciduple(L3, L).

%presek listi
presek([X|R], L2, [X|R1]):- presek(R, L2, R1),
                            sadrzi(L2, X), !.
presek([_|R], L2, R1):- presek(R, L2, R1).
presek([], _, []).

%razlika listi
razlika([], _, []).
razlika([X|R], L2, L3):- sadrzi(L2, X), razlika(R, L2, L3), !.
razlika([X|R], L2, [X|R1]):- razlika(R, L2, R1).


%Napisati PROLOG program koji resava sledecu zagonetku. Cetiri gospodje se sastaju
%svakog cetvrtka da igraju bridz. Svaki put se dogovaraju ko  ce sta da donese sledeci
%put.
%Gospodja Andric ce doneti cokoladnu tortu.
%Ni gospodja Brankovic, ni Vladislava nece doneti kolacice.
%Ruska, koja nije Davidovic, ce doneti kafu.
%Marija nece doneti vino.
%Kako se koja gospodja zove i ko sta doneti slede ce nedelje?

% ime, prezime, donosi
resi5(L):- L = [_, _, _, _],
           clan([_, andric, cokoladnaT], L),
           clan([ruska, _, kafa], L),
           clan([marija, _, vino], L),
           clan([ana, petrovic, _], L),
           clan([_, brankovic, _], L),
           clan([vladislava, _, _], L),
           clan([_, davidovic, _], L),
           clan([_, _, kolacice], L),
           \+(clan([ruska, davidovic, _], L)),
           \+(clan([_, brankovic, kolacice], L)),
           \+(clan([vladislava, _, kolacice],L)).


% pairsums(L1, L2) koji za zadatu listu L1 vraca listu L2
% suma elemenata liste L1 na susednim pozicijama. Na primer,
% ako je L1 [1,3,6,10], onda L2 treba da bude [4,9,16].
% Ako L1 sadrzi manje od dva elementa, L2 treba postaviti na
% praznu listu.

pairsums([X, Y|R], [G|R1]):- G is X + Y, pairsums([Y|R], R1).
pairsums([X], []).
pairsums([], []).


           
