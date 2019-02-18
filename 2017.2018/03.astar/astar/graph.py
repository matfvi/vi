#! /usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque

class MazeGraph:
    def __init__ (self, adjacency_list, heuristic):
        self.adjacency_list = adjacency_list
        self.marked = {}
        self.heuristic = heuristic

    # Uklanjanje oznaka sa svih cvorova
    def reset_marks(self):
        self.marked = {}

    # Nalazenje najkraceg puta izmedju cvorova start i stop pomocu Dijkstra algoritma
    def dijkstra(self, start, stop):
        # Q je skup ovorenih cvorova, inicijalno sadrzi sve cvorove grafa
        Q = set([v for v in self.adjacency_list])

        # D sadrzi tekuce udaljenosti od polaznog cvora (start) do ostalih cvorova, inicijalno beskonacne
        D = dict([(v, float('inf')) for v in self.adjacency_list])

        # Udaljenost polaznog cvora od samog sebe je 0
        D[start] = 0

        # Mapa parents cuva roditelje cvorova
        parents = {}
        for v in self.adjacency_list:
            parents[v] = None

        # Dok je skup Q neprazan:
        while len(Q) > 0:
            # Pronalazi se cvor sa najmanjoj udaljenoscu od polaznog cvora i uklanja iz Q
            n = None
            for w in Q:
                if n == None or (D[w] != float('inf') and D[w] < D[n]):
                    n = w

            # Ako ne postoji cvor cija je udaljenost manja od beskonacnosti put od polaznog do ciljnog cvora ne postoji
            if n == None:
                print('Path not found!')
                return []

            # Ako je n ciljni cvor, izvesti o uspehu i vrati resenje konstruisuci put
            # od polaznog do ciljnog cvora (iduci unazad — od ciljnog cvora).
            if n == stop:
                path = deque([])

                while parents[n] != None:
                    path.appendleft(n)
                    n = parents[n]

                # Dodajemo polazni cvor
                path.appendleft(start)

                return list(path)

            # Proveri da li je ustanovljeno rastojanje od polaznog cvora do m vece od rastojanja
            # od polaznog cvora do m preko cvora n i ako jeste, promeniti informaciju
            # o roditelju cvora m na cvor n i upamtiti novo rastojanje.
            for (m, weight) in self.adjacency_list[n]:
                if D[m] == float('inf') or D[n] + weight < D[m]:
                    D[m] = D[n] + weight
                    parents[m] = n

            Q.remove(n)

        #  Obavesti da trazeni put ne postoji (Q je prazan skup i uspeh nije prijavljen).
        print('Path not found!')
        return []

    def set_heuristic(self, H):
        self.H = H

    # Heuristika
    def h(self, n):
        return self.heuristic[n]

    # Pronalazenje najkraceg puta pomocu algoritma A*
    def astar(self, start, stop):
        # Zatvorena lista je inicijalno prazna, a otvorena lista sadrzi samo polazni cvor
        open_list = dict([(start, True)])
        closed_list = {}

        # g sadrzi tekuce udaljenosti od polaznog cvora (start) do ostalih cvorova, inicijalno beskonacne
        g = dict([(v, float('inf')) for v in self.adjacency_list])

        # Udaljenost polaznog cvora od samog sebe je 0
        g[start] = 0

        # Mapa parents cuva roditelje cvorova
        parents = {}
        for v in self.adjacency_list:
            parents[v] = None

        # Izvrsavaj dok god ima elemenata u otvorenoj listi
        while len(open_list) > 0:
            n = None

            for v in open_list:
                if g[v] != float('inf') and
                (n == None or g[v] + self.h(v) < g[n] +  self.h(n)):
                    n = v;

            if n == None:
                print("Path not found!")
                return []

            # Ako je n ciljni cvor, izvesti o uspehu i vrati resenje konstruisuci put
            # od polaznog do ciljnog cvora (iduci unazad — od ciljnog cvora).
            if n == stop:
                path = deque([])

                while parents[n] != None:
                    path.appendleft(n)
                    n = parents[n]

                # Dodajemo polazni cvor
                path.appendleft(start)

                return list(path)

            # Za svaki cvor m koji je direktno dostupan izn𝑛 uradi sledece:
            for (m, weight) in self.adjacency_list[n]:
                # Ako m nije ni u otvorenoj ni u zatvorenoj listi, dodaj ga u otvorenu listu
                # i oznaci n kao njegovog roditelja.
                if m not in open_list and m not in closed_list:
                    open_list[m] = True
                    parents[m] = n
                    g[m] = g[n] + weight

                # Inace, proveri da li je put od polaznog cvora do cvora m preko
                # cvora n bolji (kraci ili jeftiniji) od postojeceg puta do m
                # (trenutna vrednost g(m)). Ako jeste, promeni informaciju o roditelju
                # cvora m na cvor n i azuriraj vrednosti g(m), a ako je
                # m bio u zatvorenoj listi, prebaci ga u otvorenu.
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            del closed_list[m]
                            open_list[m] = True

            # Izbaci n iz otvorene liste i dodaj ga u zatvorenu listu
            del open_list[n]
            closed_list[n] = True

        #  Obavesti da trazeni put ne postoji (otvorena lista je prazna i uspeh nije prijavljen).
        print('Path not found!')
        return []

