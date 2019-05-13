% ekstenzija BProlog fajla je .pl
% zbog problem sa serverom (ne otvara fajlove sa ekstenziom .pl)
% ekstenzija fajla koji se skida sa internet strane kursa je .pl(1)
% preimenovati fajl
% tj. obrisati (1)

% ako je u primer.pl napisan prolog program
% sa /home/BProlog/bp se pokrece Prolog intepreter
% [primer].
% se ukucava da bi se u intepreter consultovao napisani prolog program
% postoje  i drugi nacini (cl -- da se komapjlira  i ucita), ali 
% tada nije mooguce koristiti trace mode


%razlika izmedju = (unifikabilni), \= (nisu unifikabilni), ==(identicno jednaki termovi), \== (nisu identicno jednaki termovi)

op11(X, Y):- X = Y.

op12(X, Y):- X == Y.

%razlika izmedju is (aritmeticko izracunavanje) i =:= (aritmeticki jednaki); =\= - aritmeticki nisu jednaki
%op1(3,4).
%op1(3,3).
%op1(X,4).
%op1(4,X).
%op1(X,3*3).
%op1(3*3, 9).

op1(X, Y):- X is Y.

op2(X, Y):- X =:= Y.

%negotion as failure
%not(P):- call(P), !, fail.
%not(P).

%nezenja(P):- \+(ozenjen(P)), musko(P).
%razlicito od
%nezenja(P):- musko(P), \+(ozenjen(P)).

%musko(marko).
%musko(tomislav).

%ozenjen(tomislav).

%poredak ne sme da bude bitan
%ovakav program nije dobro pisati jer
%op3(N, N).
%op3(N, 0):- N < 10.
%ne daje isto.
%Najbolje je ograniciti se ovakvih greski i pisati
%op3(N, 0):- N < 10.
%op3(N, N):- N >= 10.
op3(N, 0):- N < 10.
op3(N, N).

%porodicno stablo
musko(dragan).
musko(dejan).
musko(dule).
musko(ilija).

zensko(milijana).
zensko(danijela).
zensko(zivka).
zensko(mirjana).
zensko(snezana).
zensko(radojka).

roditelj(dragan, dejan).
roditelj(dragan, danijela).
roditelj(milijana, danijela).
roditelj(milijana, dejan).
roditelj(ilija, milijana).
roditelj(radojka, milijana).
roditelj(ilija, dule).
roditelj(radojka, dule).
roditelj(dule, mirjana).
roditelj(dule, snezana).
roditelj(ilija, zivka).
roditelj(radojka, zivka).

otac(X, Y):- musko(X), roditelj(X, Y).
majka(X, Y):- zensko(X), roditelj(X, Y).

%findall(X, otac(X, Y), Res). -- u listu Res smesta sva moguca resenja za 
% promenljivu X koja ispunjava predikat otac(X, Y).

% trace -- omogucava da se prati izvrsavanje programa korak po korak
% notrace -- prekida se trace mod rada

predak(X, Y):- roditelj(X, Y).
predak(X, Y):- roditelj(X, Z), predak(Z, Y).

sestra(X, Y):- zensko(X), roditelj(Z, X), roditelj(Z, Y), X\==Y.
brat(X, Y):- musko(X), roditelj(Z, X), roditelj(Z, Y), X\==Y.

tetka(X, Y):- roditelj(Z,Y), sestra(X, Z).
ujak(X, Y):- majka(Z, Y), brat(X, Z).

sestraodujaka(X, Y):- ujak(Z, Y), roditelj(Z, X), zensko(X).

% Ko je udario macku Tunu?
% macka je zivotinja
% vlasnik psa voli zivotinje
% ne bi udario zivotinju ko voli zivotinje
% macku bi udario onaj koji bi je mozda udario i nije da je ne bi udario.
macka(tuna).
vlasnikpsa(janko).
mozda_udario(marko,tuna).
mozda_udario(janko,tuna).

zivotinja(X):-macka(X). 
volizivotinje(X):-vlasnikpsa(X).
ne_bi_udario(X,Y):-volizivotinje(X),zivotinja(Y).
udario(X,Y):-mozda_udario(X,Y), \+(ne_bi_udario(X,Y)).

%


%suma prvih N prirodnih brojeva
suma1(1, 1).
suma1(N, S):- N > 1,
              M is N - 1,
              suma1(M, S1),
              S is S1 + N. 
              
%suma cifara broja
suma2(N, N):- N < 10.
suma2(N, S):- N >= 10,
              M is N // 10,
	          suma2(M, S1),
	          S is S1 + (N mod 10). 
	          
%Euklidov algoritam
nzd(M, 0, M).
nzd(M, N, D):- N > 0,
               N1 is (M mod N),
               nzd(N, N1, D).

%faktorijel
factoriel(0, 1).

factoriel(A, B):- A > 0,
                  C is A - 1,
                  factoriel(C, D),
                  B is A*D,
                  write(A),
                  write(' ').
                  
%da li je godina prestupna
prestupna(G):- G mod 400 =:= 0.

prestupna(G):- G mod 4 =:= 0,
               G mod 100 =\= 0.     
               
broj_dana(januar, _, 31).
broj_dana(april, _, 30).
broj_dana(februar, X, 29):- prestupna(X).
broj_dana(februar, X, 28):- \+(prestupna(X)).
%itd za ostale mesece
                  
                  
%Hanojeve kule
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
                    
%obrni cifre broja
obrni(N, N, P):- N < 10,
                 P is 10.
obrni(N, R, P):- N >= 10,
                 N1 is N // 10, 
                 obrni(N1, R1, P1),
                 R is (R1 + (N mod 10)*P1),
                 P is (P1*10).
                    
%provera da li je broj prost
prost(X):- X1 is X // 2, prost_pom(X, X1).

prost_pom(X, 1):- true.
prost_pom(X, B):- B > 0,
		          X mod B =\= 0,
		          B1 is B - 1,
		          prost_pom(X, B1).
		          
%bojenje grafa
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


%apsolutna vrednost
%losa implementacija
aps1(X, X):- X >= 0.
aps1(X, Y):- Y is -X.

%dobre implementacija
aps2(X, X):- X >= 0.
aps2(X, Y):- X < 0,
             Y is -X.
             
aps3(X, X):- X >= 0, !. %koriscenje operatora "cut"
aps3(X, Y):- Y is -X.

%N-ti clan Fibonacijevog niza
fibonaci(1, 1).
fibonaci(2, 1).
fibonaci(N, R):- N > 2, 
                 N1 is N - 1,
                 N2 is N - 2,
                 fibonaci(N1, R1),
                 fibonaci(N2, R2),
                 R is R1 + R2.
                 
%N-ti clan Fibonacijevog niza, verzija II
fibonaci2(1, 1):- !.
fibonaci2(2, 1):- !.
fibonaci2(N, R):- N1 is N - 1,
                  N2 is N - 2,
                  fibonaci2(N1, R1),
                  fibonaci2(N2, R2),
                  R is R1 + R2.       
                  
%ispis cifara unetog broja
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
             
%Ko laze taj krade.
%Ko krade i uhvacen je u kradi taj ide u zatvor.
%Al Kapone laze.
%Al Kapone je uhvacen u kradi.
%Laki Luciano laze.
%Napisati PROLOG program koji opisuje navedene cinjenice i pravila. Koje odgovore PROLOG daje na upite
%”da li Al Kapone ide u zatvor” i ”da li Laki Luciano ide u zatvor”.

krade(X):- laze(X).
zatvor(X):- krade(X), uhvacen_u_kradji(X).

laze(alKapone).
uhvacen_u_kradji(alKapone).
laze(lakiLuciano).

%izracunati stepen broja
stepen(X,0,1).
stepen(X,Y,R):- Y>0,
					 Y1 is Y-1,
					 stepen(X,Y1,R1),
					 R is R1*X.

%Prema Goldbahovoj hipotezi, svaki paran broj moze se napisati kao zbir dva
%prosta broja. Napisati PROLOG predikat koji za dati paran broj X odreduje
%njegove Goldbahove sabirke.

gol_pom(X1, Y1, X1, Y1):- prost(X1),
                       prost(Y1),
                       !.
gol_pom(X, Y, X1, Y1):- X2 is (X1 + 1),
                           Y2 is (Y1 - 1),
                           gol_pom(X, Y, X2, Y2).
gol(N, X, Y):- Y1 is (N-2),
               gol_pom(X, Y, 2, Y1).   
               








  
