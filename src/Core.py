import getopt
import sys
from queue import PriorityQueue

from src.Constants import Constants
from src.Event import Event
from src.Parameters import Parameters
from src.Processor import Processor
from src.Queue import Queue
from src.Random import Random
from src.Source import Source


class Core:
    # CLASS FUNCTIONS

    def __init__(self, processors=0, sources=0):
        # Attributes initialization
        self.processors = []
        self.sources = []
        self.eventsList = PriorityQueue(0)  # maxsize = 0 (infinite)
        self.previousTime = Constants.SIMULATION_INITIAL_TIME
        self.currentTime = Constants.SIMULATION_INITIAL_TIME
        self.idleProcessors = 0
        self.serviceProcessors = 0
        self.entitiesSystem = 0

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
            source.addOutput(self.buffer)  # source -> buffer
        self.buffer.addOutput(self.queue)  # buffer -> queue
        self.queue.addInput(self.buffer)  # queue <- buffer
        for processor in self.processors:
            self.queue.addOutput(processor)  # queue -> processor
            processor.addInput(self.queue)  # processor <- queue

        self.numberOfIdleProcessors = len(processors)

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
            self,  # eventCreator
            Constants.END_SIMULATION,  # eventName
            self.currentTime,  # eventScheduled
            self.currentTime  # eventTime
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

    def updateState(self, event):
        self.previousTime = self.currentTime
        self.currentTime = event.eventTime
        timeStep = self.currentTime - self.previousTime
        self.numberOfIdleProcessors = 0
        for processor in self.processors:
            if processor.isIdle():
                self.idleProcessors += timeStep
                self.numberOfIdleProcessors += 1
            else:
                self.serviceProcessors += timeStep

    def getCurrentShift(self):
        param = Parameters()
        return param.getCurrentShift(self.currentTime)

    def logHeaders(self):
        s = 'Current_Time,'
        s += 'Event_Name,'
        s += 'Event_Scheduled,'
        s += 'Event-Time,'
        s += 'Idle_Processors,'
        s += 'Service_Processors,'
        s += 'Number_Idle_Processors,'
        s += 'Buffer_Length,'
        s += 'Queue_Length,'
        s += 'Entities_System'
        print(s)
        f = open("../output/trace.csv", "w+")
        f.write(s + '\n')
        f.close()

    def logEvent(self, currentEvent):
        s = str(self.currentTime) + ','
        s += currentEvent.eventName + ','
        s += str(currentEvent.eventScheduled) + ','
        s += str(currentEvent.eventTime) + ','
        s += str(self.idleProcessors) + ','
        s += str(self.serviceProcessors) + ','
        s += str(self.numberOfIdleProcessors) + ','
        s += str(self.buffer.getQueueLength()) + ','
        s += str(self.queue.getQueueLength()) + ','
        s += str(self.entitiesSystem)
        print(s)
        f = open("../output/trace.csv",
                 "a+")  # abrir el fichero en otro sitio, para no tener que abrirlo por cada evento
        f.write(s + '\n')
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
