#!/usr/bin/python

import random, string
import sys, os


class GeneticAlgorithm:
    """
    Klasa predstavlja implementaciju genetskog algoritma za resavanje problema pogadjanja niske.
    Koristi se:
    - Jednopoziciono ukrstanje sa nasumicnom tackom ukrstanja
    - Mutacija sa verovatnocom '_mutation_rate'
    - Ruletska selekcija
    - Zamena generacije se vrsi tako sto se od jedinki izabranih pri selekciji ukrstanjem
        pravi celokupna nova generacija (pogledati u knjizi alternativne zamene generacija)
    """
    def __init__(self, target, allowed_gene_values):
        self._target = target                               # Niska koja se pogadja
        self._target_size = len(target)                     # Duzina niske koja se pogadja
        self._allowed_gene_values = allowed_gene_values     # Dozvoljene vrednosti koje mogu biti u genu

        """Parametri genetskog algoritma, eksperimentalno izabrani."""
        self._iterations = 1000                             # Maksimalni dozvoljeni broj iteracija
        self._generation_size = 5000                        # Broj jedinki u jednoj generaciji
        self._mutation_rate = 0.01                          # Verovatnoca da se desi mutacija
        self._reproduction_size = 1000                      # Broj jedinki koji ucestvuje u reprodukciji
        self._current_iteration = 0                         # Koristi se za interno pracenje iteracija algoritma
        self._top_chromosome = None                         # Hromozom koji predstavlja resenje optimizacionog procesa


    def optimize(self):
        # Generisi pocetnu populaciju jedinki i izracunaj
        # prilagodjenost svake jedinke u populaciji
        chromosomes = self.initial_population()

        # Sve dok uslov zaustavljanja nije zadovoljen
        while not self.stop_condition():
            print("Iteration: %d" % self._current_iteration)

            # Izaberi iz populacije skup jedinki za reprodukciju
            for_reproduction = self.selection(chromosomes)

            # Prikaz korisniku trenutnog stanja algoritma
            the_sum = sum(chromosome.fitness for chromosome in chromosomes)
            print("Reproduction chromos sum fitness: %d" % the_sum)
            print("top solution: %s" % max(chromosomes, key=lambda chromo: chromo.fitness))

            # Primenom operatora ukrstanja i mutacije kreiraj nove jedinke
            # i izracunaj njihovu prilagodjenost.
            # Dobijene jedinke predstavljaju novu generaciju.
            chromosomes = self.create_generation(for_reproduction)
            self._current_iteration += 1
            print()

        # Vrati najkvalitetniju jedinku u poslednjoj populaciji
        if self._top_chromosome:
            return Chromosome(self._top_chromosome, self.fitness(self._top_chromosome))
        else:
            return max(chromosomes, key=lambda chromo: chromo.fitness)


    def create_generation(self, for_reproduction):
        """
        Od jedinki dobijenih u okviru 'for_reproduction' generise novu generaciju
        primenjujuci genetske operatore 'crossover' i 'mutation'.
        Nova generacija je iste duzine kao i polazna.
        """
        new_generation = []
        # sve dok ne popunimo generaciju
        while len(new_generation) < self._generation_size:
            # Biramo dva nasumicno i vrsimo ukrstanje
            parents = random.sample(for_reproduction, 2)
            child1, child2 = self.crossover(parents[0].content, parents[1].content)

            # Vrsimo mutaciju nakon ukrstanja
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)

            # Dodajemo nove hromozome u novu generaciju
            new_generation.append(Chromosome(child1, self.fitness(child1)))
            new_generation.append(Chromosome(child2, self.fitness(child2)))

        return new_generation


    def crossover(self, a, b):
        """Vrsi jednopoziciono ukrstanje po nasumicnoj poziciji unutar hromozoma."""
        cross_point = random.randint(0, len(a)-1)
        ab = a[:cross_point] + b[cross_point:]
        ba = b[:cross_point] + a[cross_point:]
        return (ab, ba)


    def mutation(self, chromosome):
        """Vrsi mutaciju nad hromozomom sa verovatnocom self._mutation_rate"""
        t = random.random()
        if t < self._mutation_rate:
            i = random.randint(0, len(chromosome)-1)
            chromosome = list(chromosome)       # usled imutabilnosti string moramo prebaciti u listu
            chromosome[i] = random.choice(self._allowed_gene_values)
            chromosome =  "".join(chromosome)   # od liste pravimo nazad string
        return chromosome


    def selection(self, chromosomes):
        """
        Funkcija bira self._reproduction_size hromozoma koristeci ruletsku selekciju
        koji ce se na dalje koristiti za ukrstanje i smenu generacija.
        """
        # Izracunava se suma funkcija prilagodjenosti svih hromozoma.
        the_sum = sum(chromosome.fitness for chromosome in chromosomes)
        selected_chromos = []

        # for i in range(self._reproduction_size):
            # selected_chromos.append(self.selection_roulette_pick_one(chromosomes, the_sum))
        # Drugi nacin:
        selected_chromos = [
            self.selection_roulette_pick_one(chromosomes, the_sum)
            for i in range(self._reproduction_size)]

        return selected_chromos


    def selection_roulette_pick_one(self, chromosomes, the_sum):
        """
        Bira jednu jedinku koristeci ruletsku selekciju. Ne vrsi normalizaciju
        i sortiranje po funkciji prilagodjenosti usled performansi.
        """
        pick = random.uniform(0, the_sum)
        value = 0
        i = 0
        for chromosome in chromosomes:
            i += 1
            value += chromosome.fitness
            if value > pick:
                return chromosome


    # TODO: renamt to chromo
    def the_goal_function(self, chromosome):
        """
         Za slucaj da smo nasli optimalno resenje (u opstem slucaju ovo retko znamo)
         pamtimo gen kao optimalni i prekidamo algoritam (bice zadovoljen kriterijum zaustavljanja).
         Iako u praksi ne znamo da li je dobijeno resenje optimalno, cesto postoji odredjena
         'funkcija cilja' koja testira da li je dobijeno resenje dovoljno kvalitetno da se prihvati.
        """
        if chromosome == self._target:
            print("Found solution at iteration: %d" % self._current_iteration)
            self._top_chromosome = chromosome


    def fitness(self, chromosome):
        """Vraca broj karaktera koji se u genu poklapaju sa pravom vrednoscu."""
        matched = zip(self._target, chromosome)             # Uparuju se stringovi element po element
        compared = map(lambda t: t[0] == t[1], matched)     # Za svaki par proveravamo da li je jednak
        compared = list(filter(lambda x: x, compared))      # Zadrzavamo samo one elemente koji su tacni
        self.the_goal_function(chromosome)

        return len(compared)                                # Njihov broj je upravo broj elemenata koji se poklapaju


    def take_random_element(self, fromHere):
        """ Funkcija vraca nasumicno odabran element iz kolekcije 'fromHere'. """
        i = random.randrange(0, len(fromHere))
        return fromHere[i]


    def initial_population(self):
        """Generisemo _generation_size nasumicnih jedinki."""
        allowed_symbols = list(string.ascii_letters)
        init_pop = []                   # inicijalna populacija jedinki
        for i in range(self._generation_size):
            genetic_code = []           # genetski kod koji cemo nasumicno izabrati
            for k in range(self._target_size):
                # Uzimamo nasumicni gen iz dozvoljenih vrednosti za gen
                genetic_code.append(self.take_random_element(self._allowed_gene_values))
            # U inicijalnu generaciju dodajemo novi genetski kod
            init_pop.append("".join(genetic_code))

        # Transformisemo listu tako da od liste genetskih kodova postane lista hromozoma
        init_pop = [Chromosome(content, self.fitness(content)) for content in init_pop]
        return init_pop


    def stop_condition(self):
        return self._current_iteration > self._iterations or self._top_chromosome != None


class Chromosome:
    """
    Klasa predstavlja jedan hromozom za koji se cuva njegov genetski kod i vrednost funkcije prilagodjenosti.
    """
    def __init__(self, content, fitness):
        self.content = content
        self.fitness = fitness
    def __str__(self): return "%s f=%d" % (self.content, self.fitness)
    def __repr__(self): return "%s f=%d" % (self.content, self.fitness)


if __name__ == "__main__":
    genetic = GeneticAlgorithm("HelloWorld", string.ascii_letters)
    # print(genetic.fitness("Hello xxxx"))
    solution = genetic.optimize()
    print("Solution: %s fitness: %d" % (solution.content, solution.fitness))
