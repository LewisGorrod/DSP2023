
from LightsOut import *
import random
import matplotlib.pyplot as plot

# GA constants
POP_SIZE = 50
N_ELITES = 1
P_CROSSOVER = 0.75
P_MUTATE = 0.1
N_GENS = 500

# Encourages more diverse initial population
def genPopulation():
    population = []
    for i in range(POP_SIZE):
        individual = [0 for j in range(N_BUTTONS)]
        for k in range(random.randint(0, N_BUTTONS)):
            individual[random.randint(0, N_BUTTONS - 1)] = 1
        population.append(individual)
    return population

def fitness(individual):
    r = p[:]
    for i in range(N_BUTTONS):
        if individual[i] == 1:
            r = getNextState(r, i)
    return N_BUTTONS - sum(r) - sum(individual)
    
def totalFitness(population):
    f = 0
    for i in population:
        f += fitness(i)
    return f

def averageFitness(population):
    return totalFitness(population) / POP_SIZE

def best(population):
    return population[0]

def sort(population):
    for i in range(POP_SIZE):
        for j in range(POP_SIZE - 1):
            if fitness(population[j]) < fitness(population[j + 1]):
                tmp = population[j]
                population[j] = population[j + 1]
                population[j + 1] = tmp

def selection(population):
    tmp = random.random() * totalFitness(population)
    for i in population:
        tmp -= fitness(i)
        if tmp <= 0:
            return i

def crossover(parent1, parent2):
    crosspoint = random.randint(0, N_BUTTONS)
    offspring1 = mutate(parent1[:crosspoint] + parent2[crosspoint:])
    offspring2 = mutate(parent2[:crosspoint] + parent1[crosspoint:])
    return offspring1, offspring2

def mutate(chromosome):
    if random.random() < P_MUTATE:
        chromosome[random.randint(0, N_BUTTONS - 1)] ^= 1
    return chromosome

def diversity(population):
    unique = []
    for i in population:
        if i not in unique:
            unique.append(i)
    return len(unique)

def diversity_score(individual, population):
    c = 0
    for i in population:
        if individual == i:
            c += 1
    return POP_SIZE / c

def graph(y1, y2, y3):
    x = [i for i in range(N_GENS)]
    fig, ax1 = plot.subplots()
    ax2 = ax1.twinx()
    ax1.plot(x, y1, color='limegreen')
    ax1.plot(x, y2, color='lightgrey')
    ax2.plot(x, y3, 'lightblue')
    plot.title('Lights Out GA')
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('Fitness', color='limegreen')
    ax2.set_ylabel('Diversity', color='lightblue')
    plot.show()

def main():
    y1, y2, y3 = [], [], []
    for gen in range(N_GENS):
        if gen == 0:
            population = genPopulation()
        else:
            next_population = []
            for i in range(N_ELITES): # Elitism
                next_population.append(population[i])
            while len(next_population) < POP_SIZE:
                parent1 = selection(population)
                while (parent2 := selection(population)) == parent1: # Prevent asexual reproduction
                    None
                if random.random() < P_CROSSOVER: # Reproduce
                    offspring1, offspring2 = crossover(parent1, parent2)
                    next_population.append(offspring1)
                    if len(next_population) < POP_SIZE: # Preserve population size
                        next_population.append(offspring2)
                else:
                    next_population.append(parent1)
                    if len(next_population) < POP_SIZE:
                        next_population.append(parent2) # Preserve population size
            population = next_population
        sort(population)
        y1.append(fitness(best(population)))
        y2.append(averageFitness(population))
        y3.append(diversity(population))
    print(f'Best: {best(population)}')
    graph(y1, y2, y3)

if __name__ == '__main__':
    # Game variables
    x = genSolution(1)
    p = genStartingConfig(x)
    main()