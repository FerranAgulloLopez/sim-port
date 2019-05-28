import os
import subprocess
import sys

from src.Constants import Constants
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
    with open(inputFile, 'r') as ifs:
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

                with open(output_file, 'w+') as ofs:
                    # NOTE: switch as needed between python3, py
                    # cmd = ['python3', './Core.py', '-e', '-p', str(args[1])]
                    cmd = ['py', './Core.py', '-e', '-p', str(args[1])]
                    subprocess.Popen(cmd)
                # TODO: analyze trace
                with open(output_file, 'r') as ofs:
                    # TODO: read idle times by shift, more idle time = better (less workers needed)
                    # TODO: update best configuration
                    pass
        # TODO: print best configuration
