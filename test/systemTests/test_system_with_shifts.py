import os
from unittest import TestCase

from src.Constants import Constants
from src.Core import Core
from src.Parameters import Parameters
from src.Random import Random
from test.DataBase import *


class TestSystemWithShifts(TestCase):
    INTEGER_ROWS = [0, 2, 3, 4, 5, 6, 7, 8, 9]
    STRING_ROWS = [1, 10]

    static_big_matrix = []
    cols = {}

    @classmethod
    def process_line(cls, line):
        row = line.split(',')
        row = [tmp.split('\n')[0] for tmp in row]
        for i in cls.INTEGER_ROWS:
            row[i] = int(row[i])
        for i in cls.STRING_ROWS:
            row[i] = str(row[i])
        return row

    @classmethod
    def setUpClass(cls):
        param = Parameters()
        param.num_processors = Constants.DEFAULT_PROCESSORS
        cls.coreObj = Core(param)
        cls.coreObj.output_file = open('./TEST_System.txt', "w+")
        cls.coreObj.parameters.output_file = "TEST_System"
        cls.coreObj.run()
        cls.coreObj.output_file.close()
        with open('../output/TEST_System.csv', "r") as read:
            header = read.readline().split(',')
            header = [tmp.split('\n')[0] for tmp in header]
            for i in range(len(header)):
                cls.cols[header[i]] = i
            line = read.readline()
            # [current_time, event_name, event_scheduled, event_time, idle_proc, service_proc, num_idle_proc, buff_len, queue_len, entities_system, shift]
            # Current_Time,Event_Name,Event_Scheduled,Event-Time,Idle_Processors,Service_Processors,Number_Idle_Processors,Buffer_Length,Queue_Length,Entities_System,Shift
            while line:
                row = TestSystemWithShifts.process_line(line)
                cls.static_big_matrix.append(row)
                line = read.readline()

    @classmethod
    def tearDownClass(cls):
        cls.coreObj = None
        os.remove("../output/TEST_System.csv")
        os.remove("../output/TEST_System.stats.csv")
        os.remove("./TEST_System.txt")

    def setUp(self):
        self.big_matrix = self.static_big_matrix.copy()

    def test_system_checks_start_end_simulation(self):
        first_row = self.big_matrix[:][0]
        last_row = self.big_matrix[:][-1]
        self.assertEquals(first_row[1], Constants.START_SIMULATION,
                          "The first row should be the beginning of the simulation")
        self.assertEquals(last_row[1], Constants.END_SIMULATION,
                          "The first row should be the end of the simulation")

    def test_probability_distribution_processors(self):
        processing_times = selection(self.cols['Event_Name'], lambda x: x == Constants.END_SERVICE, self.big_matrix)
        processing_times = transformCols([self.cols['Event_Scheduled'], self.cols['Event-Time']],
                                         self.cols['Current_Time'], lambda x, y: y - x, processing_times)
        processing_times = groupBy([self.cols['Shift']],
                                   [self.cols['Current_Time'], self.cols['Current_Time'], self.cols['Current_Time'],
                                    self.cols['Current_Time']], [countA, sumA, minA, maxA], processing_times, True)
        processing_times = transformCols([1, 2], 1, lambda x, y: y / x, processing_times)  # average
        processing_times = projection([0, 1, 3, 4], processing_times)
        self.assertEquals(len(processing_times), 3, "There should be 3 shifts")

        print(processing_times)

        shift3 = processing_times[0]
        self.assertGreaterEqual(shift3[2], Constants.MINIMUM_TIME_DUAL,
                                "The time should be greater or equal for DUAL")
        self.assertLessEqual(shift3[3], Constants.MAXIMUM_TIME_DUAL,
                             "The time should be less of equal for DUAL")
        mean = (Constants.MINIMUM_TIME_DUAL + Constants.MAXIMUM_TIME_DUAL) / 2
        self.assertTrue(abs(shift3[2] - mean) < 100, "The time should be almost equal for DUAL")

        shift1 = processing_times[1]
        self.assertGreaterEqual(shift1[2], Constants.MINIMUM_TIME_ENTREGA,
                                "The time should be greater or equal for ENTREGA")
        self.assertLessEqual(shift1[3], Constants.MAXIMUM_TIME_ENTREGA,
                             "The time should be less of equal for ENTREGA")
        mean = (Constants.MINIMUM_TIME_ENTREGA + Constants.MAXIMUM_TIME_ENTREGA) / 2
        self.assertTrue(abs(shift1[2] - mean) < 100, "The time should be almost equal for ENTREGA")

        shift2 = processing_times[2]
        self.assertGreaterEqual(shift2[2], Constants.MINIMUM_TIME_RECOGIDA,
                                "The time should be greater or equal for RECOLLIDA")
        self.assertLessEqual(shift2[3], Constants.MAXIMUM_TIME_RECOGIDA,
                             "The time should be less of equal for RECOLLIDA")
        mean = (Constants.MINIMUM_TIME_RECOGIDA + Constants.MAXIMUM_TIME_RECOGIDA) / 2
        self.assertTrue(abs(shift2[2] - mean) < 100, "The time should be almost equal for RECOLLIDA")

    def test_probability_distribution_source(self):
        processing_times = selection(self.cols['Event_Name'], lambda x: x == Constants.NEXT_ARRIVAL, self.big_matrix)
        processing_times = transformCols([self.cols['Event_Scheduled'], self.cols['Event-Time']],
                                         self.cols['Current_Time'], lambda x, y: y - x, processing_times)
        processing_times = groupBy([self.cols['Shift']],
                                   [self.cols['Current_Time'], self.cols['Current_Time'], self.cols['Current_Time'],
                                    self.cols['Current_Time']], [countA, sumA, minA, maxA], processing_times, True)
        processing_times = transformCols([1, 2], 1, lambda x, y: y / x, processing_times)  # average
        processing_times = projection([0, 1, 3, 4], processing_times)
        self.assertEquals(len(processing_times), 3, "There should be 3 shifts")

        print(processing_times)

        shift3 = processing_times[0]
        self.assertGreater(shift3[2], 0,
                           "The time should be greater or equal for DUAL")

        random = Random()
        self.assertTrue(abs(shift3[2] - random.LAMBDA_Dual) < 50, "The lambda should be almost equal for DUAL")

        shift1 = processing_times[1]
        self.assertGreater(shift1[2], 0,
                           "The time should be greater or equal for ENTREGA")

        random = Random()
        self.assertTrue(abs(shift1[2] - random.LAMBDA_Entrega) < 50, "The lambda should be almost equal for ENTREGA")

        shift2 = processing_times[2]
        self.assertGreater(shift2[2], 0,
                           "The time should be greater or equal for RECOLLIDA")
        random = Random()
        self.assertTrue(abs(shift2[2] - random.LAMBDA_Recogida) < 50, "The lambda should be almost equal for RECOLLIDA")
