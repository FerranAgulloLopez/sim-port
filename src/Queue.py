class Queue:

    # CLASS FUNCTIONS

    def __init__(self, maxCapacity=0):
        self.maxCapacity = maxCapacity  # 0 = inf (default)
        self.inputModule = None
        self.entitiesList = []
        self.outputList = []
        self.maxQueueLength = 0 # Estadistico
        self.timeAtMaxCapacity = 0  # TODO: update (stat for capacity-limited queue)

    def addOutput(self, outputElement):
        self.outputList.append(outputElement)

    def removeOutput(self, outputIndex):
        self.outputList.pop(outputIndex)

    def addInput(self, inputModule):
        self.inputModule = inputModule

    def removeInput(self):
        self.inputModule = None

    def getQueueLength(self):
        return len(self.entitiesList)

    def getMaxQueueLength(self):
        return self.maxQueueLength

    def getTimeAtMaxCapacity(self):
        return self.timeAtMaxCapacity

    def nextArrival(self, entity):
        transferred = False
        if (self.maxCapacity == 0) or len(self.entitiesList) == 0:  # buffer or empty queue
            for output in self.outputList:
                if output.canHostEntity():
                    transferred = True
                    output.nextArrival(entity)
                    break
        if not transferred:
            self.entitiesList.append(entity)
            if len(self.entitiesList) > self.maxQueueLength:
                self.maxQueueLength = len(self.entitiesList)

            if self.maxCapacity != 0 and len(self.entitiesList) > self.maxCapacity:
                raise Exception("The queue cannot store the entity")

    def canHostEntity(self):
        return (self.maxCapacity == 0) or len(self.entitiesList) < self.maxCapacity

    def getEntity(self, outputModule):
        entity = self.entitiesList.pop(0)
        outputModule.nextArrival(entity)
        # if self.inputModule != None
        if self.inputModule and self.inputModule.getQueueLength() > 0 and self.canHostEntity():
            self.inputModule.getEntity(self)
