from src.Auxiliary import Auxiliary
from src.Constants import *


class _Parameters:
    _instance = None

    # Simulator parameters
    def __init__(self):
        # Type of Execution
        self.WITH_SHIFTS = True

        self.shift_duration = [5, 5, 2, 2]
        self.shift_type = [Constants.ENTREGA, Constants.ENTREGA, Constants.RECOGIDA, Constants.DUAL]
        self.shift_factor = 3600  # hours
        self.num_processors = Constants.DEFAULT_PROCESSORS
        self.output_file = Constants.OUTPUT_PATH + "trace"

    def setNumProcessors(self, num_processors):
        self.num_processors = num_processors

    def setParameters(self, shift_duration, shift_type, shift_factor):
        self.shift_duration = shift_duration
        self.shift_type = shift_type
        self.shift_factor = shift_factor

    def getParameters(self):
        return self.shift_type, self.shift_duration

    def getTotalTime(self, shift):
        if self.WITH_SHIFTS:
            duration = 0
            idx = 0
            for i in self.shift_type:
                if i == shift:
                    duration += self.shift_duration[idx]
                idx += 1
        else:
            duration = 0
            for i in self.shift_duration:
                duration += i
        return duration

    def getCurrentShift(self, currentTime):
        if self.WITH_SHIFTS:
            currentTime -= Constants.SIMULATION_INITIAL_TIME
            seconds_incremental = []
            accum = 0
            seconds_incremental.append(accum)
            for i in self.shift_duration:
                accum += i * self.shift_factor
                seconds_incremental.append(accum)
            aux = Auxiliary()
            index = aux.binarySearch(seconds_incremental, currentTime)
            index = min(index, len(self.shift_type) - 1)
            return self.shift_type[index]
        else:
            return '-'


def Parameters():
    if _Parameters._instance is None:
        _Parameters._instance = _Parameters()
    return _Parameters._instance
