from random import seed, random, randint, sample

from src import Auxiliary
from src.Constants import Constants
from src.Core import Core
from src.Parameters import Parameters

"""
OPTIMIZER
- Strategy: genetic algorithm
- Codification:
    00 = extends previous shift
    01 = new shift ENTREGA
    10 = new shift RECOGIDA
    11 = new shift DUAL
- Checks:
    At least one shift of each type
    The first shift cannot be 00
- Operators:
    Crossover
    Mutation
- Fitness:
    Processors idle time
"""


def first_shift_is_valid(cur_individual):
    """ checks if the first shift is not an extension """
    return cur_individual[:2] != '00'


def at_least_one_shift_each(cur_individual):
    """ checks if there is at least one of each shift: 01, 10, 11 """
    num_entrega = 0
    num_recogida = 0
    num_dual = 0
    while cur_individual:
        shift = cur_individual[:2]
        cur_individual = cur_individual[2:]
        if shift == '01':
            num_entrega += 1
        elif shift == '10':
            num_recogida += 1
        elif shift == '11':
            num_dual += 1
        if num_entrega > 0 and num_recogida > 0 and num_dual > 0:
            return True
    return False


def get_new_individual():
    """ generates random individuals
    checks first shift
    checks at least one shift each """
    new_individual = ''
    while len(new_individual) < 2 * int(Constants.SIMULATION_DURATION / 3600):
        new_individual += str(randint(0, 1))
    while not first_shift_is_valid(new_individual) or not at_least_one_shift_each(new_individual):
        new_individual = (new_individual + str(randint(0, 1)))[1:]
    return new_individual


def operator_crossover(first_individual, second_individual):
    """ 50% chance for each hour (pair of bits)
    no need to check first shift (both individuals valid)
    checks at least one shift each """
    new_individual = ''
    while new_individual == '':
        for idx in range(int(len(first_individual) / 2)):
            if randint(0, 1) > 0:
                new_individual += first_individual[2 * idx:2 * idx + 2]
            else:
                new_individual += second_individual[2 * idx:2 * idx + 2]
        if not at_least_one_shift_each(new_individual):
            new_individual = ''
    return new_individual


def operator_mutation(old_individual):
    """ changes random shift (pair of bits)
    checks first shift
    checks at least one shift each """
    new_individual = old_individual
    while new_individual == old_individual or not first_shift_is_valid(
            new_individual) or not at_least_one_shift_each(new_individual):
        idx = randint(0, int(len(old_individual)) / 2 - 1)
        old_shift = old_individual[2 * idx:2 * idx + 2]
        new_shift = old_shift
        while new_shift == old_shift:
            new_shift = str(randint(0, 1)) + str(randint(0, 1))
            new_individual = old_individual[:2 * idx] + new_shift + old_individual[2 * idx + 2:]
    return new_individual


def individual_to_parameters(cur_individual):
    """ transforms an individual to a valid parameter configuration """
    new_shift_duration = []
    new_shift_type = []
    while cur_individual:
        shift = cur_individual[:2]
        cur_individual = cur_individual[2:]
        if shift == '00':
            new_shift_duration[-1] += 1
        elif shift == '01':
            new_shift_type.append(Constants.ENTREGA)
            new_shift_duration.append(1)
        elif shift == '10':
            new_shift_type.append(Constants.RECOGIDA)
            new_shift_duration.append(1)
        else:  # shift == '11'
            new_shift_type.append(Constants.DUAL)
            new_shift_duration.append(1)
    return new_shift_type, new_shift_duration


# MAIN
NUM_GENERATIONS = 50
NUM_INDIVIDUALS = 50
NUM_KEEP_BEST = int(2 * NUM_INDIVIDUALS / 5)  # 2/5
NUM_OFFSPRING = int(2 * NUM_INDIVIDUALS / 5)  # 2/5
CHANCE_KEEP_BAD = 0.05
CHANCE_MUTATION = 0.05

seed(664)  # seed tested: 6, 1, 21, 25, 200, 212, 60, 78, 1024, 789, 3379, 567, 4655, 878, 123, 46, 1221, 111, 777, 664
parameters = Parameters()

population = []

# Check consistency
while NUM_KEEP_BEST < 0 or NUM_OFFSPRING < 0 or NUM_KEEP_BEST + NUM_OFFSPRING > NUM_INDIVIDUALS:
    print('NUM_KEEP_BEST + NUM_OFFSPRING cannot be higher than', NUM_INDIVIDUALS)
    NUM_KEEP_BEST = int(input('Enter new value for NUM_KEEP_BEST:'))
    NUM_OFFSPRING = int(input('Enter new value for NUM_OFFSPRING:'))

# GEN 0
while len(population) < NUM_INDIVIDUALS:
    gen_individual = get_new_individual()
    population.append(gen_individual)

# Begin selection
fitness = {}
for generation in range(NUM_GENERATIONS):
    print('Generation', generation)
    for individual in population:
        if individual not in fitness:
            shift_type, shift_duration = individual_to_parameters(individual)
            parameters.setParameters(shift_duration, shift_type, 3600)
            print('    Testing ' + individual + '...')
            core = Core()
            core.run()
            fitness[individual] = Auxiliary.get_fitness(parameters.output_file)
    population = sorted(population, key=lambda idv: fitness[idv], reverse=True)
    if generation < NUM_GENERATIONS - 1:
        fittest = population[:NUM_KEEP_BEST]
        unfit = population[NUM_KEEP_BEST:]
        population = fittest
        while len(population) < NUM_KEEP_BEST + NUM_OFFSPRING:
            individual1, individual2 = sample(fittest, 2)
            population.append(operator_crossover(individual1, individual2))
        while len(population) < NUM_INDIVIDUALS:
            if random() < CHANCE_KEEP_BAD:
                population.append(unfit[NUM_INDIVIDUALS - len(population) - 1])
            else:
                population.append(get_new_individual())
        for ind in range(len(population)):
            if random() < CHANCE_MUTATION:
                population[ind] = operator_mutation(population[ind])

# Select first (best)
print('\nBest configuration:')
best = population[0]
print(best)
best_type, best_duration = individual_to_parameters(best)
print(str(best_type))
print(str(best_duration))
print('Sum of idle time squared (magnitude):', fitness[best])

# Sets trace to best configuration
parameters.setParameters(best_duration, best_type, 3600)
core = Core()
core.run()
