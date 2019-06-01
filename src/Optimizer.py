from random import seed, random, randint

from src.Constants import Constants
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
"""


def first_shift_is_valid(individual):
    """ checks if the first shift is not an extension """
    return individual[:2] != '00'


def at_least_one_shift_each(individual):
    """ checks if there is at least one of each shift: 01, 10, 11 """
    num_entrega = 0
    num_recogida = 0
    num_dual = 0
    while individual:
        shift = individual[:2]
        individual = individual[2:]
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
    while len(new_individual) < 2 * Constants.SIMULATION_DURATION / 3600:
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
        for idx in range(int(len(first_individual)/2)):
            if randint(0, 1) > 0:
                new_individual += first_individual[2*idx:2*idx+2]
            else:
                new_individual += second_individual[2*idx:2*idx+2]
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
        idx = int(randint(0, len(old_individual)) / 2)
        old_shift = old_individual[2*idx:2*idx+2]
        new_shift = old_shift
        while new_shift == old_shift:
            new_shift = str(randint(0, 1)) + str(randint(0, 1))
            new_individual = old_individual[:2*idx] + new_shift + old_individual[2*idx+2:]
    return new_individual


def individual_to_parameters(individual):
    """ transforms an individual to a valid parameter configuration """
    shift_duration = []
    shift_type = []
    while individual:
        shift = individual[:2]
        individual = individual[2:]
        if shift == '00':
            shift_duration[-1] += 1
        elif shift == '01':
            shift_type.append(Constants.ENTREGA)
            shift_duration.append(1)
        elif shift == '10':
            shift_type.append(Constants.RECOGIDA)
            shift_duration.append(1)
        else:  # shift == '11'
            shift_type.append(Constants.DUAL)
            shift_duration.append(1)
    return shift_type, shift_duration


def fitness(_):  # unused param needed
    """ reads stats from the default output_file and determines the viability and benefits """
    with open('../output/' + parameters.output_file + '.stats.csv', 'r') as ifs:
        pass


# DEBUG
# NOTE: these are random, seed is fixed below
individual1 = get_new_individual()
individual2 = get_new_individual()
print('Crossover:')
print(individual1)
print(individual2)
print(operator_crossover(individual1, individual2))
print('Mutation:')
print(individual1)
print(operator_mutation(individual1))
print('Parameters:')
print(individual1)
shift_type, shift_duration = individual_to_parameters(individual1)
print(str(shift_type))
print(str(shift_duration))
#


# MAIN
NUM_GENERATIONS = 10
NUM_INDIVIDUALS = 10
NUM_KEEP_BEST = 4
CHANCE_KEEP_BAD = 0.05
CHANCE_MUTATION = 0.05

seed(6)
parameters = Parameters()

population = []

# GEN 0
for _ in range(NUM_INDIVIDUALS):
    new_individual = get_new_individual()
    population.append(new_individual)

# Begin selection
for generation in range(NUM_GENERATIONS):
    for individual in population:
        shift_type, shift_duration = individual_to_parameters(individual)
        # TODO: set parameters
        #  run core
        #  get fitness
        #  population = sorted(population, key = fitness)
        #  if generation < NUM_GENERATIONS - 1:
        #  unfit = population[NUM_KEEP_BEST:]
        #  population = population[:NUM_KEEP_BEST]
        #  apply crossover
        #  while len(population) < NUM_INDIVIDUALS:
        #  if random() < CHANCE_KEEP_BAD:
        #  population.append(unfit[len(population)])
        #  else
        #  population.append(get_new_individual())
        #  for idx in range(len(population)):
        #  if random() < CHANCE_MUTATION:
        #  population[idx] = operator_mutation(population[idx])
        pass

# Select first (best)
best = population[0]
print(best)
best_type, best_duration = individual_to_parameters(best)
print(str(best_type))
print(str(best_duration))
