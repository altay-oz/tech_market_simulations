import unittest
import random
import sys
from twisted.python.formmethod import InputError

sys.path.append("../")

from main.network import Network
from main.calculator import Calculator
from main.cyclic_data import CyclicData

class TestNetwork(unittest.TestCase):

    def setUp(self):
        '''
        Initializes the necessary resources for the tests.
        Works only if IS_SIGMA_RANDOM == 0 in global_values.py
        
        The expected sequence of generated random numbers with seed 10 is:
        random.seed(10)
        random.uniform(0,20)   ------- the map is 20 in each sides
        random.uniform(0,5) --- for the start of the cum_knonwledge

        the values of the agent 0 are:
        map_market =  11.4280518938
        map_knowledge =  8.5777810935
        cum_knowledge =  2.89045650567
        
        the values of the agent 1 are:
        map_market =  4.12196464279
        map_knowledge =  16.2664250271
        cum_knowledge =  4.11794436267
        
        the values of the agent 2 are:
        map_market =  13.069450678
        map_knowledge =  3.20459113038
        cum_knowledge =  2.6033467982
        
        the values of the agent 3 are:
        map_market =  6.55545623244
        map_knowledge =  4.99993353373
        cum_knowledge =  4.76408454573
        
        the values of the agent 4 are:
        map_market =  19.9311398508
        map_knowledge =  0.891127649009
        cum_knowledge =  4.30080518643
        
        the values of the agent 5 are:
        map_market =  12.0638122194
        map_knowledge =  7.63211971838
        cum_knowledge =  1.41809108953
        '''

        random.seed(10)
        self.cyclic_data = CyclicData()
        self.network = Network(6, self.cyclic_data)

        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        # for i in range(6):
        #     print 'Agent = ', i
        #     print 'market = ', self.network.agents[i].map_market
        #     print 'knowledge = ', self.network.agents[i].map_knowledge
        #     print 'cum_know = ', self.network.agents[i].cum_knowledge
        #     print '----------------'
                    
    def tearDown(self):
        self.network = None
        self.cyclic_data = None
        if os.path.exists(OUTPUT_DIR):
            os.removedirs(OUTPUT_DIR)

    def test_constructor(self):
        '''
        Tests the constructor of the Network class.
        '''
        self.assertEqual(0, self.network.cyclic_data.cycle_number)
        self.assertEqual(6, len(self.network.agents))
        self.assertNotEqual(None, self.network.sigma)
        self.assertEqual(20.094728488233791, self.network.total_cum_knowledge)
        self.assertEqual(3.3491214147056318, self.network.average_agent_cum_knowledge)
        self.assertEqual(0, len(self.network.expected_learning_matrix))
        self.assertEqual(0, len(self.network.expected_learning_matrix_with_loss))

        # the values of the agent 0 are:
        # map_market =  11.4280518938
        # map_knowledge =  8.5777810935
        # cum_knowledge =  2.89045650567

        self.assertAlmostEqual(11.4280518938, \
                               self.network.agents[0].map_market)
        self.assertAlmostEqual(8.5777810935, \
                         self.network.agents[0].map_knowledge)
        self.assertAlmostEqual(2.8904565056723519, \
                               self.network.agents[0].cum_knowledge)

        # the values of the agent 1 are:
        # map_market =  4.12196464279
        # map_knowledge =  16.2664250271
        # cum_knowledge =  4.11794436267

        self.assertAlmostEqual(4.12196464279, \
                               self.network.agents[1].map_market)
        self.assertAlmostEqual(16.2664250271, \
                               self.network.agents[1].map_knowledge)
        self.assertAlmostEqual(4.11794436267, \
                               self.network.agents[1].cum_knowledge)

        # the values of the agent 2 are:
        # map_market =  13.069450678
        # map_knowledge =  3.20459113038
        # cum_knowledge =  2.6033467982

        self.assertAlmostEqual(13.069450678, \
                               self.network.agents[2].map_market)
        self.assertAlmostEqual(3.20459113038, \
                               self.network.agents[2].map_knowledge)
        self.assertAlmostEqual(2.6033467982, \
                               self.network.agents[2].cum_knowledge)

        # the values of the agent 3 are:
        # map_market =  6.55545623244
        # map_knowledge =  4.99993353373
        # cum_knowledge =  4.76408454573

        self.assertAlmostEqual(6.55545623244, \
                               self.network.agents[3].map_market)
        self.assertAlmostEqual(4.99993353373, \
                               self.network.agents[3].map_knowledge)
        self.assertAlmostEqual(4.76408454573, \
                               self.network.agents[3].cum_knowledge)

        # the values of the agent 4 are:
        # map_market =  19.9311398508
        # map_knowledge =  0.891127649009
        # cum_knowledge =  4.30080518643

        self.assertAlmostEqual(19.9311398508, \
                               self.network.agents[4].map_market)
        self.assertAlmostEqual(0.891127649009, \
                               self.network.agents[4].map_knowledge)
        self.assertAlmostEqual(4.30080518643, \
                               self.network.agents[4].cum_knowledge)

        # the values of the agent 5 are:
        # map_market =  12.0638122194
        # map_knowledge =  7.63211971838
        # cum_knowledge =  1.41809108953

        self.assertAlmostEqual(12.0638122194, \
                               self.network.agents[5].map_market)
        self.assertAlmostEqual(7.63211971838, \
                               self.network.agents[5].map_knowledge)
        self.assertAlmostEqual(1.41809108953, \
                               self.network.agents[5].cum_knowledge)
        
        self.assertAlmostEqual(20.094728488233791, self.network.total_cum_knowledge)

    def test_reset(self):
        '''
        Tests the reset method of the Network class.
        '''
        self.network.cyclic_data.set_cycle(5)
        self.network.agents[1].exit()
        self.network.reset()

        self.assertEqual(0, self.network.average_agent_cum_knowledge)
        self.assertEqual(0, len(self.network.expected_learning_matrix))
        self.assertEqual(0, len(self.network.expected_learning_matrix_with_loss))
        self.assertEqual(5, self.network.cyclic_data.cycle_number)
        self.assertEqual(6, len(self.network.agents))
        self.assertNotEqual(None, self.network.sigma)
        self.assertEqual(20.094728488233791, self.network.total_cum_knowledge)
        
        self.assertEqual(0.0, self.network.agents[0].cycle_realized_learning)
        self.assertEqual(None, self.network.agents[0].alliance)
        self.assertEqual(0.0, self.network.agents[0].next_map_market)
        self.assertEqual(0.0, self.network.agents[0].next_map_knowledge)
        
        self.assertEqual(0.0, self.network.agents[5].cycle_realized_learning)
        self.assertEqual(None, self.network.agents[5].alliance)
        self.assertEqual(0.0, self.network.agents[5].next_map_market)
        self.assertEqual(0.0, self.network.agents[5].next_map_knowledge)
        
        self.assertAlmostEqual(4.12196464279, \
                               self.network.agents[1].map_market)
        self.assertAlmostEqual(16.2664250271, \
                               self.network.agents[1].map_knowledge)
            
    def test_create_expected_learning_matrix(self):
        '''
        Tests the create_evaluation_matrices method of the Network class.
        '''

        # agent 2 is exit so every expected learning calculations
        # related to agent 2 should be 0
        self.network.agents[2].exit()

        self.network.create_evaluation_matrices()
        
        # The expected learning of agent2 from any other agent must be
        # 0 since agent2 is not active.
        self.assertAlmostEqual(0, \
                               self.network.expected_learning_matrix[0][2])
        self.assertAlmostEqual(0, \
                               self.network.expected_learning_matrix[1][2])
        self.assertAlmostEqual(0, \
                               self.network.expected_learning_matrix[3][2])
        self.assertAlmostEqual(0, \
                               self.network.expected_learning_matrix[4][2])
        self.assertAlmostEqual(0, \
                               self.network.expected_learning_matrix[5][2])

        
        # The expected learning of agent0 from agent0 must be 0.
        self.assertEqual(0, self.network.expected_learning_matrix[0][0]) 
        self.assertEqual(0, self.network.expected_learning_matrix[1][1])
        self.assertEqual(0, self.network.expected_learning_matrix[2][2]) 
        self.assertEqual(0, self.network.expected_learning_matrix[3][3])
        self.assertEqual(0, self.network.expected_learning_matrix[4][4]) 
        self.assertEqual(0, self.network.expected_learning_matrix[5][5])
        
        
        # Test expected_learning for agent0
        self.assertAlmostEqual(0, \
                               self.network.expected_learning_matrix[0][1])
        self.assertAlmostEqual(14.1451284754856, \
                               self.network.expected_learning_matrix[0][3])
        self.assertAlmostEqual(0, \
                               self.network.expected_learning_matrix[0][4])
        self.assertAlmostEqual(3.08468113368173, \
                               self.network.expected_learning_matrix[0][5])

        # Test expected_learning for agent 1
        self.assertAlmostEqual(2.52758171621341, \
                               self.network.expected_learning_matrix[1][0])
        self.assertAlmostEqual(8.5659563015936, \
                               self.network.expected_learning_matrix[1][3])
        self.assertAlmostEqual(16.5230281780298, \
                               self.network.expected_learning_matrix[1][4])
        self.assertAlmostEqual(0, \
                               self.network.expected_learning_matrix[1][5])

        # Test expected_learning for agent 2 should be zero because
        # agent 2 is exit
        
        self.assertAlmostEqual(0, \
                              self.network.expected_learning_matrix[2][0])
        self.assertAlmostEqual(0, \
                              self.network.expected_learning_matrix[2][1])
        self.assertAlmostEqual(0, \
                              self.network.expected_learning_matrix[2][3])
        self.assertAlmostEqual(0, \
                              self.network.expected_learning_matrix[2][4])
        self.assertAlmostEqual(0, \
                              self.network.expected_learning_matrix[2][5])

        # Test expected_learning for agent 3
        self.assertAlmostEqual(17.7139840641858, \
                               self.network.expected_learning_matrix[3][0])
        self.assertAlmostEqual(0.956444371563587, \
                               self.network.expected_learning_matrix[3][1])
        self.assertAlmostEqual(16.1349628236964, \
                               self.network.expected_learning_matrix[3][4])
        self.assertAlmostEqual(16.2426173253092, \
                               self.network.expected_learning_matrix[3][5])

        # Test expected_learning for agent 4
        self.assertAlmostEqual(0, \
                               self.network.expected_learning_matrix[4][0])
        self.assertAlmostEqual(16.7010192277332, \
                               self.network.expected_learning_matrix[4][1])
        self.assertAlmostEqual(11.8150724425493, \
                               self.network.expected_learning_matrix[4][3])
        self.assertAlmostEqual(0, \
                               self.network.expected_learning_matrix[4][5])

        # Test expected_learning for agent 5
        self.assertAlmostEqual(0.905351406607448, \
                               self.network.expected_learning_matrix[5][0])
        self.assertAlmostEqual(0, \
                               self.network.expected_learning_matrix[5][1])
        self.assertAlmostEqual(5.44885016295865, \
                               self.network.expected_learning_matrix[5][3])
        self.assertAlmostEqual(7.55144184619663, \
                               self.network.expected_learning_matrix[5][4])



        ####
        # Tests the expected learning after loss of agent0 from agent5 at radius R.
        # self.assertEqual(1.4688863524797151, self.network.expected_learning_matrix_with_loss[0][5])

    def test_calculate_learning_after_loss(self):
        '''
        Tests the calculate_learning_after_loss method of the Network class.
        '''
        # num_agent = len(self.network.agents)
        # self.network.create_evaluation_matrices()
        # self.network.expected_learning_matrix_with_loss = Calculator.init_matrix(num_agent, 0)
        # self.assertEqual(1.4688863524797151, self.network.calculate_learning_after_loss(5.7299199550382705, 4.2652490123731477, 0, 5, 1.4688863524797151))
        # Test with R = 2
        #self.assertAlmostEqual(1.4688863524797151, self.network.calculate_learning_after_loss(5.7299199550382705, 4.2652490123731477, 0, 5, 1.4688863524797151))
    
    def test_evaluate_alliances(self):
        '''
        Tests the evaluate_alliances method of the Network class.
        '''
        pass
    
    def test_try_alliance(self):
        '''
        Tests the try_alliance method of the Network class.
        '''
        pass
    
    def test_can_make_alliance(self):
        '''
        Tests the can_make_alliance method of the Network class.
        '''
        pass
    
    def test_calculate_realized_learning(self):
        '''
        Tests the calculate_realized_learning method of the Network class.
        '''
        pass
    
    def test_manage_exit(self):
        '''
        Tests the manage_exit method of the Network class.
        '''
    
    def test_plot_map(self):
        '''
        Tests the plot_map method of the Network class.
        '''
        self.network.plot_map(0, 0)

    def test_plot_map_exception(self):
        '''
        Tests the plot_map method of the Network class for invalid input.
        '''
        self.assertRaises(InputError, Network.plot_map, self.network, -1, 0)
        self.assertRaises(InputError, Network.plot_map, self.network, 1, -2)

if __name__ == "__main__":
    unittest.main()
