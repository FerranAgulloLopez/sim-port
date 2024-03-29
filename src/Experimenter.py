import sys

from src import Auxiliary
from src.Constants import Constants
from src.Core import Core
from src.Parameters import Parameters


def usage():
    print('Experimenter.py inputFile')
    print('inputFile format: <processors> <outputFile>')


# MAIN FUNCTION
if __name__ == "__main__":

    # Get arguments
    try:
        inputFile = sys.argv[1]
    except:
        usage()
        sys.exit()

    # Start core
    with open(Constants.INPUT_PATH + inputFile, 'r') as ifs:
        population = []
        fitness = {}
        content = ifs.readlines()
        for line in content:
            if line:
                args = line.split()

                parameters = Parameters()

                shift_duration = []
                shift_type = []
                shift_factor = 3600
                duration_total = 0
                idx = 2
                while duration_total < Constants.SIMULATION_DURATION / 3600:
                    in_shift_type = str(args[idx])
                    in_shift_duration = int(args[idx + 1])
                    idx += 2
                    if duration_total + in_shift_duration <= Constants.SIMULATION_DURATION / 3600 and \
                            in_shift_type in (Constants.ENTREGA, Constants.RECOGIDA, Constants.DUAL):
                        duration_total += in_shift_duration
                        shift_duration.append(in_shift_duration)
                        shift_type.append(in_shift_type)
                    else:
                        raise Exception('Wrong format: time limit exceeded.')
                parameters.setParameters(shift_duration, shift_type, shift_factor)

                output_file = str(args[0])
                parameters.output_file = Constants.OUTPUT_PATH + output_file

                # RUN CORE
                path_list = output_file.split('/')
                filename = str(path_list[len(path_list) - 1:][0])
                if filename not in fitness:
                    population.append(filename)
                    s = '    Testing ' + filename + '...'
                    print(s)
                    core = Core()
                    core.run()
                    fitness[filename] = Auxiliary.get_fitness(parameters.output_file)

        population = sorted(population, key=lambda idv: fitness[idv], reverse=True)
        best = population[0]
        print('\nBest configuration: ' + best)
