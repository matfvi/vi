%napisati predikat prebroj koji za datu listu listi proizvodi listu duzina tih listi
duzina([], 0).
duzina([G|R], N):- duzina(R, N1),
                   N is N1 + 1.
                   
prebroj([], []).
prebroj([G|R], [N|R1]):- duzina(G, N),
                         prebroj(R, R1).
                         

%Napisati predikat minmax koji racuna minimum maksimuma elemanata liste listi
%minmax([[1,2,3],[3,4,5],[2,3,4]],X)
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



%ispisuje prvih N redova paskalovog trougla
ispisi_listu([X|R]):- write(X), write(' '), ispisi_listu(R).
ispisi_listu([]):- nl.

%paskalov trougao
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


%ispeglaj listu
%[1, 2, [3, 4], 5] --> [1, 2, 3, 4, 5]
spoj([],L2,L2).
spoj([H|T],L2,[H|R]):-spoj(T,L2,R).

ispeglaj([], []).
ispeglaj([H|R], L):- is_list(H), ispeglaj(H, L1), ispeglaj(R, L2), spoj(L1, L2, L).
ispeglaj([H|R], [H|R1]):- ispeglaj(R, R1).


%kombinacije 0 1, duzine N
kombinacije(0, []):-!.
kombinacije(N, [0|R]):- N1 is N - 1,
                        kombinacije(N1, R).
kombinacije(N, [1|R]):- N1 is N - 1,
                        kombinacije(N1, R).
                        

%da li je lista sortirana
sortirana([]):-!.
sortirana([_]):-!.
sortirana([X, Y|L]):- Y >= X,
                      sortirana([Y|L]).
               
                        
%qsort sort
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
                  
            
%da li je X clan liste L
clan(X, [X|_]).
clan(X, [_|R]):- clan(X, R).

%brisi element iz liste
brisi(X, [], []).
brisi(X, [X|R], R).
brisi(X, [G|R], [G|R1]):- G \== X,
                          brisi(X, R, R1).
                  
%permutacije
permutacije([], []).
permutacije(L, [X|R]):- clan(X, L),
                        brisi(X, L, L1),
                        permutacije(L1, R).




%kombinacije
kombinacije(_, 0, []).
kombinacije(L, N, [X|R]):- clan(X, L),
                           brisi(X, L, L1),
                           N1 is N - 1,
                           kombinacije(L1, N1, R).
                           
                           
%Napisati predikat pozneg koji za datu listu brojeva izracunava koliko se podniski kontstantnog znaka javlja u toj nisci
pozneg([], 0).
pozneg([_], 1).
pozneg([X, Y|R], N):- pozneg([Y|R], N1),
                      X * Y < 0,
                      N is N1 + 1.
pozneg([X, Y|R], N):- pozneg([Y|R], N),
                      X * Y > 0.       
%resenje popraviti tako da radi i ako niz sadrzi 0


%da li je lista palindrom
%obrni, pa uporedi da li su jednake

%Napisati predikat rotiraj koji ciklicno pomera elemente liste ulevo za N mesta. Pretpostaviti da N nije vece
%od duzine liste.

ubaci_na_kraj(X, [], [X]).
ubaci_na_kraj(X, [G|R], [G|R1]):- ubaci_na_kraj(X, R, R1).

rotiraj(L, 0, L):-!.
rotiraj([G|R], N, L):- ubaci_na_kraj(G, R, R1),
                       N1 is N - 1,
                       rotiraj(R1, N1, L).



%Napisati predikat koji u listi L pronalazi pojavljivanja liste A i zamenjuje ih listom B
spoji([], L, L).
spoji([G|R], L, [G|R1]):- spoji(R, L, R1).

podeli(L, [], L).
podeli([G|R], [G|R1], L):- podeli(R, R1, L).

podlista(_, []).
podlista([G|R], [G|R1]):- podlista(R, R1).

zameni([], _, _, []).
zameni(L1, L2, L3, L):- podlista(L1, L2),
                        podeli(L1, L2, Ost),
                        zameni(Ost, L2, L3, LOst),
                        spoji(L3, LOst, L).
zameni([G1|R1], L2, L3, [G1|R]):- \+(podlista([G1|R1], L2)),
                                  zameni(R1, L2, L3, R).
                        

%Napisati predikat ciji su argumenti lista brojeva i tri broja a, b i c koji proverava da li se u listi
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


%Napisati PROLOG predikat koji iz liste brojeva izdvaja elemente ciji su indeksi stepeni dvojke. Pretpostaviti
%da indeksi pocinju od 1
izdvoj(L, X):- izdvoj(L, 1, 1, X).
izdvoj([], _, _, []).
izdvoj([G|R], N, N, [G|R1]):- N1 is N + 1,
                              N2 is N * 2,
                              izdvoj(R, N1, N2, R1).
izdvoj([G|R], I, S, L):- I \== S,
                         I1 is I + 1,
                         izdvoj(R, I1, S, L).


%Napisati predikat ubaci koji izlistava sve moguce nacine ubacivanja elementa u datu listu
ubaci(X, [], [X]):-!. %videti sta se desava kada se izostavi !
ubaci(X, L, [X|L]).
ubaci(X, [G|R], [G|R1]):- ubaci(X, R, R1).




















                 













