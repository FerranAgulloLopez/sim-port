from queue import PriorityQueue

from Event import Event
from Server import Server
from Source import Source


class Scheduler:

    # CLASS CONSTANTS

    # Time constants (in seconds)
    SIMULATION_INITIAL_TIME = 6 * 60 * 60  # 6:00:00 h
    SIMULATION_DURATION = 20 * 60 * 60  # 20:00:00 h

    # Event names 
    START_SIMULATION = 'START_SIMULATION'
    NEXT_ARRIVAL = 'NEXT_ARRIVAL'
    END_SERVICE = 'END_SERVICE'
    END_SIMULATION = 'END_SIMULATION'

    # TODO:
    # MAX_QUEUE = 89  # no importa si fan cua dins o fora, es pot ignorar (?) confirmar
    # NUM_SERVERS = 12  # considerem totes les grues com un unic servidor (?) confirmar

    # CLASS ATTRIBUTES
    
    server = None
    source = None

    eventsList = PriorityQueue(0)  # maxsize = 0 = infinite
    previousTime = SIMULATION_INITIAL_TIME
    currentTime = SIMULATION_INITIAL_TIME
    idleServer = 0
    serviceServer = 0
    queueLength = 0
    entitiesSystem = 0

    # CLASS FUNCTIONS

    def __init__(self):
        self.server = Server(self)
        self.source = Source(self)
        startEvent = Event(
            self.START_SIMULATION,
            self.currentTime,
            self.currentTime
        )
        self.eventsList.put(startEvent, startEvent.eventTime)

    def run(self):
        self.logHeaders()
        while not self.eventsList.empty():
            currentEvent = self.eventsList.get()
            self.updateState(currentEvent)
            self.logEvent(currentEvent)
            if currentEvent.eventName == self.START_SIMULATION:
                self.startSimulation()
            elif currentEvent.eventName == self.NEXT_ARRIVAL:
                self.nextArrival()
            elif currentEvent.eventName == self.END_SERVICE:
                self.endService()
        endEvent = Event(
            self.END_SIMULATION,
            self.currentTime,
            self.currentTime
        )
        self.logEvent(endEvent)
        # self.logHeaders()  # DEBUG
        self.endSimulation()

    def logHeaders(self):
        print('Current_Time', end=',')
        print('Event_Name', end=',')
        print('Event_Scheduled', end=',')
        print('Event_Time', end=',')
        print('Idle_Server', end=',')
        print('Service_Server', end=',')
        print('Queue_Length', end=',')
        print('Entities_System')

    def logEvent(self, event):
        print(self.currentTime, end=',')
        print(event.eventName, end=',')
        print(event.eventScheduled, end=',')
        print(event.eventTime, end=',')
        print(self.idleServer, end=',')
        print(self.serviceServer, end=',')
        print(self.queueLength, end=',')
        print(self.entitiesSystem)

    def startSimulation(self):
        arrivalEvent = self.source.scheduleNextArrival()
        self.eventsList.put(arrivalEvent, arrivalEvent.eventTime)

    def updateState(self, event):
        self.previousTime = self.currentTime
        self.currentTime = event.eventTime
        timeStep = self.currentTime - self.previousTime
        if self.server.idle:
            self.idleServer += timeStep
        else:
            self.serviceServer += timeStep

    def nextArrival(self):
        self.entitiesSystem += 1
        if self.server.idle:
            endServiceEvent = self.server.scheduleEndService()
            self.eventsList.put(endServiceEvent, endServiceEvent.eventTime)
        else:
            self.queueLength += 1
        if self.currentTime < self.SIMULATION_DURATION:
            arrivalEvent = self.source.scheduleNextArrival()
            self.eventsList.put(arrivalEvent, arrivalEvent.eventTime)

    def endService(self):
        self.entitiesSystem -= 1
        if self.queueLength > 0:
            self.queueLength -= 1
            endServiceEvent = self.server.scheduleEndService()
            self.eventsList.put(endServiceEvent, endServiceEvent.eventTime)
        else:
            self.server.idle = True

    def endSimulation(self):
        # TODO: stats
        pass


# MAIN FUNCTION

if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()
