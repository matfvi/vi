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
sadrzi(X, [X|_]).
sadrzi(X, [_|R]) :- sadrzi(X, R).

resi(L) :-
    L = [[laza, pera, _], [X, _, peric], [mika, X, _], _],
    % uslov da postoje ocevi
    sadrzi([jova, _, _], L),
    sadrzi([pera, _, _], L),
    % uslov da postoje djeca
    sadrzi([_, jova, _], L),
    sadrzi([_, mika, _], L),
    sadrzi([_, laza, _], L),
    % uslovi za prezimena
    sadrzi([_, _, jovic], L),
    sadrzi([_, _, mikic], L),
    sadrzi([_, _, lazic], L),
    % ostatak uslova - prezimena i imena oceva
    \+(sadrzi([mika, _, mikic], L)),
    \+(sadrzi([pera, _, peric], L)),
    \+(sadrzi([jova, _, jovic], L)),
    \+(sadrzi([laza, _, lazic], L)),
    % ostatak uslova - prezimena i imena sinova
    \+(sadrzi([_, mika, mikic], L)),
    \+(sadrzi([_, pera, peric], L)),
    \+(sadrzi([_, jova, jovic], L)),
    \+(sadrzi([_, laza, lazic], L)),
    % TODO dodati u materijale :D
    \+(sadrzi([X, X, _], L))
    %\+(sadrzi([pera, pera, _], L)), 
    %\+(sadrzi([mika, mika, _], L)), 
    %\+(sadrzi([laza, laza, _], L)), 
    %\+(sadrzi([jova, jova, _], L))
    .

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
desno_od(X, Y, [G|R]) :- desno_od(X, Y, R).

pored(X, Y, L) :- desno_od(X, Y, L).
pored(X, Y, L) :- desno_od(Y, X, L).

resi2(L) :-
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
    sadrzi([_, _, _, orange, luckyStrike], L),
    sadrzi([_, japanese, _, _, parliament], L),
    sadrzi([_, _, _, water, _], L),
    sadrzi([_, _, zebra, _, _], L).
