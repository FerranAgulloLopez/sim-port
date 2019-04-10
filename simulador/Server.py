import numpy

from Event import Event


class Server:

    # CLASS ATTRIBUTES

    scheduler = None
    
    idle = True

    # CLASS FUNCTIONS

    def __init__(self, scheduler):
        self.scheduler = scheduler
        numpy.random.seed(0)

    def scheduleEndService(self):
        self.idle = False
        # TODO: parameter conversion
        # size = 3.426632
        # mu = 1608.256647
        # prob = size / (size + mu)
        # variance = mu + mu**2 / size
        # successes = mu**2 / (variance - mu)
        # serviceIncrement = numpy.random.negative_binomial(successes, prob)
        # TODO: DE DONDE SALEN ESTAS PROBABILIDADES???
        prob = 0.03660948
        serviceIncrement = numpy.random.geometric(prob)
        endServiceEvent = Event(
            self.scheduler.END_SERVICE,
            self.scheduler.currentTime,
            self.scheduler.currentTime + serviceIncrement
        )
        return endServiceEvent
