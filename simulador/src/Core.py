import sys
import getopt

from queue import PriorityQueue

from Constants import Constants
from Event import Event
from Processor import Processor
from Queue import Queue
from Random import Random
from Source import Source
from Parameters import Parameters
from Auxiliary import Auxiliary

class Core:

    # CLASS ATTRIBUTES

    buffer = None
    processors = []
    queue = None
    random = None
    sources = []

    eventsList = PriorityQueue(0)  # maxsize = 0 (infinite)
    previousTime = Constants.SIMULATION_INITIAL_TIME
    currentTime = Constants.SIMULATION_INITIAL_TIME
    idleProcessors = 0
    serviceProcessors = 0
    entitiesSystem = 0

    # CLASS FUNCTIONS

    def __init__(self, processors, sources):
        # Instance creation
        self.buffer = Queue(Constants.SLOTS_BUFFER)
        self.queue = Queue(Constants.SLOTS_QUEUE)
        self.random = Random()
        for _ in range(0, processors):
            self.processors.append(Processor(self))
        for _ in range(0, sources):
            self.sources.append(Source(self))
        # Dependency injection
        for source in self.sources:
            source.addOutput(self.buffer)    # source -> buffer
        self.buffer.addOutput(self.queue)    # buffer -> queue
        self.queue.addInput(self.buffer)     # queue <- buffer
        for processor in self.processors:
            self.queue.addOutput(processor)  # queue -> processor
            processor.addInput(self.queue)   # processor <- queue

    def increaseEntitiesSystem(self):
        self.entitiesSystem += 1

    def decreaseEntitiesSystem(self):
        self.entitiesSystem -= 1

    def startSimulation(self):
        """Implemented by all modules"""
        startEvent = Event(
            self,
            Constants.START_SIMULATION,
            self.currentTime,
            self.currentTime
        )
        self.logEvent(startEvent)
        for source in self.sources:
            source.startSimulation()

    def endSimulation(self):
        """Implemented by all modules"""
        endEvent = Event(
            self,                      # eventCreator
            Constants.END_SIMULATION,  # eventName
            self.currentTime,          # eventScheduled
            self.currentTime           # eventTime
        )
        self.logEvent(endEvent)

    def executeEvent(self, currentEvent):
        """Implemented by all event creator modules"""
        if currentEvent.eventName == Constants.START_SIMULATION:
            self.startSimulation()

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
    
    def getCurrentTime(self):
        return self.currentTime

    def getCurrentShift(self):
        seconds_incremental = []
        accum = 0
        seconds_incremental.append(accum)
        for i in Parameters.shift_duration:
            accum += i*Parameters.shift_factor
            seconds_incremental.append(accum)
        aux = Auxiliary()
        index = aux.binarySearch(seconds_incremental, 0, len(seconds_incremental), self.currentTime)
        return Parameters.shift_type[index]

    def updateState(self, event):
        self.previousTime = self.currentTime
        self.currentTime = event.eventTime
        timeStep = self.currentTime - self.previousTime
        for processor in self.processors:
            if processor.isIdle():
                self.idleProcessors += timeStep
            else:
                self.serviceProcessors += timeStep

    def logHeaders(self):
        s = 'Current_Time,'
        s += 'Event_Name,'
        s += 'Event_Scheduled,'
        s += 'Event-Time,'
        s += 'Idle_Processors,'
        s += 'Service_Processors,'
        s += 'Buffer_Length,'
        s += 'Queue_Length,'
        s += 'Entities_System'
        print(s)
        f = open("trace.csv", "w+")
        f.write(s+'\n')
        f.close()

    def logEvent(self, currentEvent):
        s = str(self.currentTime) + ','
        s += currentEvent.eventName + ','
        s += str(currentEvent.eventScheduled) + ','
        s += str(currentEvent.eventTime) + ','
        s += str(self.idleProcessors) + ','
        s += str(self.serviceProcessors) + ','
        s += str(self.buffer.getQueueLength()) + ','
        s += str(self.queue.getQueueLength()) + ','
        s += str(self.entitiesSystem)
        print(s)
        f = open("trace.csv", "a+") # abrir el fichero en otro sitio, para no tener que abrirlo por cada evento
        f.write(s+'\n')
        f.close()

    def stats(self):
        print('Max_Queue_Length', self.queue.getMaxQueueLength())


def usage():
    print('Core.py [options]')
    print('Model: source(s) -> queue -> processor(s) -> sink')
    print('Options:')
    print('-h, --help\t\tShows the program usage help.')
    print('-p, --processors=...\tSets the number of processors.')
    print('-s, --sources=...\tSets the number of sources.')


# MAIN FUNCTION
if __name__ == "__main__":

    # Default arguments
    sources = Constants.DEFAULT_SOURCES
    processors = Constants.DEFAULT_PROCESSORS

    # Get arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:s:', [
                                   'help', 'processors=', 'sources='])
        for opt, arg in opts:
            if opt in ('-h, --help'):
                usage()
                sys.exit()
            if opt in ('-p', '--processors'):
                processors = int(arg)
            if opt in ('-s', '--sources'):
                sources = int(arg)
    except getopt.GetoptError:
        usage()
        sys.exit()

    # Start core
    core = Core(processors, sources)
    core.run()
