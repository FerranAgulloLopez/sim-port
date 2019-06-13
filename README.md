# Simulation of the Barcelona port

_This service was created as a result of a university project in The Facultat d'Informàtica de Barcelona._

## Introduction

This component is a simulation of the APMTC terminal of the Barcelona port. The project is focused on improving the efficiency of the terminal by distributing the truck entries in distinct time slots according to their type of operation. 

## Technical description

Next sections provide a general overview of the technical details of the simulation service.

### Files distribution

    - src: this directory contains all the source code of the component
    - input: this directory contains the input file needed for running the experimenter class
    - output: this directory contains the output traces and the expected results for the different tests
    - test: this directory contains the tests source code
    - requirements.txt: this file contains all the libraries used to run the component

### Main functionalities

This project has four different runnable modules each one with a specific purpose.

    - Core.py: Runs the simulation with the params specified in the Constants and Parameters classes. It asks for the composition of the different time-slots when they are activated. It generates two traces that describe the execution
    - Experimenter.py: Runs the simulation with the params specified in the Constants and Parameters classes. It takes the time-slots configuration from the specified input file. It generates two traces that describe the execution
    - Optimizer.py: Runs a genetic algorithm to find the best configuration
    - ViewController.py: Runs a web server in localhost to visualize a execution loaded from one specified trace file. It displays different charts that show the main features of the chosen execution

### How to install

Next instructions are mandatory to configure the service in Linux

    - Install python3 and pip3
    - Install virtualenv: python3 -m pip install --user virtualenv
    - Generate a virtual environment: python3 -m venv env
    - Activate the virtual environment: source env/bin/activate
    - Install component dependencies with the requirements file: pip3 install -r requirements.txt
    - Configure python path. Type the next commands in terminal changing the path to your project folder path: 
        - PYTHONPATH=$PYTHONPATH:/home/user/documents/sim-port/src
        - export PYTHONPATH

### How to use it

Falta explicar los comandos para cada uno de los ejecutables: core, experimenter...

    python3 src/ViewController.py
    
    python3 src/Core.py -p 52
    
    ...

    Core.py [options]
    Options:
    -h, --help              Shows the program usage help.
    -p, --processors=...    Sets the number of processors.
    -s, --sources=...       Sets the number of sources.
    
## License

Free use of this software is granted under the terms of the Apache License 2.0
