
from LightsOut import *
import random
import time

N_POPULATION = 10 # Number of candidate solutions
N_RULES = 2 # Number of rules per candidate solution
P_CROSSOVER = 0.5 # Probability of crossover
P_MUTATE = 1 # Probability of mutation
R_MUTATE = 0.75 # Ratio of condition to output mutation
N_GENS = 100 # Number of generations
N_DATAPOINTS = 25

data = []

def printData():
    for dp in data:
        printRule(dp)

def toString(list):
    return ''.join(str(i) for i in list)

def toList(string):
    l = []
    for i in string:
        if i == '#' or i == '*':
            l.append(i)
        else:
            l.append(int(i))
    return l

def printRule(rule):
    r_info = getRuleInfo(rule)
    print(f'[{toString(rule[0])}, {toString(rule[1])}] Matched: {r_info[0]}, Correct: {r_info[1]}')

def printIndividual(individual):
    for r in individual:
        printRule(r)

def printPopulation(population):
    for i in population:
        printIndividual(i)

def genData():
    data = []
    for i in range(N_BUTTONS):
        x = [0 for i in range(N_BUTTONS)]
        x[i] = 1
        p = genStartingConfig(x)
        data.append([p, x])
    return data

def matchCondition(rule, datapoint):
    for i in range(N_BUTTONS):
        if rule[0][i] != '#' and (rule[0][i] != datapoint[0][i]):
            return False
    # print(f'[{toString(rule[0])}, {toString(rule[1])}]')
    # print(f'[{toString(datapoint[0])}, {toString(datapoint[1])}]')
    return True

def matchOutput(rule, datapoint):
    if rule[1] == datapoint[1]:
        return True
    return False

def genRule():
    dp = random.choice(data)
    c = dp[0]
    for i in range(20):
        c[random.randint(0, N_BUTTONS - 1)] = '#'
    if random.random() < 0.5:
        tmp = random.randint(1, int(N_BUTTONS / 2) - 1)
        for i in range(tmp):
            c[i] = '*'
            c[N_BUTTONS - 1 - i] = '*'
    return [c, dp[1]]

def mutateRule(rule):
    if random.random() < R_MUTATE: # Mutate condition
        x = random.randint(0, N_BUTTONS - 1)
        mutated = False
        while not mutated:
            m_type = random.randint(1, 5)
            # print(f'm_type {m_type}')
            if m_type == 1 and (0 in rule[0] or 1 in rule[0]): # Change button press
                # print('1: change button press')
                while rule[0][x] == '#' or rule[0][x] == '*':
                    x = random.randint(0, N_BUTTONS - 1)
                rule[0][x] ^= 1
                mutated = True
            elif (m_type == 2) and ('#' in rule[0]): # Specify button press
                # print('2: specify button press')
                while rule[0][x] != '#':
                    x = random.randint(0, N_BUTTONS - 1)
                rule[0][x] = random.randint(0, 1)
                mutated = True
            elif m_type == 3 and (rule[0].count(0) + rule[0].count(1) > 1): # Generalize button press
                # print('3: generalize button press')
                while rule[0][x] == '#' or rule[0][x] == '*':
                    x = random.randint(0, N_BUTTONS - 1)
                rule[0][x] = '#'
                mutated = True
            elif m_type == 4 and '*' in rule[0]: # Constrain button press sequence
                # print('4: constrain button presses')
                n_aster = rule[0].count('*')
                rule[0][int(n_aster / 2) - 1] = random.randint(0, 1)
                rule[0][N_BUTTONS - 1 - (int(n_aster / 2) - 1)] = random.randint(0, 1)
                mutated = True
            elif m_type == 5 and rule[0].count('*') < N_BUTTONS - 2: # Generalize button press sequence
                # print('5: generalize button presses')
                n_aster = rule[0].count('*')
                rule[0][int(n_aster / 2)] = '*'
                rule[0][N_BUTTONS - 1 - int(n_aster / 2)] = '*'
                mutated = True
            else:
                None
                # print('secret option b?')
    else: # Mutate output
        # print('6: change output')
        b = toString(rule[1]).index('1')
        newB = random.randint(0, N_BUTTONS - 1)
        while b == newB:
            newB = random.randint(0, N_BUTTONS - 1)
        rule[1][b] = 0
        rule[1][newB] = 1

def expand(rule):
    if '*' in rule[0]:
        root_c = [i for i in rule[0] if i != '*']
        sub_rules = []
        n_aster = rule[0].count('*')
        for i in range(n_aster + 1):
            c = ['#' for j in range(i)] + root_c + ['#' for j in range(n_aster - i)]
            o = rule[1][int(n_aster / 2) - i:] + rule[1][:int(n_aster / 2) - i]
            sub_rules.append([c, o])
    else:
        sub_rules = [rule]
    return sub_rules

def getRuleInfo(rule):
    n_matched, n_correct = 0, 0
    sub_rules = expand(rule)
    for sr in sub_rules:
        for dp in data:
            if matchCondition(sr, dp):
                n_matched += 1
                if matchOutput(sr, dp):
                    n_correct += 1
    return [n_matched, n_correct]

def fitness(individual):
    n_matched, n_correct, f = 0, 0, 0
    for r in individual:
        sub_rules = expand(r)
        for a in sub_rules:
            for dp in data:
                if matchCondition(a, dp):
                    n_matched += 1
                    if matchOutput(a, dp):
                        n_correct += 1
    return n_correct**2 / (N_RULES * n_matched * N_DATAPOINTS)

def getBest(population):
    return population[0] # Must be sorted first

def genIndividual():
    return [genRule() for i in range(N_RULES)]

def genPopulation():
    return [genIndividual() for i in range(N_POPULATION)]

def totalFitness(population):
    f = 0
    for i in population:
        f += fitness(i)
    return f

def averageFitness(population):
    return totalFitness(population) / N_POPULATION

def sort(population):
    # t_start = time.time()
    for i in range(N_POPULATION):
        for j in range(N_POPULATION - 1):
            if fitness(population[j]) < fitness(population[j + 1]):
                tmp = population[j]
                population[j] = population[j + 1]
                population[j + 1] = tmp
    # t_stop = time.time()
    # print(f'sort(): {t_stop - t_start}s')

def selection(population):
    tmp = random.random() * totalFitness(population)
    for i in population:
        tmp -= fitness(i)
        if tmp <= 0:
            return i
        
def crossover(parent1, parent2):
    cp = random.randint(0, N_RULES)
    child1 = parent1[:cp] + parent2[cp:]
    child2 = parent2[:cp] + parent1[cp:]
    return child1, child2

def mutate(individual):
    if random.random() < P_MUTATE:
        i = random.randint(0, N_RULES - 1)
        # print(f'Mutating rule {i + 1}')
        mutateRule(individual[i])

def diversity(population):
    unique = []
    for i in population:
        for r in i:
            if r not in unique:
                unique.append(r)
    return len(unique) / N_RULES

def main():
    global data
    data = genData()
    for g in range(N_GENS):
        print(f'gen {g + 1}/{N_GENS}')
        if g == 0:
            population = genPopulation()
            sort(population)
            best = getBest(population)
        else:
            next_population = []
            for i in range(int(N_POPULATION / 2)):
                parent1 = selection(population)
                parent2 = selection(population)
                if random.random() < P_CROSSOVER:
                    offspring1, offspring2 = crossover(parent1, parent2)
                    mutate(offspring1)
                    mutate(offspring2)
                    next_population.append(offspring1)
                    next_population.append(offspring2)
                else:
                    next_population.append(parent1)
                    next_population.append(parent2)
            population = next_population
        sort(population)
        if fitness(getBest(population)) > fitness(best):
            best = getBest(population)
    print(f'Best fitness: {fitness(best)}')
    printIndividual(best)

main()

