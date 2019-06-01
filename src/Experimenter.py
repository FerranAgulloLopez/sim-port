import os
import subprocess
import sys

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

    # DEBUG BEGIN
    # print(inputFile)
    # DEBUG END

    # Start core
    with open('../input/' + inputFile, 'r') as ifs:
        best_configuration = ''
        best_idle = 0
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
                while duration_total < Constants.SIMULATION_DURATION/3600:
                    in_shift_type = str(args[idx])
                    in_shift_duration = int(args[idx + 1])
                    idx += 2
                    if duration_total + in_shift_duration <= Constants.SIMULATION_DURATION/3600 and \
                            in_shift_type in (Constants.ENTREGA, Constants.RECOGIDA, Constants.DUAL):
                        duration_total += in_shift_duration
                        shift_duration.append(in_shift_duration)
                        shift_type.append(in_shift_type)
                    else:
                        raise Exception('Wrong format: time limit exceeded.')
                parameters.setParameters(shift_duration, shift_type, shift_factor)

                output_file = str(args[0])
                # print(output_file)
                parameters.output_file = output_file

                # RUN CORE
                path_list = output_file.split('/')
                filename = str(path_list[len(path_list)-1:][0])
                s = '[Configuration: ' + filename + ']\n'
                s += '    Parameters set.'
                print(s)
                core = Core()
                core.run()

                with open('../output/' + output_file + '.stats.csv', 'r') as ifs2:
                    total_service = 0
                    total_idle = Constants.SIMULATION_DURATION * parameters.num_processors
                    exceeds_capacity = False
                    headers = ifs2.readline()[:-1].split(',')
                    data = ifs2.readline()[:-1].split(',')
                    for idx in range(len(headers)):
                        if headers[idx] == 'Shift_Type':
                            duration = float(data[idx+1])
                            capacity_usage = float(data[idx+2])
                            if capacity_usage > 70.0:
                                exceeds_capacity = True
                            total_service += capacity_usage * duration * parameters.num_processors
                    total_idle -= total_service
                    if not exceeds_capacity and total_idle > best_idle:
                        best_idle = total_idle
                        best_configuration = filename
        print('\nBest configuration: ' + best_configuration)
