
import string
import random
class Chromosome:
    def __init__(self, genetic_code, fitness):
        self.genetic_code = genetic_code # [a, B, c, f, H, g]
        self.fitness = fitness

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "{} = {}".format(''.join(self.genetic_code), self.fitness)

class GeneticAlgorithm:
    def __init__(self, possible_gene_values, target):
        self.possible_gene_values = possible_gene_values
        self.target = target

        self.max_iterations = 1000
        self.generation_size = 5000
        self.chromosome_size = len(target)
        self.reproduction_size = 1000
        self.selection_function = self.tournament_selection
        self.tournament_size = 10
        self.mutation_rate = 0.1

    def calculate_fitness(self, genetic_code):
        fitness_value = 0
        for i in range(self.chromosome_size):
            if genetic_code[i] == self.target[i]:
                fitness_value += 1
        return fitness_value

    def initial_population(self):
        result = []
        for _ in range(self.generation_size):
            genetic_code = [random.choice(self.possible_gene_values) for _ in range(self.chromosome_size)]
            fitness = self.calculate_fitness(genetic_code)
            chromosome = Chromosome(genetic_code, fitness)
            result.append(chromosome)
        return result

    def roulette_selection(self, population):
        result = random.choices(population, weights = [x.fitness for x in population], k = 1)
        return result[0]

    def tournament_selection(self, population):
        selected = random.sample(population, self.tournament_size)
        result = max(selected, key = lambda x: x.fitness)
        return result

    def selection(self, population):
        result = [self.selection_function(population) for _ in range(self.reproduction_size)]
        return result

    def crossover(self, parent1:Chromosome, parent2:Chromosome):
        break_point = random.randrange(1, self.chromosome_size)
        child1 = parent1.genetic_code[:break_point] + parent2.genetic_code[break_point:]
        child2 = parent2.genetic_code[:break_point] + parent1.genetic_code[break_point:]
        return child1, child2

    def mutate(self, code):
        random_value = random.random()

        if random_value < self.mutation_rate:
            random_index = random.randrange(self.chromosome_size)
            while True:
                new_value = random.choice(self.possible_gene_values)
                if code[random_index] != new_value:
                    code[random_index] = new_value
                    break 

        return code

    def create_generation(self, selected):
        result = []

        for _ in range(self.generation_size // 2):
            # proizvoljno odabermo dva roditelja
            parents = random.sample(selected, 2)
            
            # napravimo dva detata od ta dva roditelja
            child1_code, child2_code = self.crossover(parents[0], parents[1])

            # izvrismo mutaciju gena
            child1_code = self.mutate(child1_code)
            child2_code = self.mutate(child2_code)
            
            # dodamo u result
            child1 = Chromosome(child1_code, self.calculate_fitness(child1_code))
            child2 = Chromosome(child2_code, self.calculate_fitness(child2_code))

            result.append(child1)
            result.append(child2)

        return result

    def best_fit(self, chromosome):
        return chromosome.fitness == self.chromosome_size

    def optimize(self):
        result = None

        population = self.initial_population()

        for _ in range(0, self.max_iterations):
            # Ruletska ili turnirska

            selected = self.selection(population)

            population = self.create_generation(selected)

            global_best_chromosome = max(population, key = lambda x: x.fitness)
            print(global_best_chromosome)
            if self.best_fit(global_best_chromosome): 
                result = global_best_chromosome
                break

        return result

if __name__ == '__main__':
    genetic_algorithm = GeneticAlgorithm(string.ascii_letters, 'ABCDEFGHIJKL')
    result = genetic_algorithm.optimize()

    print(result)




