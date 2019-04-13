class Event:

    # CLASS ATTRIBUTES

    eventName = None
    eventScheduled = None
    eventTime = None

    # CLASS FUNCTIONS

    def __init__(self, eventCreator, eventName, eventScheduled, eventTime):
        self.eventCreator = eventCreator
        self.eventName = eventName
        self.eventScheduled = eventScheduled
        self.eventTime = eventTime

    def executeEvent(self):
        """Implemented by all components"""
        self.eventCreator.executeEvent(self)

    def __gt__(self, other):
        return self.eventTime > other.eventTime

    def __ge__(self, other):
        return self.eventTime >= other.eventTime
