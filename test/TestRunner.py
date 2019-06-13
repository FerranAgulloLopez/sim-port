import unittest

from test.unitTests.test_auxiliary import TestAuxiliary
from test.unitTests.test_core import TestCore
from test.unitTests.test_event import TestEvent
from test.unitTests.test_parameters import TestParameters
from test.unitTests.test_processor import TestProcessor
from test.unitTests.test_queue import TestQueue
from test.unitTests.test_random import TestRandom
from test.integrationTests.test_integration_core_event import TestIntegrationCoreEvent
from test.integrationTests.test_integration_core_other_classes import TestIntegrationCoreOtherClasses
from test.integrationTests.test_integration_core_processor import TestIntegrationCoreProcessor
from test.integrationTests.test_integration_core_queue import TestIntegrationCoreQueue
from test.integrationTests.test_integration_core_source import TestIntegrationCoreSource
from test.systemTests.test_system_with_shifts import TestSystemWithShifts
from test.systemTests.test_system_without_shifts import TestSystemWithoutShifts


def suite_unit_tests():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestAuxiliary))
    test_suite.addTest(unittest.makeSuite(TestCore))
    test_suite.addTest(unittest.makeSuite(TestEvent))
    test_suite.addTest(unittest.makeSuite(TestParameters))
    test_suite.addTest(unittest.makeSuite(TestProcessor))
    test_suite.addTest(unittest.makeSuite(TestQueue))
    test_suite.addTest(unittest.makeSuite(TestRandom))
    return test_suite


def suite_integration_tests():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestIntegrationCoreEvent))
    test_suite.addTest(unittest.makeSuite(TestIntegrationCoreOtherClasses))
    test_suite.addTest(unittest.makeSuite(TestIntegrationCoreProcessor))
    test_suite.addTest(unittest.makeSuite(TestIntegrationCoreQueue))
    test_suite.addTest(unittest.makeSuite(TestIntegrationCoreSource))
    return test_suite


def suite_system_tests():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestSystemWithShifts))
    test_suite.addTest(unittest.makeSuite(TestSystemWithoutShifts))
    return test_suite


# MAIN FUNCTION
if __name__ == "__main__":
    in_tests_run = str(input('Enter which type of tests you want to run (a - All; u - Unit Tests; i - Integration '
                             'Tests; s - System Tests; x - Exit):'))

    def run_unit_tests():
        mySuit = suite_unit_tests()
        runner = unittest.TextTestRunner()
        runner.run(mySuit)
        print("All unit tests passed successfully!")

    def run_integration_tests():
        mySuit = suite_integration_tests()
        runner = unittest.TextTestRunner()
        runner.run(mySuit)
        print("All integration tests passed successfully!")

    def run_system_tests():
        mySuit = suite_system_tests()
        runner = unittest.TextTestRunner()
        runner.run(mySuit)
        print("All system tests passed successfully!")

    while in_tests_run != 'x':
        if in_tests_run == 'a':
            run_unit_tests()
            run_integration_tests()
            run_system_tests()
        elif in_tests_run == 'u':
            run_unit_tests()
        elif in_tests_run == 'i':
            run_integration_tests()
        elif in_tests_run == 's':
            run_system_tests()
        else:
            print("Command not recognized.")
        print()
        in_tests_run = str(
            input('Enter which type of tests you want to run (a - All; u - Unit Tests; i - Integration '
                  'Tests; s - System Tests; x - Exit):'))
