# Genetski algoritam za resavanje problema: Zbir podskupa
# Za dati niz i vrednost, naci podskup niza koji u zbiru daje zadatu vrednost
# NP tezak problem
# [1, 2, 76, -34, 45,23, 8, 3]
# 34 = 23 + 8 + 3
# a = [0, 0, 1,| 0, 0,| 0, 1, 1]
# b = [1, 1, 0,| 0, 1,| 0, 0, 0]
# c = [0, 0, 1, 0, 1, 0, 0, 0]
# d = [1, 1, 0, 0, 0, 0, 1, 1]
import random

class Individual():
    def __init__(self, array, target):
        self.array = array
        self.target = target
        self.length = len(array)
        self.code = [random.choice([0, 1]) for _ in range(len(array))]
        self.fitness = self.calculateFitness()

    def __lt__(self, other):
        return self.fitness < other.fitness

    def calculateFitness(self):
        suma = 0
        for i in range(self.length):
            suma += self.array[i] * self.code[i]

        return abs(suma - self.target)

    def mutation(self, mutation_rate):
        x = random.uniform(0, 1)
        if x < mutation_rate:
            index = random.randint(0, self.length-1)
            self.code[index] = 1 if self.code[index] == 0 else 0

            self.fitness = self.calculateFitness()

def selection(population, size):
    minFitness = float('inf')
    bestIndex = -1
    for i in range(size):
        index = random.randrange(len(population))
        if population[index].fitness < minFitness:
            minFitness = population[index].fitness
            bestIndex = index
    return bestIndex

def crossover(parent1, parent2, array, target):
    child1 = Individual(array, target)
    child2 = Individual(array, target)

    breakpoint = random.randrange(len(array))
    child1.code[:breakpoint] = parent1.code[:breakpoint]
    child2.code[:breakpoint] = parent2.code[:breakpoint]

    child1.code[breakpoint:] = parent2.code[breakpoint:]
    child2.code[breakpoint:] = parent1.code[breakpoint:]

    child1.fitness = child1.calculateFitness()
    child2.fitness = child2.calculateFitness()

    return (child1, child2)

TOURNAMENT_SIZE = 6
POPULATION_SIZE = 100
ELITISM_SIZE = int(0.3 * POPULATION_SIZE)
MAX_ITER = 500
MUTATION_RATE = 0.02
# Test niz
array = list(range(1000))
random.shuffle(array)
# Vrednost
target = 150682

# Inicijalna populacija
population = [Individual(array, target) for i in range(POPULATION_SIZE)]
newPopulation = [Individual(array, target) for i in range(POPULATION_SIZE)]

for i in range(MAX_ITER):
    population.sort()
    if i % 10 == 0:
        print(population[0].fitness)
    if population[0].fitness == 0:
        break
    newPopulation[:ELITISM_SIZE] = population[:ELITISM_SIZE]
    for j in range(ELITISM_SIZE, POPULATION_SIZE, 2):
        parent1index = selection(population, TOURNAMENT_SIZE)
        parent2index = selection(population, TOURNAMENT_SIZE)

        child1, child2 = crossover(population[parent1index], population[parent2index], array, target)
        child1.mutation(MUTATION_RATE)
        child2.mutation(MUTATION_RATE)

        newPopulation[j] = child1
        newPopulation[j+1] = child2

    population = newPopulation

bestIndividual = min(population, key=lambda x: x.fitness)
print(bestIndividual.code)
print(bestIndividual.fitness)
