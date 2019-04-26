import numpy

# from Core import Core
from Event import Event


class Source:

    # CLASS ATTRIBUTES

    core = None

    outputList = []

    # CLASS FUNCTIONS

    def __init__(self, core):
        self.core = core
        numpy.random.seed(0)
    
    def addOutput(self, outputElement):
        self.outputList.append(outputElement)
    
    def removeOutput(self, outputIndex):
        self.outputList.pop(outputIndex)

    def scheduleNextArrival(self):
        prob = 0.02450346
        arrivalIncrement = numpy.random.geometric(prob)
        arrivalEvent = Event(
            self,
            self.core.NEXT_ARRIVAL,
            self.core.currentTime,
            self.core.currentTime + arrivalIncrement
        )
        return arrivalEvent

    def startSimulation(self):
        """Implemented by all modules"""
        arrivalEvent = self.scheduleNextArrival()
        self.core.addEvent(arrivalEvent)

    def endSimulation(self):
        """Implemented by all modules"""
        pass

    def executeEvent(self, currentEvent):
        if currentEvent.eventName == self.core.NEXT_ARRIVAL:
            self.nextArrival()

    def nextArrival(self):
        self.core.entitiesSystem += 1
        processed = False
        for processor in self.core.processors:
            if processor.idle:
                processed = True
                endServiceEvent = processor.scheduleEndService()
                self.core.addEvent(endServiceEvent)
                break
        if not processed:
            self.core.queueLength += 1
            if self.core.queueLength > self.core.maxQueueLength:
                self.core.maxQueueLength = self.core.queueLength
        if self.core.currentTime < self.core.SIMULATION_DURATION:
            arrivalEvent = self.scheduleNextArrival()
            self.core.addEvent(arrivalEvent)
