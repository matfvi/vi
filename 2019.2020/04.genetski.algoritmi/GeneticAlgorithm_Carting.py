"""
Kako pravimo animaciju potrebno je ukljuciti neke pakete.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import copy
import random
import string

class Chromosome:
    '''
    Klasa predstavlja jedan hromozom za koji se cuva njegov genetski kod i vrednost funkcije prilagodjenosti.
    '''
    def __init__(self, content, fitness):
        self.content = content
        self.fitness = fitness
    
    def __str__(self):
        return "%s f=%d" % (self.content, self.fitness)


class GeneticAlgorithm:
    def __init__(self, mapa):
        self.map = mapa
        
        self._allowed_gene_values = [0, 1, 2, 3, 4] 

        '''Parametri genetskog algoritma, proizvoljno izabrani.'''
        self.generation_size = 30              # Broj jedinki u jednoj generaciji
        self.chromosome_size = 32              # Duzina hromozoma
        self.reproduction_size = 20            # Broj jedinki koji ucestvuje u reprodukciji    
        self.max_iterations = 10000             # Maksimalni dozvoljeni broj iteracija
        self.mutation_rate = 0.1               # Verovatnoca da se desi mutacija
        self.tournament_size = 10              # Velicina turnira
        self.cross_rate = 0.6                  # Verovatnoca za odabir bita prvog roditelja pri ukrstanju
        self.minimal_target_fitness = 50       # Minimalna prilagodjenost koju mora da zadovoljava resenje


        # Vrsta selekcije, moze biti turnirska (tournament) ili ruletska (roulette)
        self.selection_type = 'tournament' 
        
        '''Deo potreban za animaciju (ignorisati)'''
        self.arr = np.array([])
        self.i   = 0
        self.num_of_matrices = 0
        self.fig = plt.figure()

    
    """
        Generisemo generation_size nasumicnih jedinki kao instance klase Chromosome i vracamo ih u listi.
        Svaki hromozom je duzine 32 i moze imati samo vrednosti [0, 1, 2, 3, 4].
    """
    def initial_population(self):
        populacija = []
        
        for i in range(self.generation_size):
            hromozom = []
            for i in range(self.chromosome_size): #svaki hromozom je duzine 32
                # Biramo jednu vrednost iz skupa [0, 1, 2, 3, 4]
                value = random.choice(self._allowed_gene_values)
                hromozom.append(value)
                
            fitness = self.fitness(hromozom)
            populacija.append(Chromosome(hromozom, fitness))
            
        return populacija


    def selection(self, population):
        selected = []

        for i in range(self.reproduction_size):
            if self.selection_type == 'tournament':
                selected.append(self.tournament_selection(population))
            else:
                selected.append(self.roulette_selection(population))

        return selected


    def roulette_selection(self, population):
        total_fitness = sum([x.fitness for x in population])

        # slucaj broj
        random_value = random.random()

        for i in range(self.generation_size):
            if population[i].fitness/total_fitness > random_value:
                return population[i]


    def tournament_selection(self, population):
        # Biramo self.tournament_size nasumicnih jedinki iz populacije i trazimo jedinku
        # koja ima najvecu funkciju prilagodjenosti
        # Ovo predstavlja jednu od varijanti turnirske selekcije.

        selected = random.sample(population, self.tournament_size)

        winer = max(selected, key = lambda x: x.fitness)

        return winer


    def create_generation(self, selected):
        generation = []
        generation_size = 0

        while generation_size < self.generation_size:
            # Proizvoljno se biraju 2 roditelja za ukrstanje
            [parent1, parent2] = random.sample(selected, 2)

            # Dobijaju se 2 detata ukrstanjem
            child1_code, child2_code = self.crossover(parent1, parent2)

            # Vrsi se mutacija nad decom
            child1_code = self.mutation(child1_code)
            child2_code = self.mutation(child2_code)

            # Prave se novi hromozomi
            child1 = Chromosome(child1_code, self.fitness(child1_code))
            child2 = Chromosome(child2_code, self.fitness(child2_code))
            
            # Dodaju se u generaciju
            generation.append(child1)
            generation.append(child2)
            
            generation_size += 2
            
        return generation

    """
        Vrsi uniformno ukrstanje po verovatnoci self._crossover_p i vraca 2 nove jedinke.
    """
    def crossover(self, parent1, parent2):
        child1 = []
        child2 = []

        for i in range(self.chromosome_size):
            p = random.random()
            if p < self.cross_rate:
                child1.append(parent1.content[i])
                child2.append(parent2.content[i])
            else:
                child1.append(parent2.content[i])
                child2.append(parent1.content[i])

        return child1, child2


    '''Vrsi mutaciju nad hromozomom sa verovatnocom self._mutation_rate.
       Mutacija se vrsi nad jednim genom (karakterom) sa proizvoljnim indeksom.
    '''
    def mutation(self, child):
        random_value = random.random()

        if random_value < self.mutation_rate:
            random_index = random.randrange(1, self.chromosome_size)   

            while True:
                new_value = random.choice(self._allowed_gene_values)

                if child[random_index] != new_value:
                    break

            child[random_index] = new_value

        return child

    

    '''Izvrsavanje genetskog algoritma'''
    def optimize(self):
        population = self.initial_population()
        
        for i in range(self.max_iterations):
            # Selekcija (ruletska ili turnirska)
            selected = self.selection(population)

            # Kreiraj generaciju ukrstanjem i mutacijom
            population = self.create_generation(selected)
            
            best_chromosome = max(population, key=lambda x: x.fitness)
            print(best_chromosome.fitness)
            # self.animate_map(best_chromosome.content)            

            if best_chromosome.fitness >= self.minimal_target_fitness:
                break
         
        self.animate_map(best_chromosome.content)   
        return best_chromosome



    
    '''Izracunava prilagodjenost. U ovom primeru se gleda da li akcije koje su predlozene za svako stanje 
       dovode najbrzem prelasku puta po datoj trajektoriji ili da li auto uspe da zavrsi trku i obidje ceo krug.
    '''
    def fitness(self, hromozom):
        # Pocetna pozicija
        x = 2
        y = 2
        
        # Pocetni pravac kretanja
        pravacx = 1
        pravacy = 0
        
        # Pocetna brzina
        brzina  = 0
        
        # Ukupna brzina (sto je vrednost veca to je bolje)
        ukupna_brzina = 0
        
        while True:
            # Vozimo prema trenutnim parametrima (pomerimo karting)
            x = x + pravacx
            y = y + pravacy
            
            ukupna_brzina += brzina
            
            # Ukoliko smo se vratili na start, izvozali smo ceo krug, znaci sve akcije su 
            # bile dobre. Takvom hromozomu dajemo dodatnu prednost (odnosno += 44)
            if x == 2 and y == 2:
                ukupna_brzina += 44
                return ukupna_brzina
            
            # A mozda smo se zakucali u zid
            if self.map[y][x] == 0:
                return ukupna_brzina
            
            
            #Naredni redovi odredjuju trenutno stanje
            
            # Ispitivanje da li je na polju ispred zid (oznacen 0) ili put (oznacen 1)
            polje_ispred = self.map[y + pravacy][x + pravacx]
            
            # Ispitivanje da li je na dva polja ispred zid (oznacen 0) ili put (oznacen 1)
            dva_polje_ispred = self.map[y + 2*pravacy][x + 2*pravacx]
            
            # Ispitivanje sta je levo od trenutne pozicije
            levo = self.map[y - pravacx][x + pravacy]
            
            #Ispitivanje sta je desno od trenutne pozicije
            desno = self.map[y + pravacx][x - pravacy]
            
            # Odredjujemo indeks stanja u hromozomu
            indeks = 16*brzina + 8*polje_ispred + 4*dva_polje_ispred + 2*levo + desno            
            
            # U hromozom[indeks] je akcija koja se preduzima i moze biti neka od vrednosti [0, 1, 2, 3, 4]
            # Ako je 0 nema akcije -- nastavlja se istom brzinom u istom pravcu
            # U ostalim slucajevima ima promene koje se mogu videti
            if hromozom[indeks] == 1:
                # smanji brzinu
                brzina = 0
            elif hromozom[indeks] == 2:
                # povecaj brzinu
                brzina = 1
            elif hromozom[indeks] == 3:
                # skrenuti levo, ali samo ako je brzina 1, tj. ako brzo vozi ne moze se skrenuti
                if brzina == 0:
                    pomocna = pravacx
                    pravacx = pravacy
                    pravacy = -pomocna
            elif hromozom[indeks] == 4:
                # skrenuti desno, ali samo ako je brzina 1, tj. ako brzo vozi ne moze se skrenuti
                if brzina == 0:
                    pomocna = pravacx
                    pravacx = -pravacy
                    pravacy = pomocna
                    
        return ukupna_brzina
                    
    
    """
    Deo za animaciju matrice -- mape kuda vozimo karting. 
    (Iako prilicno interesatno, ova funkcija ne spada u obaveze kursa i sluzi samo za vizuelizaciju. 
    Stoga nije neophodno uciti i ne dolazi na ispitu/kolokvijumu.)
    """  
    def animate_map(self, hromozom):
        iterator = 0
        arr = []
        
        # Pocetna pozicija
        x = 2
        y = 2
        
        # Pocetni pravac kretanja
        pravacx = 1
        pravacy = 0
        
        # Pocetna brzina
        brzina  = 0
        
        mapa2 = copy.deepcopy(self.map)
        # mapa2 = [[200 for x in row if x == 0] for row in mapa2]
        for i in range(10):
            for j in range(10):
                if mapa2[i][j] == 0:
                    mapa2[i][j] = 100
              
        matrica = copy.deepcopy(mapa2)
        matrica[x][y] = 200
        arr.append(matrica)
        iterator += 1
        
         
        
        while True:
            # Vozimo prema trenutnim parametrima (pomerimo karting)
            x = x + pravacx
            y = y + pravacy
            
            
            # Ukoliko smo se vratili na start, izvozali smo ceo krug, znaci sve akcije su 
            # bile dobre. Takvom hromozomu dajemo dodatnu prednost
            if x == 2 and y == 2:
                break
            
            # A mozda smo se zakucali u zid
            if self.map[y][x] == 0:
                matrica = copy.deepcopy(mapa2)
                matrica[y][x] = 50
                arr.append(matrica)
                iterator += 1
                break
            
            matrica = copy.deepcopy(mapa2)
            matrica[y][x] = 200
            arr.append(matrica)
            iterator += 1
            
            #Naredni redovi odredjuju trenutno stanje
            
            # Ispitivanje da li je na polju ispred zid (oznacen 0) ili put (oznacen 1)
            polje_ispred = self.map[y + pravacy][x + pravacx]
            
            # Ispitivanje da li je na dva polja ispred zid (oznacen 0) ili put (oznacen 1)
            dva_polje_ispred = self.map[y + 2*pravacy][x + 2*pravacx]
            
            # Ispitivanje sta je levo od trenutne pozicije
            levo = self.map[y - pravacx][x + pravacy]
            
            #Ispitivanje sta je desno od trenutne pozicije
            desno = self.map[y + pravacx][x - pravacy]
            
            # Odredjujemo indeks stanja u hromozomu
            indeks = 16*brzina + 8*polje_ispred + 4*dva_polje_ispred + 2*levo + desno
            
            # U hromozom[indeks] je akcija koja se preduzima i moze biti neka od vrednosti [0, 1, 2, 3, 4]
            # Ako je 0 nema akcije -- nastavlja se istom brzinom u istom pravcu
            # U ostalim slucajevima ima promene koje se mogu videti
            if hromozom[indeks] == 1:
                # smanji brzinu
                brzina = 0
            elif hromozom[indeks] == 2:
                # povecaj brzinu
                brzina = 1
            elif hromozom[indeks] == 3:
                # skrenuti levo, ali samo ako je brzina 1, tj. ako brzo vozi ne moze se skrenuti
                if brzina == 0:
                    pomocna = pravacx
                    pravacx = pravacy
                    pravacy = -pomocna
            elif hromozom[indeks] == 4:
                # skrenuti desno, ali samo ako je brzina 1, tj. ako brzo vozi ne moze se skrenuti
                if brzina == 0:
                    pomocna = pravacx
                    pravacx = -pravacy
                    pravacy = pomocna
        
        
             
        
        self.i = 0
        self.num_of_matrices = iterator - 1
        self.arr = arr
        self.im = plt.imshow(self.arr[0], animated=True)
        ani = FuncAnimation(self.fig, self.updatefig,   frames=self.num_of_matrices-1, interval=1000, blit=True, repeat=False)
        plt.show(block=True)
        
        
    def updatefig(self, *args):
        if (self.i<self.num_of_matrices):
            self.i += 1
        else:
            self.i=0
        self.im.set_array(self.arr[self.i])
        return self.im,        


def main():
    """
    Matrica je mapa puta kuda se vozi auto. 
    Broj 0 oznacava zid i tu se ne moze voziti.
    Broj 1 oznacava put kuda se moze voziti.
    Da bi animacija radila neophodno je koristiti numpy niz. O numpy nizovima ce biti kasnije vise reci 
    (kada budemo radili masinsko ucenjenje). Za sada ga mozemo koristiti kao najobicniji niz/matricu.
    """
    mapa = np.array([[0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,1,1,1,0,0,0,0],
                    [0,0,1,0,0,1,1,1,0,0],
                    [0,0,1,0,0,0,0,1,0,0],                  
                    [0,0,1,0,0,0,0,1,0,0],
                    [0,0,1,1,1,1,0,1,0,0],                  
                    [0,0,0,0,0,1,1,1,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0]])  

    g = GeneticAlgorithm(mapa)
    g.optimize()

if __name__ == "__main__":
    main()