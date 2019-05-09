from src.Constants import Constants
from src.Event import Event
from src.Random import Random

class Processor:

    # CLASS ATTRIBUTES

    core = None

    # CLASS FUNCTIONS

    def __init__(self, core):
        self.core = core
        self.hostedEntity = None
        self.inputModule = None

    def addInput(self, inputModule):
        self.inputModule = inputModule

    def removeInput(self):
        self.inputModule = None

    def isIdle(self):
        return not self.hostedEntity

    def canHostEntity(self):
        return self.isIdle()

    def executeEvent(self, currentEvent):
        """Implemented by all event creator modules"""
        if currentEvent.eventName == Constants.END_SERVICE:
            self.endService()

    def nextArrival(self, entity):
        self.hostedEntity = entity
        endServiceEvent = self.scheduleEndService()
        self.core.addEvent(endServiceEvent)

    def scheduleEndService(self):
        operationType = self.hostedEntity.getOperationType()
        rand = Random()
        serviceIncrement = rand.processorIncrement(operationType)
        endServiceEvent = Event(
            self,                                     # eventCreator
            Constants.END_SERVICE,                    # eventName
            self.core.currentTime,                    # eventScheduled
            self.core.currentTime + serviceIncrement  # eventTime
        )
        return endServiceEvent

    def endService(self):
        self.core.decreaseEntitiesSystem()
        if self.inputModule.getQueueLength() > 0:
            self.inputModule.getEntity(self)
        else:
            self.hostedEntity = None
