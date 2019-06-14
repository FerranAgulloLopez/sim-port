from src.Constants import Constants
from src.Entity import Entity
from src.Event import Event
from src.Random import Random


class Source:
    # CLASS FUNCTIONS

    def __init__(self, core=None):
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
            self,  # eventCreator
            Constants.NEXT_ARRIVAL,  # eventName
            self.core.currentTime,  # eventSheduled
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
        if self.outputModule is not None:
            self.outputModule.nextArrival(entity)
            if self.core.currentTime < Constants.SIMULATION_FINAL_TIME:
                arrivalEvent = self.scheduleNextArrival()
                self.core.addEvent(arrivalEvent)
