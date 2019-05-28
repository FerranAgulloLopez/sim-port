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

    def __init__(self, num_processors=Constants.DEFAULT_PROCESSORS, shift_duration_1=6, shift_duration_2=7,
                 shift_duration_3=6):

        # TODO: set instance Parameters shift duration

        num_sources = Constants.DEFAULT_SOURCES
        parameters = Parameters()
        parameters.setNumProcessors(num_processors)
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
        self.queue = Queue(Constants.SLOTS_BUFFER)
        self.parking = Queue(Constants.SLOTS_QUEUE)
        self.random = Random()
        for _ in range(0, num_processors):
            self.processors.append(Processor(self))
        for _ in range(0, num_sources):
            self.sources.append(Source(self))
        # Dependency injection
        for source in self.sources:
            source.addOutput(self.queue)  # source -> queue
        self.queue.addOutput(self.parking)  # queue -> parking
        self.parking.addInput(self.queue)  # parking <- queue
        for processor in self.processors:
            self.parking.addOutput(processor)  # parking -> processor
            processor.addInput(self.parking)  # processor <- parking

        self.numberOfIdleProcessors = num_processors

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
        s += str(self.queue.getQueueLength()) + ','
        s += str(self.parking.getQueueLength()) + ','
        s += str(self.entitiesSystem)
        print(s)
        f = open("../output/trace.csv",
                 "a+")  # abrir el fichero en otro sitio, para no tener que abrirlo por cada evento
        f.write(s + '\n')
        f.close()

    def stats(self):
        print('Max_Queue_Length', self.parking.getMaxQueueLength())


def usage():
    print('Core.py [options]')
    print('Model: source -> queue -> parking -> processor(s) -> sink')
    print('Options:')
    print('-h, --help\t\t\t\tShows the program usage help.')
    print('-p, --processors=...\tSets the number of processors.')
    print('-sX, --shiftX=...\t\tSets shift duration in hours for shift X, where X = {1, 2, 3}. Minimum 2 required. '
          'Must add up to', int(Constants.SIMULATION_DURATION/3600))


# MAIN FUNCTION
if __name__ == "__main__":

    # Default arguments
    processors = Constants.DEFAULT_PROCESSORS
    shift_duration_1 = 0
    shift_duration_2 = 0
    shift_duration_3 = 0
    num_shifts_defined = 0

    # Get arguments
    try:
        # TODO: Cambiar nombres (?) ex: -1 -> -e, --shift1= -> --entregas= ...
        opts, args = getopt.getopt(sys.argv[1:], 'hp:1:2:3:', [
            'help', 'processors=', 'shift1=', 'shift2=', 'shift3='])
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                usage()
                sys.exit()
            if opt in ('-p', '--processors'):
                processors = int(arg)
            if opt in ('-1', '--shift1'):
                shift_duration_1 = int(arg)
                num_shifts_defined += 1
            if opt in ('-2', '--shift2'):
                shift_duration_2 = int(arg)
                num_shifts_defined += 1
            if opt in ('-3', '--shift3'):
                shift_duration_3 = int(arg)
                num_shifts_defined += 1
    except getopt.GetoptError:
        usage()
        sys.exit()

    if num_shifts_defined < 2 or (num_shifts_defined == 3 and
                                  shift_duration_1 + shift_duration_2 + shift_duration_3 !=
                                  Constants.SIMULATION_DURATION/3600):
        # DEBUG BEGIN
        print('p = ', processors, 'num_shifts_defined =', num_shifts_defined)
        print('s1 =', shift_duration_1, 's2 =', shift_duration_2, 's3 =', shift_duration_3)
        # DEBUG END
        usage()
        sys.exit()
    else:
        if not shift_duration_3:
            shift_duration_3 = int(Constants.SIMULATION_DURATION / 3600 - (shift_duration_1 + shift_duration_2))
        if not shift_duration_2:
            shift_duration_2 = int(Constants.SIMULATION_DURATION / 3600 - (shift_duration_1 + shift_duration_3))
        if not shift_duration_1:
            shift_duration_1 = int(Constants.SIMULATION_DURATION / 3600 - (shift_duration_2 + shift_duration_3))

    # DEBUG BEGIN
    print('DONE')
    print('s1 =', shift_duration_1, 's2 =', shift_duration_2, 's3 =', shift_duration_3)
    sys.exit()
    # DEBUG END

    # Start core
    core = Core(processors, shift_duration_1, shift_duration_2, shift_duration_3)
    core.run()
