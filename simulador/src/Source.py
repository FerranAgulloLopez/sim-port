from Constants import Constants
from Entity import Entity
from Event import Event
from Random import Random

class Source:

    # CLASS ATTRIBUTES

    core = None

    # CLASS FUNCTIONS

    def __init__(self, core):
        self.core = core
        self.outputModule = None

    def addOutput(self, outputModule):
        self.outputModule = outputModule

    def removeOutput(self):
        self.outputModule = None

    def scheduleNextArrival(self):
        shift = self.core.getCurrentShift()
        rand = Random()
        arrivalIncrement = rand.sourceIncrement(shift)
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
        entity = Entity(self.core.getCurrentShift())
        self.outputModule.nextArrival(entity)
        # TODO: (optional) check instead num of entities dispatched
        if self.core.currentTime < Constants.SIMULATION_DURATION:
            arrivalEvent = self.scheduleNextArrival()
            self.core.addEvent(arrivalEvent)
