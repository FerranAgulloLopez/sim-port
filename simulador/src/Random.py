from numpy import random
from src.Constants import Constants
from src.schemas import TriangularParametersSchema

# TODO: modificar self.numRecogida, self.numEntrega, self.numDual (dist triangular)

# Singleton Pattern
class _Random:
    _instance = None

    # Variable para lambda -> exponencial

    def __init__(self):
        self.initialization()

    def initialization(self):
        random.seed(0)
        # se hace getNumTrucks para las tres
        self.numTrucksEntrega = self.getNumTrucks(Constants.ENTREGA)
        self.numTrucksRecogida = self.getNumTrucks(Constants.RECOGIDA)
        self.numTrucksDual = self.getNumTrucks(Constants.DUAL)
        self.LAMBDA_Entrega =
        self.LAMBDA_Recogida =
        self.LAMBDA_Dual =

    def getNumTrucks(self, operationType):
        if operationType == Constants.ENTREGA:
            return random.triangular(Constants.MINIMUM_TRUCKS_ENTREGA, Constants.MEDIAN_TRUCKS_ENTREGA,
                                     Constants.MAXIMUM_TRUCKS_ENTREGA)
        elif operationType == Constants.RECOGIDA:
            return random.triangular(Constants.MINIMUM_TRUCKS_RECOGIDA, Constants.MEDIAN_TRUCKS_RECOGIDA,
                                     Constants.MAXIMUM_TRUCKS_RECOGIDA)
        else:  # DUAL
            return random.triangular(Constants.MINIMUM_TRUCKS_DUAL, Constants.MEDIAN_TRUCKS_DUAL,
                                     Constants.MAXIMUM_TRUCKS_DUAL)

    def sourceIncrement(self, operationType):
        if operationType == Constants.ENTREGA:
            return random.exponential(Constants.BETA_ENTREGA)
        elif operationType == Constants.RECOGIDA:
            return random.exponential(Constants.BETA_RECOGIDA)
        else:  # DUAL
            return random.exponential(Constants.BETA_DUAL)

    def processorIncrement(self, shift):
        if shift == Constants.ENTREGA:
            return random.uniform(Constants.MINIMUM_TIME_ENTREGA, Constants.MAXIMUM_TIME_ENTREGA)
        elif shift == Constants.RECOGIDA:
            return random.uniform(Constants.MINIMUM_TIME_RECOGIDA, Constants.MAXIMUM_TIME_RECOGIDA)
        else:  # DUAL
            return random.uniform(Constants.MINIMUM_TIME_DUAL, Constants.MAXIMUM_TIME_DUAL)

def Random():
    if _Random._instance is None:
        _Random._instance = _Random()
    return _Random._instance
