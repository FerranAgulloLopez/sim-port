from src.Constants import *


class Parameters:
    # Simulator parameters
    shift_duration = [5, 5, 2, 1]
    shift_type = [Constants.ENTREGA, Constants.ENTREGA, Constants.RECOGIDA, Constants.DUAL]
    shift_factor = 3600 # hours



    def getTotalTime(self, shift):
        if shift == "ENTEGES"