from numpy import random

class Random:

    # CLASS ATTRIBUTES

    SOURCE_PROB = 0.02450346
    PROCESSOR_PROB = prob = 0.03660948

    # añadir atributos:
    # numero camiones 1
    # numero camiones 2
    # numero camiones 3

    # CLASS FUNCTIONS

    def __init__(self):
        random.seed(0)

    def sourceIncrement(self):
        return random.geometric(self.SOURCE_PROB)
    
    def processorIncrement(self):
        return random.geometric(self.PROCESSOR_PROB)

    # TODO: Funciones por jornada

    # modificar "init" calcular numero de camiones franja parametro: franja
        # Triangular 1
        # Triangular 2
        # Triangular 3
        # guardar en atributo
    
    # adaptar processorIncrement parametro: franja (o tiempo y determinar franja)
        # devolver tiempo constante de operacion que toque en esa franja (uniforme)

    # adapta sourceIncrement parametro: franja (o tiempo y determinar franja)
        # switch franja
            # devolver incremento de tiempo obtenido con exponencial de parametro=(1/numero camiones)
