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
clan(X, [X|_]).
clan(X, [G|R]) :- clan(X, R).

better_than(X, Y, [X|T]) :- clan(Y, T).
better_than(X, Y, [H|T]) :- better_than(X, Y, T).

% Nacionalnost, ime, sport
three_friends(L) :-
    L = [[_,_,cricket],[_,_,_],[_,_,_]],
    clan([_,michael,basketball],L),
    clan([_,kosta,_],L),
    clan([australian,_,_], L),
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
