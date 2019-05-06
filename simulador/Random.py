from numpy import random

class Random:

    # CLASS ATTRIBUTES

    core = None

    # TODO: borrar cuando tengamos las distribuciones buenas
    SOURCE_PROB = 0.02450346
    PROCESSOR_PROB = prob = 0.03660948

    numRecogida = 0
    numEntrega = 0
    numDual = 0

    # CLASS FUNCTIONS

    def __init__(self, core):
        random.seed(0)
        self.core = core
        # TODO: modificar self.numRecogida, self.numEntrega, self.numDual (dist triangular)

    def sourceIncrement(self, operationType):
        return random.geometric(self.SOURCE_PROB)
        # TODO: switch operationType
            # devolver incremento de tiempo obtenido con exponencial de parametro=(1/numero camiones)
    
    def processorIncrement(self, shift):
        return random.geometric(self.PROCESSOR_PROB)
        # TODO: switch shift
            # devolver incremento de tiempo obtenido con uniforme
