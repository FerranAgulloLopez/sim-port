from Constants import Constants
from Event import Event


class Source:

    # CLASS ATTRIBUTES

    core = None
    random = None
    outputModule = None

    # CLASS FUNCTIONS

    def __init__(self, core, random):
        self.core = core
        self.random = random
    
    def addOutput(self, outputModule):
        self.outputModule = outputModule
    
    def removeOutput(self):
        self.outputModule = None

    def scheduleNextArrival(self):
        arrivalIncrement = self.random.sourceIncrement()
        arrivalEvent = Event(
            self,
            Constants.NEXT_ARRIVAL,
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
        """Implemented by all event creator modules"""
        if currentEvent.eventName == Constants.NEXT_ARRIVAL:
            self.nextArrival()

    def nextArrival(self):
        self.core.increaseEntitiesSystem()
        self.outputModule.nextArrival()
        if self.core.currentTime < Constants.SIMULATION_DURATION:
            arrivalEvent = self.scheduleNextArrival()
            self.core.addEvent(arrivalEvent)
