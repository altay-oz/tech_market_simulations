'''
Created on Sep 15, 2012

@author: hande
'''
import unittest
from main.plotter import Plotter
import sys

sys.path.append("../")



class TestPlotter(unittest.TestCase):


    def setUp(self):
        self.x_array = [1, 5, 3, 4, 7, 10]
        self.y_array = [0, 3, 8, 2, 5, 1]
        self.size_array = [1, 2, 3, 4, 5, 6]


    def tearDown(self):
        self.x_array = None
        self.y_array = None
        self.size_array = None


    def test_scatter(self):
        '''
        Tests the scatter method of the Plotter class.
        '''
        Plotter.scatter('Title', 'file_name', self.x_array, \
                        self.y_array, self.size_array, 'Xaxis', 'Yaxis', 10, 20, 1)


if __name__ == "__main__":
    unittest.main()
