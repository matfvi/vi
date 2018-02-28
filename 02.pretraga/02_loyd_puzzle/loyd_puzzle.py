#! /usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque
import copy


class Puzzle():

    def __init__(self, start_state):
        self.current_state = start_state
        self.end_state = [[1,2,3],[4,5,6],[7,8,0]]

    def neighbours(self, current_state):

        neighbour_states = []

        empty_position_i = None
        empty_position_j = None

        # Trazimo poziciju praznog polja (moglo bi se ubrzati cuvanjem trenutne pozicije, no ovako deluje lakse za razumevanje)
        # DOMACI ZA STUDENTE: Da li mozete elegantnije napisati kod za pretragu praznog polja?
        for i in range(len(current_state)):
            for j in range(len(current_state[i])):
                if current_state[i][j] == 0:
                    empty_position_i = i
                    empty_position_j = j

        # Ispituje se da li se praznog polje moze pomeriti gore,
        # ako moze, generisemo novu matricu koja nastaje pomeranjem praznog polja gore.
        if empty_position_i - 1 >= 0:
            new_neighbour_top = copy.deepcopy(current_state)
            new_neighbour_top[empty_position_i][empty_position_j] = new_neighbour_top[empty_position_i-1][empty_position_j]
            new_neighbour_top[empty_position_i-1][empty_position_j] = 0
            neighbour_states.append(new_neighbour_top)

        if empty_position_i + 1 <= 2:
            new_neighbour_bottom = copy.deepcopy(current_state)
            new_neighbour_bottom[empty_position_i][empty_position_j] = new_neighbour_bottom[empty_position_i+1][empty_position_j]
            new_neighbour_bottom[empty_position_i+1][empty_position_j] = 0
            neighbour_states.append(new_neighbour_bottom)

        if empty_position_j - 1 >= 0:
            new_neighbour_left = copy.deepcopy(current_state)
            new_neighbour_left[empty_position_i][empty_position_j] = new_neighbour_left[empty_position_i][empty_position_j-1]
            new_neighbour_left[empty_position_i][empty_position_j-1] = 0
            neighbour_states.append(new_neighbour_left)

        if empty_position_j + 1 <= 2:
            new_neighbour_right = copy.deepcopy(current_state)
            new_neighbour_right[empty_position_i][empty_position_j] = new_neighbour_right[empty_position_i][empty_position_j+1]
            new_neighbour_right[empty_position_i][empty_position_j+1] = 0
            neighbour_states.append(new_neighbour_right)

        # Rezultat rada je lista matrica ciji su elementi susedna stanja puzle.
        return neighbour_states


    def serialize_state(self, state):
        """
        Serijalizuje matricu (stanje igre) u string
        [[1,2,3],
         [4,5,6],
         [7,8,0]]
        = "123456890"

        Koristi se kako bi se cuvale informacije o posecenim stanjima/cvorovima.
        """

        serialized_state = ""

        for i in range(len(state)):
            for j in range(len(state[i])):
                serialized_state += str(state[i][j])

        return serialized_state


    def solveBFS(self):
        """Resava Lojdovu slagalicu koristeci pretragu u sirinu."""
        marked = {}

        # Polazni cvor (start) se oznacava i dodaje u red
        marked[self.serialize_state(self.current_state)] = True
        queue = deque([self.current_state])

        # Mapa parents cuva roditelje cvorova
        parents = {}

        # Dok red nije prazan uklanjamo cvor sa pocetka reda i dodajemo u red njegove neoznacene susede
        while len(queue) > 0:
            v = queue.popleft()

            # Ako je na vrhu reda ciljni cvor (stop), rekonstruise se putanja do njega
            if self.serialize_state(v) == self.serialize_state(self.end_state):

                path = deque([])

                while self.serialize_state(v) in parents:
                    path.appendleft(v)
                    v = parents[self.serialize_state(v)]

                # Dodajemo polazni cvor
                path.appendleft(v)

                return list(path)

            # U suprotnom, oznacavamo i dodajemo u red sve neoznacene susede cvora sa pocetka reda
            for w in self.neighbours(v):
                if self.serialize_state(w) not in marked:
                    marked[self.serialize_state(w)] = True
                    parents[self.serialize_state(w)] = v
                    queue.append(w)


    def solveDFS(self):

        # Mapa koja cuva podatke o stanjima koje smo posetili.
        marked = {}

        # Oznacavamo tekuce stanje kao poseceno.
        marked[self.serialize_state(self.current_state)] = True

        # Zapocinjemo konstrukciju puta.
        path = [self.current_state]

        # Dok putanja nije prazna (putanja se ponasa kao stek)
        # uzima se cvor sa vrha steka, koji predstavlja tekucu putanju
        # i dodaje njegov prvi neoznaceni sused na stek
        while len(path) > 0:
            v = path[-1]

            # Ukoliko je na vrhu steka ciljni cvor (stop), vraca se sadrzaj
            # steka koji predstavlja put od cvora start do cvora stop
            if self.serialize_state(v) == self.serialize_state(self.end_state):
                return path

            has_unvisited = False

            for w in self.neighbours(v):
                if self.serialize_state(w) not in marked:
                    path.append(w)
                    marked[self.serialize_state(w)] = True
                    has_unvisited = True
                    break

            # Ako cvor nema vise neoznacenih suseda uklanja se sa steka
            if has_unvisited == False:
                path.pop()


def show_solution(solution):
    if solution == None:
        print('No solution!')
    else:
        for i in solution:
            print(i)
        print("Solved in %d steps" % len(solution))

