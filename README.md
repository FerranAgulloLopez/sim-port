# Simulation of the Port of Barcelona

_This program was created as a result of a university project in the Barcelona School of Informatics.

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
    - definitions.py: declares variables related to the paths used in the project

### Main functionalities

This project has five different runnable modules each one with a specific purpose.

    - Core.py: Runs the simulation with the params specified in the Constants and Parameters classes.
     It asks for the composition of the different time-slots when they are activated. It generates 
     two traces that describe the execution
    
    - Experimenter.py: Runs the simulation with the params specified in the Constants and Parameters 
    classes. It takes the time-slots configuration from the specified input file. It generates two 
    traces that describe the execution
    
    - Optimizer.py: Runs a genetic algorithm to find an approximation to the best configuration
    
    - ViewController.py: Runs a web server in localhost to visualize a execution loaded from one 
    specified trace file. It displays different charts that show the main features of the 
    chosen execution
    
    - TestRunner.py: Allows the user to select and run automatic tests through a CLI interface

### How to install

Next instructions are mandatory to configure the service in Linux

    - Install python3, python3-venv and pip3: sudo apt-get install python3 python3-venv pip3
    - Install virtualenv: python3 -m pip install --user virtualenv
    - Generate a virtual environment: python3 -m venv env
    - Activate the virtual environment: source env/bin/activate
    - Install component dependencies with the requirements file: pip3 install -r requirements.txt
    - Configure python path. Type the next commands in terminal changing the path to your project folder path: 
        - PYTHONPATH=$PYTHONPATH:/home/user/documents/sim-port/src  # or your path to sim-port/src
        - export PYTHONPATH

Next instructions are mandatory to configure the service in Windows

    - Install python3 and pip3
    - Install virtualenv: python3 -m pip install --user virtualenv
    - Generate a virtual environment: python3 -m venv env
    - Activate the virtual environment: source env/bin/activate
    - Install component dependencies with the requirements file: pip3 install -r requirements.txt

### How to use it

To run the different modules follow the next instructions

1. Run Core
    
    python -m src.Core [options]
    Options:
    -h, --help              Shows the program usage help.
    -p, --processors=...    Sets the number of processors.
    
2. Run Experimenter

    python -m src.Experimenter ../input/testInput.txt
    
3. Run Optimizer

    python -m src.Optimizer

4. Run ViewController (go to http://127.0.0.1:8050/)

    python -m src.ViewController

5. Run tests

    python -m test.TestRunner
    Next, the user would have to enter which type of tests he wants to run or wheter or 
    whether he wants to stop the execution of the program:
        a - All
        u - Unit Tests
        i - Integration Tests
        s - System Tests
        x - Exit
    
## License

Free use of this software is granted under the terms of the Apache License 2.0
