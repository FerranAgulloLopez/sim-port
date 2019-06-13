from definitions import ROOT_DIR


class Constants:
    INPUT_PATH = ROOT_DIR + 'input/'
    OUTPUT_PATH = ROOT_DIR + '/output/'

    # Infrastructure usage restrictions
    MAX_CAPACITY_USAGE = 70

    # Default values
    DEFAULT_SOURCES = 1
    DEFAULT_PROCESSORS = 52

    # Queue
    SLOTS_QUEUE = 90
    SLOTS_BUFFER = 0  # unlimited

    # Time constants (in seconds)
    SIMULATION_INITIAL_TIME = 6 * 60 * 60  # 6:00:00 h = 21600 s
    SIMULATION_FINAL_TIME = 20 * 60 * 60  # 20:00:00 h = 72000 s
    SIMULATION_DURATION = SIMULATION_FINAL_TIME - SIMULATION_INITIAL_TIME

    # Event names
    START_SIMULATION = 'START_SIMULATION'
    NEXT_ARRIVAL = 'NEXT_ARRIVAL'
    END_SERVICE = 'END_SERVICE'
    END_SIMULATION = 'END_SIMULATION'

    # Operation / shift names
    RECOGIDA = "RECOGIDA"
    ENTREGA = "ENTREGA"
    DUAL = "DUAL"

    # TODO: cambiar (5 primeros...)
    # Processor parameters
    MINIMUM_TIME_ENTREGA = 1018
    MAXIMUM_TIME_ENTREGA = 1018

    MINIMUM_TIME_RECOGIDA = 1517
    MAXIMUM_TIME_RECOGIDA = 1517

    MINIMUM_TIME_DUAL = 1957
    MAXIMUM_TIME_DUAL = 1957

    MINIMUM_TIME = 1578
    MAXIMUM_TIME = 1578

    # Source parameters
    BETA_ENTREGA = 340
    LAMBDA_ENTREGA = 1 / BETA_ENTREGA

    BETA_RECOGIDA = 360
    LAMBDA_RECOGIDA = 1 / BETA_RECOGIDA

    BETA_DUAL = 475
    LAMBDA_DUAL = 1 / BETA_DUAL

    # Spawn of Trucks
    MINIMUM_TRUCKS_ENTREGA = 390
    MAXIMUM_TRUCKS_ENTREGA = 637
    MEDIAN_TRUCKS_ENTREGA = 473

    MINIMUM_TRUCKS_RECOGIDA = 294
    MAXIMUM_TRUCKS_RECOGIDA = 653
    MEDIAN_TRUCKS_RECOGIDA = 471

    MINIMUM_TRUCKS_DUAL = 212
    MAXIMUM_TRUCKS_DUAL = 464
    MEDIAN_TRUCKS_DUAL = 380

    MINIMUM_TRUCKS = 1075
    MAXIMUM_TRUCKS = 1452
    MEDIAN_TRUCKS = 1313
