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

    def __init__(self, parameters=None):
        if parameters is None:
            self.parameters = Parameters()
        else:
            self.parameters = parameters
        num_sources = Constants.DEFAULT_SOURCES
        num_processors = self.parameters.num_processors
        # Attributes initialization
        self.processors = []
        self.sources = []
        self.eventsList = PriorityQueue(0)  # maxsize = 0 (infinite)
        self.previousTime = Constants.SIMULATION_INITIAL_TIME
        self.currentTime = Constants.SIMULATION_INITIAL_TIME
        self.idleProcessors = 0
        self.serviceProcessors = 0
        self.entitiesSystem = 0
        self.service_per_shift = []
        self.service_per_total = []
        self.shift_next_index = 1
        self.shift_durations = self.parameters.getParameters()[1]
        self.shift_next_time = self.shift_durations[self.shift_next_index]

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
        self.output_file = None
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
        self.updateState(endEvent)
        # print('    Simulation finished.')

    def executeEvent(self, currentEvent):
        """Implemented by all event creator modules"""
        if currentEvent.eventName == Constants.START_SIMULATION:
            self.startSimulation()

    def run(self):
        # print('    Core running...')
        self.logHeaders()  # creates output file with flag w+
        with open(self.parameters.output_file + '.csv', "a+") as self.output_file:
            self.startSimulation()
            while not self.eventsList.empty():
                currentEvent = self.eventsList.get()
                self.updateState(currentEvent)
                self.logEvent(currentEvent)
                currentEvent.executeEvent()
            self.endSimulation()
            self.stats()

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

        if self.currentTime > self.shift_next_time * 3600:
            if self.shift_next_index < len(self.shift_durations):
                self.shift_next_time += self.shift_durations[self.shift_next_index]
                self.shift_next_index += 1
                if not self.service_per_shift:  # first shift - empty list; if == 0
                    self.service_per_shift.append(self.serviceProcessors)
                else:
                    self.service_per_shift.append(
                        self.serviceProcessors - self.service_per_total[-1])
                self.service_per_total.append(self.serviceProcessors)
        if event.eventName == Constants.END_SIMULATION and len(self.service_per_shift) < len(self.shift_durations):
            self.service_per_shift.append(self.serviceProcessors - self.service_per_total[-1])

    def getCurrentShift(self):
        # print("DEBUG: getCurrentShift", self.currentTime, "and it returns:", self.parameters.getCurrentShift(self.currentTime))
        return self.parameters.getCurrentShift(self.currentTime)

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
        s += 'Entities_System,'
        s += 'Shift'
        # print(s)
        with open(self.parameters.output_file + '.csv', "w+") as output_file:
            output_file.write(s + '\n')

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
        s += str(self.entitiesSystem) + ','
        s += str(self.parameters.getCurrentShift(currentEvent.eventScheduled))
        # print(s)
        self.output_file.write(s + '\n')

    def stats(self):
        s = 'Max_Queue_Length'
        r = str(self.parking.getMaxQueueLength())
        s += ',Processors_Capacity_Used'
        r += ',' + str(round(100 * self.serviceProcessors /
                             (self.parameters.num_processors * Constants.SIMULATION_DURATION), 2))  # in %
        shift_type, shift_duration = self.parameters.getParameters()
        for idx in range(len(shift_type)):
            s += ',Shift_Type'
            r += ',' + shift_type[idx]
            s += ',Shift_Duration'
            r += ',' + str(shift_duration[idx])
            s += ',Shift_Capacity_Usage'
            r += ',' + str(round(100 * self.service_per_shift[idx] /
                                 (self.parameters.num_processors * self.shift_durations[idx] * 3600), 2))
        with open(self.parameters.output_file + '.stats.csv', "w+") as output_file:
            output_file.write(s + '\n')
            output_file.write(r + '\n')


def usage():
    print('Core.py [options]')
    print('Model: source -> queue -> parking -> processor(s) -> sink')
    print('Options:')
    print('-h, --help\t\t\t\tShows the program usage help.')
    print('-p, --processors=...\tSets the number of processors.')


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

    # DEBUG
    # Genome 0111000000000000001001010001
    duration_total = 999
    shift_duration = [1,             8,              1,                  1,                 2,                 1]
    shift_type = [Constants.ENTREGA, Constants.DUAL, Constants.RECOGIDA, Constants.ENTREGA, Constants.ENTREGA, Constants.ENTREGA]
    parameters.setParameters(shift_duration, shift_type, shift_factor)
    #

    while duration_total < int(Constants.SIMULATION_DURATION / 3600):
        in_shift_type = str(input('Enter shift type:'))
        if in_shift_type not in (Constants.ENTREGA, Constants.RECOGIDA, Constants.DUAL):
            print('Shift type not recognized. Shifts are:', Constants.ENTREGA, Constants.RECOGIDA, Constants.DUAL)
        else:
            in_shift_duration = int(input('Enter shift duration in hours:'))
            if duration_total + in_shift_duration <= int(Constants.SIMULATION_DURATION / 3600):
                duration_total += in_shift_duration
                shift_duration.append(in_shift_duration)
                shift_type.append(in_shift_type)
            else:
                print('Not enough time. Remaining time is:',
                      int(Constants.SIMULATION_DURATION / 3600) - duration_total, 'h.')
    parameters.setParameters(shift_duration, shift_type, shift_factor)
    print('    Parameters set.')

    # Start core
    core = Core()
    core.run()
