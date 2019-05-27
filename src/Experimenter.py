import subprocess
import sys


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
    with open(inputFile, 'r') as ifs:
        content = ifs.readlines()
        for line in content:
            if line:
                args = line.split()
                with open(str(args[2]), 'w+') as ofs:
                    cmd = ['python3', './Core.py', '-p', str(args[1])]
                    subprocess.Popen(cmd, stdout=ofs)
                # TODO: analyze trace
                with open(str(args[2]), 'r') as ofs:
                    # TODO: read idle times by shift, more idle time = better (less workers needed)
                    # TODO: update best configuration
                    pass
        # TODO: print best configuration
