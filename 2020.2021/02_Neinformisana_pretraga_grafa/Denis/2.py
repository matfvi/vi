import json
from queue import LifoQueue
from queue import Queue

def ucitaj_graf(putanja):
    try:
        with open(putanja, "r") as f:
            podaci = json.load(f)
            return dict(podaci)
    except:
        print("Greska!")
        return None

def dfs_obilazak(G, pocetak):
    stek = LifoQueue()
    stek.put(pocetak)
    poseceni = {pocetak}
    putanja = []
    putanja.append(pocetak)
    while not stek.empty():
        n = stek.get()
        if n not in poseceni:
            poseceni.add(n)
            putanja.append(n)

        for cvor, _ in G[n]:
            if cvor not in poseceni:
                stek.put(cvor)
    return putanja

def dfs(G, pocetak, kraj, putanja, poseceni):
    putanja.append(pocetak)
    poseceni.add(pocetak)

    if pocetak == kraj:
        return putanja
    for m, _ in G[pocetak]:
        if m not in poseceni:
            result = dfs(G, m, kraj, putanja, poseceni)
            if result != None:
                return result

    putanja.pop()
    return None

def bfs(G, pocetak, kraj):
    red = Queue()
    red.put(pocetak)
    roditelji = {pocetak: None}

    while not red.empty():
        n = red.get()
        if n == kraj:
            putanja = [n]
            tmp = roditelji[n]
            while tmp != None:
                putanja.append(tmp)
                tmp = roditelji[tmp]
            putanja.reverse()
            return putanja
        for cvor, _ in G[n]:
            if cvor not in roditelji:
                roditelji[cvor] = n
                red.put(cvor)

    return []


def bfs_pretraga(G, pocetak):
    red = Queue()
    red.put(pocetak)
    putanja = []
    roditelji = {pocetak: None}

    while not red.empty():
        n = red.get()
        putanja.append(n)
        for cvor, _ in G[n]:
            if cvor not in roditelji:
                roditelji[cvor] = n
                red.put(cvor)
    return putanja

def dijsktra(G, pocetak, kraj):
    Q = set(G.keys())
    cene = {}
    for cvor in Q:
        cene[cvor] = float('inf')
    cene[pocetak] = 0

    roditelji = {}
    for v in Q:
        roditelji[v] = None
    iteration = 0
    while len(Q) > 0:
        iteration += 1
        n = None
        for w in Q:
            if n == None or (cene[w] != float('inf') and cene[w] < cene[n]):
                n = w
        Q.remove(n)
        if n == kraj:
            print("Broj iteracija")
            print(iteration)
            putanja = [n]
            tmp = roditelji[n]
            while tmp != None:
                putanja.append(tmp)
                tmp = roditelji[tmp]
            putanja.reverse()
            return putanja
        for m, tezina in G[n]:
            if cene[m] == float('inf') or cene[n] + tezina < cene[m]:
                cene[m] = cene[n] + tezina
                roditelji[m] = n
    return []

def main():
    G = ucitaj_graf("cities.json")

    print("--------DFS------")
    print(dfs_obilazak(G, "Oradea"))
    print(dfs(G, "Arad", "Lasi", [], set()))
    print("--------BFS------")
    print(bfs_pretraga(G, "Timisoara"))
    print("--------BFS---------")
    print(bfs(G, "Arad", "Lasi"))
    print("------Dijsktra------")
    print(dijsktra(G, "Arad", "Buchares"))
if __name__ == "__main__":
    main()
