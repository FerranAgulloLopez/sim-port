# from Core import Core

class Sink:

    # CLASS ATTRIBUTES

    core = None

    inputList = []

    # CLASS FUNCTIONS

    def __init__(self, core):
        self.core = core
    
    def addInput(self, inputElement):
        self.inputList.append(inputElement)
    
    def removeInput(self, inputIndex):
        self.inputList.pop(inputIndex)

    def startSimulation(self):
        """Implemented by all modules"""
        arrivalEvent = self.scheduleNextArrival()
        self.core.addEvent(arrivalEvent)

    def endSimulation(self):
        """Implemented by all modules"""
        pass
