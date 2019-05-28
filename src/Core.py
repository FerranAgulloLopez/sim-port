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

    def __init__(self):

        # TODO: set instance Parameters shift duration

        num_sources = Constants.DEFAULT_SOURCES
        num_processors = parameters.num_processors
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
        f = open(parameters.output_file, "w+")
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
        f = open(parameters.output_file, "a+")
        # TODO: abrir el fichero en otro sitio, para no tener que abrirlo por cada evento
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
          'Must add up to', int(Constants.SIMULATION_DURATION / 3600))


# MAIN FUNCTION
if __name__ == "__main__":

    # Default arguments
    processors = Constants.DEFAULT_PROCESSORS
    flag_experimenter = False
    shift_duration = []
    shift_type = []
    shift_factor = 0

    parameters = Parameters()

    # Get arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:e', [
            'help', 'processors=', 'experimenter'])
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                usage()
                sys.exit()
            if opt in ('-p', '--processors'):
                num_processors = int(arg)
                parameters.setNumProcessors(num_processors)
            if opt in ('-e', '--experimenter'):
                flag_experimenter = True
    except getopt.GetoptError:
        usage()
        sys.exit()

    duration_total = 0
    if not flag_experimenter:
        while duration_total < Constants.SIMULATION_DURATION/3600:
            in_shift_type = str(input('Enter shift type:'))
            in_shift_duration = int(input('Enter shift duration in hours:'))
            if duration_total + in_shift_duration <= Constants.SIMULATION_DURATION/3600 and \
                    in_shift_type in (Constants.ENTREGA, Constants.RECOGIDA, Constants.DUAL):
                duration_total += in_shift_duration
                shift_duration.append(in_shift_duration)
                shift_type.append(in_shift_type)
            else:
                print('Not enough time. Remaining time is', Constants.SIMULATION_DURATION/3600 - duration_total)
        # Still inside if not flag_experimenter
        parameters.setParameters(shift_duration, shift_type, shift_factor)
    # else, set by Experimenter

    # DEBUG BEGIN
    with open("debug_info.txt", "w+") as dbg:
        dbg.write(str(parameters.shift_type) + '\n')
        dbg.write(str(parameters.shift_duration) + '\n')
        dbg.write(str(parameters.shift_factor) + '\n')
    # DEBUG END

    # Start core
    core = Core()
    core.run()
