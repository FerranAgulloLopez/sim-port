from queue import PriorityQueue


class Queue:

    # CLASS ATTRIBUTES

    core = None
    outputList = []
    queueLength = 0
    maxQueueLength = 0

    # CLASS FUNCTIONS

    def __init__(self, core):
        self.core = core

    def addOutput(self, outputElement):
        self.outputList.append(outputElement)

    def removeOutput(self, outputIndex):
        self.outputList.pop(outputIndex)

    def getQueueLength(self):
        return self.queueLength

    def getMaxQueueLength(self):
        return self.maxQueueLength

    def increaseQueueLength(self):
        self.queueLength += 1

    def decreaseQueueLength(self):
        self.queueLength -= 1

    def startSimulation(self):
        """Implemented by all modules"""
        pass

    def endSimulation(self):
        """Implemented by all modules"""
        pass
    
    def nextArrival(self):
        processed = False
        for processor in self.outputList:
            if processor.isIdle():
                processed = True
                processor.nextArrival()
                break
        if not processed:
            self.increaseQueueLength()
            if self.queueLength > self.maxQueueLength:
                self.maxQueueLength = self.queueLength
