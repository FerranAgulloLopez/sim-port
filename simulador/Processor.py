import numpy

from Event import Event


class Processor:

    # CLASS ATTRIBUTES

    core = None
    
    idle = True

    # CLASS FUNCTIONS

    def __init__(self, core):
        self.core = core
        numpy.random.seed(0)

    def startSimulation(self):
        """Implemented by all components"""
        pass

    def executeEvent(self, currentEvent):
        """Implemented by all components"""
        if currentEvent.eventName == self.core.END_SERVICE:
            self.endService()
        pass

    def endSimulation(self):
        """Implemented by all components"""
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
