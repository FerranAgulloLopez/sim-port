import sys
import getopt

from queue import PriorityQueue

from Event import Event
from Processor import Processor
from Source import Source


class Core:

    # CLASS CONSTANTS

    # Time constants (in seconds)
    SIMULATION_INITIAL_TIME = 6 * 60 * 60  # 6:00:00 h = 21600 s
    SIMULATION_DURATION = 20 * 60 * 60  # 20:00:00 h = 72000 s

    # Event names
    START_SIMULATION = 'START_SIMULATION'
    NEXT_ARRIVAL = 'NEXT_ARRIVAL'
    END_SERVICE = 'END_SERVICE'
    END_SIMULATION = 'END_SIMULATION'

    # TODO:
    # MAX_QUEUE = 89  # no importa si fan cua dins o fora, es pot ignorar (?) confirmar
    # NUM_PROCESSORS = 12  # considerem totes les grues com un unic servidor (?) confirmar

    # CLASS ATTRIBUTES

    sources = []
    processors = []
    resources = []

    eventsList = PriorityQueue(0)  # maxsize = 0 (infinite)
    previousTime = SIMULATION_INITIAL_TIME
    currentTime = SIMULATION_INITIAL_TIME
    idleProcessors = 0
    serviceProcessors = 0
    queueLength = 0
    maxQueueLength = 0
    entitiesSystem = 0

    # CLASS FUNCTIONS

    def __init__(self, sources, processors, resources):
        for _ in range(0, sources):
            self.sources.append(Source(self))
        for _ in range(0, processors):
            self.processors.append(Processor(self))
        for _ in range(0, resources):
            pass

    def startSimulation(self):
        """Implemented by all components"""
        startEvent = Event(
            self,
            self.START_SIMULATION,
            self.currentTime,
            self.currentTime
        )
        self.logEvent(startEvent)
        for source in self.sources:
            source.startSimulation()
        for processor in self.processors:
            processor.startSimulation()

    def executeEvent(self, currentEvent):
        """Implemented by all components"""
        if currentEvent.eventName == self.START_SIMULATION:
            self.startSimulation()

    def endSimulation(self):
        """Implemented by all components"""
        endEvent = Event(
            self,
            self.END_SIMULATION,
            self.currentTime,
            self.currentTime
        )
        self.logEvent(endEvent)

    def run(self):
        self.logHeaders()
        self.startSimulation()
        while not self.eventsList.empty():
            currentEvent = self.eventsList.get()
            self.updateState(currentEvent)
            self.logEvent(currentEvent)
            currentEvent.executeEvent()
        self.endSimulation()
        self.stats()  # DEBUG

    def addEvent(self, addedEvent):
        self.eventsList.put(addedEvent, addedEvent.eventTime)

    def updateState(self, event):
        self.previousTime = self.currentTime
        self.currentTime = event.eventTime
        timeStep = self.currentTime - self.previousTime
        for processor in self.processors:
            if processor.idle:
                self.idleProcessors += timeStep
            else:
                self.serviceProcessors += timeStep

    def logHeaders(self):
        print('Current_Time', end=',')
        print('Event_Name', end=',')
        print('Event_Scheduled', end=',')
        print('Event_Time', end=',')
        print('Idle_Processors', end=',')
        print('Service_Processors', end=',')
        print('Queue_Length', end=',')
        print('Entities_System')

    def logEvent(self, currentEvent):
        print(self.currentTime, end=',')
        print(currentEvent.eventName, end=',')
        print(currentEvent.eventScheduled, end=',')
        print(currentEvent.eventTime, end=',')
        print(self.idleProcessors, end=',')
        print(self.serviceProcessors, end=',')
        print(self.queueLength, end=',')
        print(self.entitiesSystem)

    def stats(self):
        print('Max_Queue_Length', self.maxQueueLength)


# MAIN FUNCTION


if __name__ == "__main__":

    # Default arguments
    sources = 1
    processors = 1
    resources = 0

    # Get arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:p:r', [
                                   '--sources=', '--processors=', '--resources='])
        for opt, arg in opts:
            if opt in ('-s', '--sources'):
                sources = int(arg)
            if opt in ('-p', '--processors'):
                processors = int(arg)
            if opt in ('-r', '--resources'):
                resources = int(arg)
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    
    # Start core
    core = Core(sources, processors, resources)
    core.run()


def usage():
    print('Core [-s sources] [-p processors] [-r resources]')
