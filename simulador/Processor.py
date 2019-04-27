from Constants import Constants
from Event import Event


class Processor:

    # CLASS ATTRIBUTES

    core = None
    random = None
    inputModule = None
    idle = True

    # CLASS FUNCTIONS

    def __init__(self, core, random):
        self.core = core
        self.random = random
    
    def addInput(self, inputModule):
        self.inputModule = inputModule
    
    def removeInput(self, inputIndex):
        self.inputModule = None

    def isIdle(self):
        return self.idle

    def startSimulation(self):
        """Implemented by all modules"""
        pass

    def endSimulation(self):
        """Implemented by all modules"""
        pass

    def executeEvent(self, currentEvent):
        """Implemented by all event creator modules"""
        if currentEvent.eventName == Constants.END_SERVICE:
            self.endService()
        pass
    
    def nextArrival(self):
        endServiceEvent = self.scheduleEndService()
        self.core.addEvent(endServiceEvent)

    def scheduleEndService(self):
        self.idle = False
        serviceIncrement = self.random.processorIncrement()
        endServiceEvent = Event(
            self,
            Constants.END_SERVICE,
            self.core.currentTime,
            self.core.currentTime + serviceIncrement
        )
        return endServiceEvent

    def endService(self):
        self.core.decreaseEntitiesSystem()
        if self.inputModule.getQueueLength() > 0:
            self.inputModule.decreaseQueueLength()
            endServiceEvent = self.scheduleEndService()
            self.core.addEvent(endServiceEvent)
        else:
            self.idle = True
