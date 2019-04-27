from numpy import random

class Random:

    # CLASS ATTRIBUTES

    SOURCE_PROB = 0.02450346
    PROCESSOR_PROB = prob = 0.03660948

    # CLASS FUNCTIONS

    def __init__(self):
        random.seed(0)

    def sourceIncrement(self):
        return random.geometric(self.SOURCE_PROB)
    
    def processorIncrement(self):
        return random.geometric(self.PROCESSOR_PROB)

    # TODO: Funciones por jornada
