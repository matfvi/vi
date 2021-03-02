# Tematika
- Uvod u VI
    - Bodovanje
    - Primena vestacke inteligencije
- Uvod u Python
    - [Jupyter notebook](https://jupyter.org/)
    - Podsecanje na osnovne Python-a
    - OOP koncepti u Python-u

## Uvod u VI

### Primena vestacke inteligencije
- [Coloring graph using SAT](https://www.youtube.com/watch?v=0gt503wK7AI&t=194s)
- [Resavanje igre SUDOKU koristeci SAT](https://github.com/lakshayg/sudoku)
- [DeepMind Parkour](https://www.youtube.com/watch?v=g59nSURxYgk)
- [AI igra Marija](https://www.youtube.com/watch?v=A97HL3_fxyo)
- [AlphaZero masters chess](https://www.youtube.com/watch?v=0g9SlVdv1PY)
- [AI learns to play snake](https://www.youtube.com/watch?v=3bhP7zulFfY)
- [AI learns to drive in GTA V](https://www.youtube.com/watch?v=edWI4ZnWUGg)
- [AI learns to play 2048](https://www.youtube.com/watch?v=JQut67u8LIg)
- [Dijkstra vs Astar vs Concurent Dijstra](https://www.youtube.com/watch?v=cSxnOm5aceA)
- [Astar vs Dikstra](https://www.youtube.com/watch?v=g024lzsknDo)
- [Pathfinding algorithms in Java](https://www.youtube.com/watch?v=CLbqqb53DLA&app=desktop)
- [JumpPointSearch+](https://www.gdcvault.com/play/1022094/JPS-Over-100x-Faster-than)
- [Ant optimization](https://www.youtube.com/watch?v=eVKAIufSrHs)
- [Particle swarm optimization](https://www.youtube.com/watch?v=gkGa6WZpcQg)
- [cleverbot](http://www.cleverbot.com/)
- [Genetic algorithm learns to walk](https://www.youtube.com/watch?v=uwz8JzrEwWY)
- [Genetic algoritm grows a car](https://www.youtube.com/watch?v=FKbarpAlBkw)
- [Genetic algorithm pathfinding](https://www.youtube.com/watch?v=BKF7pGw8qbY&app=desktop)

### Instalacija jupyter notebook
Jupyter notebook je open source veb aplikacija koja omogućava interaktivno pisanje i pokretanje Python koda.
Instalira se kao python paket koristeći `pip`.

Najpre, potrebno je instalirati pip za python 3.

Ubuntu:
```bash
sudo apt-get install python-pip3
```

Potom instalirati jupyter paket.

```bash
sudo pip3 install jupyter
```

Dalje je potrebno pozicionirati se u direktorijum koji želite da bude koreni direktorijum za jupyter, na primer:

```bash
cd /home/vi/
mkdir jupyter-test
cd jupyter-test
jupyter notebook
```
Naredba `jupyter notebook` će pokrenuti jupyter server u konzoli gde je ukucana i istovremenmo pokrenuti podrazumevani
veb pregledač koji će povezati na (verovatno) na `localhost:8888`.

