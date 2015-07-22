import unittest
import random
import sys

sys.path.append("../")

from main.cyclic_data import CyclicData
from numpy.lib.tests.test_format import assert_equal
from main.network import Network


class TestCyclicData(unittest.TestCase):

    def setUp(self):
        random.seed(10)
        self.cyclic_data = CyclicData()

    def tearDown(self):
        self.cyclic_data = None

    def test_constructor(self):
        '''
        Tests the constructor of CyclicData class.
        '''
    
    def test_set_run(self):
        '''
        Tests the set_run method of CyclicData class.
        '''
        pass
        
    def test_set_cycle(self):
        '''
        Tests the set_cycle method of CyclicData class.
        '''
        pass
    
    def test_create_alliance_file(self):
        '''
        Tests the create_alliance_file method of CyclicData class.
        '''
        pass

    def test_append_alliance(self):
        '''
        Tests the append_alliance method of CyclicData class.
        '''
        pass

    def test_create_agent_file(self):
        '''
        Tests the create_agent_file method of CyclicData class.
        '''
        pass

    def test_append_agent(self):
        '''
        Tests the append_agent method of CyclicData class.
        '''
        pass

    def test_create_agent_cum_knowledge_file(self):
        '''
        Tests the create_agent_cum_knowledge_file method of CyclicData class.
        '''
        pass

    def test_append_agent_cum_knowledge(self):
        '''
        Tests the append_agent_cum_knowledge method of CyclicData class.
        '''
        pass

    def test_create_network_file(self):
        '''
        Tests the create_network_file method of CyclicData class.
        '''
        pass

    def test_append_network(self):
        '''
        Tests the append_network method of CyclicData class.
        '''
        pass

    def test_open_file(self):
        '''
        Tests the open_file method of CyclicData class.
        '''
        pass

    def test_close_all(self):
        '''
        Tests the close_all method of CyclicData class.
        '''
        pass

    def test_delete_files_in_output(self):
        '''
        Tests the delete_files_in_output method of CyclicData class.
        '''
        pass

if __name__ == "__main__":
    unittest.main()
