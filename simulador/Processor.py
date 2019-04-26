import numpy

# from Core import Core
from Event import Event


class Processor:

    # CLASS ATTRIBUTES

    core = None
    
    inputList = []
    outputList = []
    idle = True

    # CLASS FUNCTIONS

    def __init__(self, core):
        self.core = core
        numpy.random.seed(0)
    
    def addInput(self, inputElement):
        self.inputList.append(inputElement)
    
    def addOutput(self, outputElement):
        self.outputList.append(outputElement)
    
    def removeInput(self, inputIndex):
        self.inputList.pop(inputIndex)
    
    def removeOutput(self, outputIndex):
        self.outputList.pop(outputIndex)

    def startSimulation(self):
        """Implemented by all modules"""
        pass

    def endSimulation(self):
        """Implemented by all modules"""
        pass

    def executeEvent(self, currentEvent):
        if currentEvent.eventName == self.core.END_SERVICE:
            self.endService()
        pass

    def scheduleEndService(self):
        self.idle = False
        prob = 0.03660948
        serviceIncrement = numpy.random.geometric(prob)
        endServiceEvent = Event(
            self,
            self.core.END_SERVICE,
            self.core.currentTime,
            self.core.currentTime + serviceIncrement
        )
        return endServiceEvent

    def endService(self):
        self.core.entitiesSystem -= 1
        if self.core.queueLength > 0:
            self.core.queueLength -= 1
            endServiceEvent = self.scheduleEndService()
            self.core.addEvent(endServiceEvent)
        else:
            self.idle = True
