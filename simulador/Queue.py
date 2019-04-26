# from Core import Core


class Queue:

    # CLASS ATTRIBUTES

    core = None

    outputList = []
    queueLength = 0

    # CLASS FUNCTIONS

    def __init__(self, core):
        self.core = core

    def addInput(self, inputElement):
        self.inputList.append(inputElement)

    def addOutput(self, outputElement):
        self.outputList.append(outputElement)

    def removeInput(self, inputIndex):
        self.inputList.pop(inputIndex)

    def removeOutput(self, outputIndex):
        self.outputList.pop(outputIndex)

    def getQueueLength(self):
        return self.queueLength

    def setQueueLength(self, length):
        self.queueLength = length

    def startSimulation(self):
        """Implemented by all modules"""

    def endSimulation(self):
        """Implemented by all modules"""
