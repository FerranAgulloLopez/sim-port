import numpy

from Event import Event


class Source:

    # CLASS ATTRIBUTES

    scheduler = None

    # CLASS FUNCTIONS

    def __init__(self, scheduler):
        self.scheduler = scheduler
        numpy.random.seed(0)

    def scheduleNextArrival(self):
        # TODO: parameter conversion
        # size = 0.3736072
        # mu = 3.0599529
        # prob = size / (size + mu)
        # variance = mu + mu**2 / size
        # successes = mu**2 / (variance - mu)
        # arrivalIncrement = numpy.random.negative_binomial(successes, prob)
        # TODO: DE DONDE SALEN ESTAS PROBABILIDADES???
        prob = 0.02450346
        arrivalIncrement = numpy.random.geometric(prob)
        arrivalEvent = Event(
            self.scheduler.NEXT_ARRIVAL,
            self.scheduler.currentTime,
            self.scheduler.currentTime + arrivalIncrement
        )
        return arrivalEvent
