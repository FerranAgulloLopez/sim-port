from Constants import Constants
from Entity import Entity
from Event import Event


class Source:

    # CLASS ATTRIBUTES

    core = None
    random = None

    # CLASS FUNCTIONS

    def __init__(self, core, random):
        self.core = core
        self.random = random
        self.outputModule = None

    def addOutput(self, outputModule):
        self.outputModule = outputModule

    def removeOutput(self):
        self.outputModule = None

    def scheduleNextArrival(self):
        shift = None  # TODO: set shift based o time
        arrivalIncrement = self.random.sourceIncrement(shift)
        arrivalEvent = Event(
            self,                                     # eventCreator
            Constants.NEXT_ARRIVAL,                   # eventName
            self.core.currentTime,                    # eventSheduled
            self.core.currentTime + arrivalIncrement  # eventTime
        )
        return arrivalEvent

    def startSimulation(self):
        arrivalEvent = self.scheduleNextArrival()
        self.core.addEvent(arrivalEvent)

    def executeEvent(self, currentEvent):
        """Implemented by all event creator modules"""
        if currentEvent.eventName == Constants.NEXT_ARRIVAL:
            self.nextArrival()

    def nextArrival(self):
        self.core.increaseEntitiesSystem()
        # TODO: set entity operationType based on time
        entity = Entity(Constants.DUAL)
        self.outputModule.nextArrival(entity)
        # TODO: (optional) check instead num of entities dispatched
        if self.core.currentTime < Constants.SIMULATION_DURATION:
            arrivalEvent = self.scheduleNextArrival()
            self.core.addEvent(arrivalEvent)
