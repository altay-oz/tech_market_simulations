'''
Created on Sep 15, 2012

@author: altay
'''
import unittest
from main.sigma import *
from numpy.lib.tests.test_format import assert_equal

import sys

sys.path.append("../")


class TestSigma(unittest.TestCase):


    def setUp(self):
        '''
        Initializes the necessary resources for the tests.
        '''
        self.sigma = Sigma()


    def tearDown(self):
        '''
        Releases the used sources for the tests.
        '''
        self.sigma = None


    def test_get_sigma(self):
        '''
        Tests the get_sigma method in the Sigma class for predefined array.
        '''
        # Check if the sigma instance returns the first value pair 
        # from the predefined sigma array.
        value = self.sigma.get_sigma()
        assert_equal(0.66241954208476006, value[0])
        assert_equal(0.66885000367117153, value[1])

        # Check if the sigma instance returns the second value pair 
        # from the predefined sigma array.
        value = self.sigma.get_sigma()
        assert_equal(0.60021257050283561, value[0])
        assert_equal(3.0323656162636006, value[1])
        
        # Check if the sigma instance returns the last value pair 
        # after being called 251 times.
        for i in range(1, 251):
            value = self.sigma.get_sigma()
        
        assert_equal(2.1725127255689838, value[0])
        assert_equal(1.6099687932924471, value[1])

        value = self.sigma.get_sigma()
        assert_equal(0.66241954208476006, value[0])
        assert_equal(0.66885000367117153, value[1])

    def test_reset(self):
        '''
        Tests the reset method in the class for predefined array.
        '''
        # Check if the sigma instance returns the first value pair 
        # from the predefined sigma array.
        value = self.sigma.get_sigma()
        assert_equal(0.66241954208476006, value[0])
        assert_equal(0.66885000367117153, value[1])

        # Check if the sigma instance returns the second value pair 
        # from the predefined sigma array.
        value = self.sigma.get_sigma()
        assert_equal(0.60021257050283561, value[0])
        assert_equal(3.0323656162636006, value[1])
        
        # Resets the sigma instance.
        self.sigma.reset()

        # Check if the sigma instance returns the first value pair 
        # from the predefined sigma array.
        value = self.sigma.get_sigma()
        assert_equal(0.66241954208476006, value[0])
        assert_equal(0.66885000367117153, value[1])

        
if __name__ == "__main__":
    unittest.main()
