#! /usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque

class Graph:

    def __init__ (self, adjacency_list):
        self.adjacency_list = adjacency_list
        self.marked = {}

    # Uklanjanje oznaka sa svih cvorova
    def reset_marks(self):
        self.marked = {}

    # Nalazenje puta izmedju cvorova start i stop pomocu pretrage u dubinu
    def DFS(self, start, stop):

        # Ponistavamo tekuce oznake cvorova
        self.reset_marks()

        # Polazni cvor se oznacava i dodaje na putanju
        self.marked[start] = True
        path = [start]

        # Dok putanja nije prazna uzima se cvor sa vrha steka, koji predstavlja tekucu putanju
        # i dodaje njegov prvi neoznaceni sused na stek
        while len(path) > 0:

            # v = path[-1:][0]      # nepotrebno
            # uzimamo vrh steka
            v = path[-1]

            # Ukoliko je na vrhu steka ciljni cvor (stop), vraca se sadrzaj steka koji predstavlja
            # put od cvora start do cvora stop
            if v == stop:
                return path

            has_unvisited = False

            for (w, weight) in self.adjacency_list[v]:
                if w not in self.marked:
                    path.append(w)
                    self.marked[w] = True
                    has_unvisited = True
                    break

            # Ako cvor nema vise neoznacenih suseda uklanja se sa steka
            if has_unvisited == False:
                path.pop()

    # Nalazenje puta izmedju cvorova start i stop pomocu pretrage u sirinu
    def BFS(self, start, stop):

        # Ponistavamo tekuce oznake cvorova
        self.reset_marks()

        # Polazni cvor (start) se oznacava i dodaje u red
        self.marked[start] = True
        queue = deque([start])

        # TODO jel ovo neophodno
        # Mapa parents cuva roditelje cvorova
        parents = {}
        for v in self.adjacency_list:
            parents[v] = None

        # Dok red nije prazan uklanjamo cvor sa pocetka reda i dodajemo u red njegove neoznacene susede
        while len(queue) > 0:
            v = queue.popleft()

            # Ako je na vrhu reda ciljni cvor (stop), rekonstruise se putanja do njega
            if v == stop:

                path = deque([])

                # do-while petlja ne postoji u Python-u
                while parents[v] != None:
                    path.appendleft(v)
                    v = parents[v]

                # Dodajemo polazni cvor
                path.appendleft(v)

                return list(path)

            # U suprotnom, oznacavamo i dodajemo u red sve neoznacene susede cvora sa pocetka reda
            for (w, weight) in self.adjacency_list[v]:
                if w not in self.marked:
                    self.marked[w] = True
                    parents[w] = v
                    queue.append(w)

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

            if n == stop:
                path = deque([])

                # do-while petlja ne postoji u Python-u
                while parents[n] != None:
                    path.appendleft(n)
                    n = parents[n]

                # Dodajemo polazni cvor
                path.appendleft(start)

                return list(path)

            # proveri da li je ustanovljeno rastojanje od polaznog cvora do m vece od rastojanja
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


    # Heuristika
    def h(self, n):
        H = {
                0 : 2,
                1 : 0,
                2 : 1
                }

        return H[n]

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
                if g[v] != float('inf') and (n == None or g[v] + self.h(v) < g[n] +  self.h(n)):
                    n = v;

            if n == None:
                print("Path not found!")
                return []

            # Ako je n ciljni cvor, izvesti o uspehu i vrati resenje konstruisuci put
            # od polaznog do ciljnog cvora (iduci unazad — od ciljnog cvora).
            if n == stop:
                path = deque([])

                # do-while petlja ne postoji u Python-u
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
            closed_list[m] = True

        #  Obavesti da trazeni put ne postoji (otvorena lista je prazna i uspeh nije prijavljen).
        print('Path not found!')
        return []

