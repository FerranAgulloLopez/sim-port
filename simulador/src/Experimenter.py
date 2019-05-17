import sys
import subprocess

from Core import Core


def usage():
    print('Experimenter.py inputFile')
    print('inputFile format: <sources> <processors> <outputFile>')


# MAIN FUNCTION
if __name__ == "__main__":

    # Default arguments
    sources = 8
    processors = 52

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
                    wd = subprocess.Popen(
                        ["pwd"], stdout=subprocess.PIPE).stdout.read().decode('utf-8')
                    cmd = ['python3', './Core.py', '-s',
                           str(args[0]), '-p', str(args[1])]
                    subprocess.Popen(cmd, stdout=ofs)
