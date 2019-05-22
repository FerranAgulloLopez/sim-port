from src.Constants import *


class Parameters:
    # Simulator parameters
    shift_duration = [5, 5, 2, 1]
    shift_type = [Constants.ENTREGA, Constants.ENTREGA, Constants.RECOGIDA, Constants.DUAL]
    shift_factor = 3600  # hours

    def setParameters(self, shift_duration, shift_type, shift_factor):
        self.shift_duration = shift_duration
        self.shift_type = shift_type
        self.shift_factor = shift_factor

    def getTotalTime(self, shift):
        duration = 0
        idx = 0
        for i in self.shift_type:
            if i == shift:
                duration += self.shift_duration[idx]
            idx += 1
        return duration