'''
Created on Sep 16, 2012

'''
import unittest
import sys
import os

sys.path.append("../")


from test_calculator import TestCalculator
from test_cyclic_data import TestCyclicData
from test_agent import TestAgent
from test_network import TestNetwork
from test_plotter import TestPlotter
#from test.test_sigma import TestSigma

if __name__ == '__main__':
    '''
    A test suite that runs all the tests in test directory.
    '''
    suiteAgent = unittest.TestLoader().loadTestsFromTestCase(TestAgent)
    suiteCalculator = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    suiteCyclicData = unittest.TestLoader().loadTestsFromTestCase(TestCyclicData)
    suiteNetwork = unittest.TestLoader().loadTestsFromTestCase(TestNetwork)
    suitePlotter = unittest.TestLoader().loadTestsFromTestCase(TestPlotter)
#    suiteSigma = unittest.TestLoader().loadTestsFromTestCase(TestSigma)
    allTests = unittest.TestSuite([suiteAgent, \
                                   suiteCalculator, \
                                   suiteCyclicData, \
                                   suiteNetwork, \
                                   suitePlotter])
#                                   suiteSigma])
    unittest.TextTestRunner(verbosity=2).run(allTests)
