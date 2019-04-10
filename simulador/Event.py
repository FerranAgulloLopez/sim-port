class Event:

    # CLASS ATTRIBUTES

    eventName = None
    eventScheduled = None
    eventTime = None

    # CLASS FUNCTIONS

    def __init__(self, eventName, eventScheduled, eventTime):
        self.eventName = eventName
        self.eventScheduled = eventScheduled
        self.eventTime = eventTime

    def __gt__(self, other):
        return self.eventTime > other.eventTime

    def __ge__(self, other):
        return self.eventTime >= other.eventTime
