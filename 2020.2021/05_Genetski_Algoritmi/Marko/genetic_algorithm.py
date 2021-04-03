
import string
import random


class Chromosome:
    def __init__(self, genetic_code, fitness):
        self.genetic_code = genetic_code #['a', 'C', 'B' ...]
        self.fitness = fitness # R

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "{} = {}".format(''.join(self.genetic_code), self.fitness)

class Problem:
    def __init__(self):
        self.possible_gene_values = string.ascii_letters
        self.target = get_random_string(120)
        self.target_length = len(self.target)
        self.target_fitness = self.target_length - 3
        
        
    def calculate_fitness(self, genetic_code):
        if len(genetic_code) != self.target_length:
            return 0
        fitness = 0
        for i in range(self.target_length):
            if genetic_code[i] == self.target[i]:
                fitness += 1
        return fitness
    
    def best_fit(self, chromosome):
        return chromosome.fitness >= self.target_fitness

    def __str__(self):
        return "{} = {}".format(self.target, self.target_fitness)


class GeneticAlgorithm:
    def __init__(self, problem):
        self.problem = problem
    
        
        self.max_iterations = 1000
        self.generation_size = 5000
        self.chromosome_size = self.problem.target_length
        self.tournament_size = 10
        self.reproduction_size = 1000
        self.selection_function = self.roulette_selection # self.tournament_selection
        self.mutation_rate = 0.1
        

    def initial_population(self):
        result = []
        for _ in range(self.generation_size):
            genetic_code = [random.choice(self.problem.possible_gene_values) for _ in range(self.chromosome_size)]
            fitness = self.problem.calculate_fitness(genetic_code)
            chromosome = Chromosome(genetic_code, fitness)
            result.append(chromosome)
        return result

    def roulette_selection(self, population):
        result = random.choices(population, weights=[x.fitness for x in population], k = 1)
        return result[0]

    def tournament_selection(self, population):
        selected = random.sample(population, self.tournament_size)
        result = max(selected, key = lambda x: x.fitness)
        return result

    def selection(self, population):
        result = [self.selection_function(population) for _ in range(self.reproduction_size)]
        return result

    def crossover(self, parent1: Chromosome, parent2: Chromosome):
        break_point = random.randint(1, self.chromosome_size)
        child1 = parent1.genetic_code[:break_point] + parent2.genetic_code[break_point:]
        child2 = parent2.genetic_code[:break_point] + parent1.genetic_code[break_point:]
        return child1, child2

    def mutate(self, genetic_code):
        random_value = random.random()

        if random_value < self.mutation_rate:
            random_index = random.randrange(len(genetic_code))
            genetic_code[random_index] = random.choice(self.problem.possible_gene_values)
        return genetic_code

    def create_generation(self, selected):
        result = []

        for _ in range(self.generation_size // 2):
            parents = random.sample(selected, 2)

            child1_code, child2_code = self.crossover(parents[0], parents[1])

            child1_code = self.mutate(child1_code)
            child2_code = self.mutate(child2_code)

            child1 = Chromosome(child1_code, self.problem.calculate_fitness(child1_code))
            child2 = Chromosome(child2_code, self.problem.calculate_fitness(child2_code))

            result.append(child1)
            result.append(child2)

        return result


    def optmize(self):
        population = self.initial_population()
        
        global_best = max(population, key = lambda x: x.fitness)
        global_best_iteration_found = 0

        for i in range(self.max_iterations):
            selected = self.selection(population)
            
            population = self.create_generation(selected)
            
            current_best = max(population, key = lambda x: x.fitness)
            print(current_best)
            
            if global_best.fitness < current_best.fitness:
                global_best = current_best
                global_best_iteration_found = i
            
            
            if self.problem.best_fit(current_best):
                result = current_best
                break
            
            if i - global_best_iteration_found >= 4:
                print('No better chromosome in 4 iterations')
                result = global_best
                break
        return result            



def get_random_string(n):
    return [random.choice(list(string.ascii_letters)) for _ in range(n)]



if __name__ == '__main__':
    problem = Problem()
    print(problem)
    genetic_algorithm = GeneticAlgorithm(problem)
    result = genetic_algorithm.optmize()
    print('Best found: ', result)
    