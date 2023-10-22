import random
import pprint

import numpy as np

POP_SIZE = 200
IND_LEN = 50
CX_PROB = 0.8
MUT_PROB = 0.05
MUT_FLIP_PROB = 0.1


# creates a single individual of lenght `lenght`
def create_ind(length):
    return [random.randint(0, 1) for _ in range(length)]


# creates a population of `size` individuals
def create_population(size):
    return [create_ind(IND_LEN) for _ in range(size)]

TOURNAMENT_COMPETITOR_COUNT = 2
# tournament selection
def tournament_selection(pop, fits):
     selected = []
     for _ in range(len(pop)):
        parents = [random.randrange(0, len(pop)) for _ in range(TOURNAMENT_COMPETITOR_COUNT)]
        selected.append(pop[max(parents, key=lambda ind:fits[ind])])
     return selected

# roulette wheel selection
def roulette_selection(pop, fits):
    return random.choices(pop, fits, k=POP_SIZE)

def selection(pop, fits):
    return tournament_selection(pop, fits)

# one point crossover
def cross(p1, p2):
    point = random.randint(0, len(p1))
    o1 = p1[:point] + p2[point:]
    o2 = p2[:point] + p1[point:]
    return o1, o2


# applies crossover to all individuals
def crossover(pop):
    off = []
    for p1, p2 in zip(pop[0::2], pop[1::2]):
        o1, o2 = p1[:], p2[:]
        if random.random() < CX_PROB:
            o1, o2 = cross(p1[:], p2[:])
        off.append(o1)
        off.append(o2)
    return off


# bit-flip mutation
def mutate(p):
    if random.random() < MUT_PROB:
        return [1 - i if random.random() < MUT_FLIP_PROB else i for i in p]
    return p[:]


# applies mutation to the whole population
def mutation(pop):
    return list(map(mutate, pop))


# applies crossover and mutation
def operators(pop):
    pop1 = crossover(pop)
    return mutation(pop1)


# evaluates the fitness of the individual
def fitness(ind):
    return max(((ind[0::2]).count(0) + (ind[1::2]).count(1), ((ind[1::2]).count(1) + (ind[0::2]).count(0))))


# implements the whole EA
def evolutionary_algorithm(fitness):
    pop = create_population(POP_SIZE)
    log = []
    for G in range(100):
        fits = list(map(fitness, pop))
        log.append((G, max(fits), sum(fits) / 100, G * POP_SIZE))
        # print(G, sum(fits), max(fits)) # prints fitness to console
        mating_pool = selection(pop, fits)
        offspring = operators(mating_pool)
        pop = offspring[:-1]+[max(pop, key=fitness)] #SGA + elitism
        #pop = offspring[:]  # SGA

    return pop, log


# i1, i2 = create_ind(10), create_ind(10)
# print((i1, i2))
# print(cross(i1, i2))
# print(mutate(i1))

# run the EA 10 times and aggregate the logs, show the last gen in last run
for j in range(10):
    print("run: " + str(j))
    CX_PROB = j/10
    TOURNAMENT_COMPETITOR_COUNT += 1
    #MUT_PROB = j/10
    #MUT_FLIP_PROB = 0.2
    logs = []
    for i in range(10):
        random.seed(i)
        pop, log = evolutionary_algorithm(fitness)
        logs.append(log)
    fits = list(map(fitness, pop))
    # pprint.pprint(list(zip(fits, pop)))
    # print(sum(fits), max(fits))
    # pprint.pprint(log)

    # extract fitness evaluations and best fitnesses from logs
    evals = []
    best_fit = []
    for log in logs:
        evals.append([l[3] for l in log])
        best_fit.append([l[1] for l in log])

    evals = np.array(evals)
    best_fit = np.array(best_fit)

    # plot the converegence graph and quartiles
    import matplotlib.pyplot as plt

    plt.plot(evals[0, :], np.median(best_fit, axis=0), label="CX_PROB: " + str(CX_PROB) + " | MUT_PROB: " + str(MUT_PROB))
    plt.fill_between(evals[0, :], np.percentile(best_fit, q=25, axis=0),
                     np.percentile(best_fit, q=75, axis=0), alpha=0.2)
plt.legend()
plt.savefig('sga.png', bbox_inches='tight', dpi=600)