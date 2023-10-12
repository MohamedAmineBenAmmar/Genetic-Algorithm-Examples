import random


class Chromosome:
    def __init__(self, length: int, mutation_rate: float) -> None:
        self.length = length
        self.numbers = [
            chr(ord("0") + x) for x in range(10)
        ]  # Create a list of characters ['0', '1', ..... '9']
        self.operations = ["+", "-", "*", "/"]
        self.dna = [None] * length  # Create an empty list of length length
        self.mutation_rate = mutation_rate
        self.fitness = None

        self.init_chromosome()

    def correct_genetic_disorder(self, gene: int, child=None):
        individual = None
        if child == None:
            individual = self
        else:
            individual = child

        if individual.dna[gene] == "0":
            if gene - 1 >= 0 and individual.dna[gene - 1] == "/":
                individual.dna[gene] = self.numbers[
                    random.randint(1, len(self.numbers) - 1)
                ]
        elif individual.dna[gene] == "/":
            if gene + 1 < self.length and individual.dna[gene + 1] == "0":
                individual.dna[gene] = self.operations[
                    random.randint(0, len(self.operations) - 2)
                ]

    def init_chromosome(self):
        pointer = "NUMBER"
        for i in range(0, self.length):
            if pointer == "OPERATION":
                self.dna[i] = self.operations[
                    random.randint(0, len(self.operations) - 1)
                ]
                pointer = "NUMBER"
            else:
                self.dna[i] = self.numbers[random.randint(0, len(self.numbers) - 1)]
                pointer = "OPERATION"

            self.correct_genetic_disorder(i)

    def crossover(self, partner) -> tuple:
        child1 = Chromosome(self.length, self.mutation_rate)
        child2 = Chromosome(self.length, self.mutation_rate)

        for i in range(0, self.length // 2):
            child1.dna[i] = partner.dna[i]
            child2.dna[i] = self.dna[i]

        for i in range(self.length // 2, self.length):
            child1.dna[i] = self.dna[i]
            child2.dna[i] = partner.dna[i]

        self.correct_genetic_disorder(self.length // 2, child1)
        self.correct_genetic_disorder(self.length // 2, child2)

        return child1, child2

    def mutate(self):
        pointer = "NUMBER"
        for i in range(0, self.length):
            if random.uniform(0, 1) <= self.mutation_rate:
                if pointer == "NUMBER":
                    self.dna[i] = self.numbers[random.randint(0, len(self.numbers) - 1)]
                else:
                    self.dna[i] = self.operations[
                        random.randint(0, len(self.operations) - 1)
                    ]

                self.correct_genetic_disorder(i)

            if pointer == "NUMBER":
                pointer = "OPERATION"
            else:
                pointer = "NUMBER"

    def calculate_fitness(self, target):
        expression = "".join(self.dna)
        result = eval(expression)
        self.fitness = abs(result - target)


class Population:
    def __init__(self, size, target: int) -> None:
        self.size = size
        self.individuals = None
        self.survivors = None
        self.generation = 0
        self.target = target
        self.evolve = True

        self.generate_initial_population()

    def generate_initial_population(self):
        individuals = []
        for i in range(0, self.size):
            new_individual = Chromosome(9, 0.03)
            individuals.append(new_individual)

        self.individuals = individuals

    def calculate_population_fitness(self):
        for i in range(0, self.size):
            self.individuals[i].calculate_fitness(self.target)
            if self.individuals[i].fitness == 0:
                self.evolve = False

    def perform_natural_selection(self):
        sorted_individuals = sorted(
            self.individuals, key=lambda individual: individual.fitness
        )
        self.survivors = sorted_individuals[: len(sorted_individuals) // 2]

    def perform_population_crossover(self):
        new_individuals = []
        for i in range(0, len(self.survivors) - 1, 2):
            child1, child2 = self.survivors[i].crossover(self.survivors[i + 1])
            child1.mutate()
            child2.mutate()

            new_individuals.append(self.survivors[i])
            new_individuals.append(self.survivors[i + 1])
            new_individuals.append(child1)
            new_individuals.append(child2)

        self.individuals = new_individuals
        self.generation += 1

    def display(self, key: str):
        entity = None
        if key == "individuals":
            entity = self.individuals
        else:
            entity = self.survivors

        print("-----------------")
        print(key)
        for i in range(0, len(entity)):
            print(entity[i].dna, entity[i].fitness)

        print("-----------------")


if __name__ == "__main__":
    # Initialize the population
    population = Population(20, 20)
    population.display("individuals")

    while True:
        # Select the survivors
        population.calculate_population_fitness()
        population.perform_natural_selection()
        population.display("survivors")

        # Perform crossover
        population.perform_population_crossover()
        population.display("individuals")

        if population.evolve == False:
            break

    print("Stats:")
    print("- number of generations: ", population.generation)
    print("- current population: ")
    population.display("individuals")
    print("- current survivors: ")
    population.display("survivors")
