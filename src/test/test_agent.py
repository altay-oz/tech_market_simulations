import unittest
import random
import sys
from twisted.python.formmethod import InputError

sys.path.append("../")

from main.agent import Agent
from main.sigma import Sigma


class TestAgent(unittest.TestCase):

    def setUp(self):
        '''
        For MAP = 20 on both dimensions.
        
        The expected sequence of generated random numbers with seed 20 is:
        random.seed(20)
        random.uniform(0, 20) = 18.112793523490414
                                   --> MAP_MARKET VALUE is assumed to be 20.
        random.uniform(0, 20) = 13.725083140534052
                                   --> MAP_TECH VALUE is assumed to be 20.
        random.uniform(0.0, 5.0) = 3.832546281813221
                                   --> MIN_CUM_KNOWLEDGE is assumed to be 0.0
                                   and MAX_CUM_KNOWLEDGE is assumed to be 5.0
        
        The expected sequence of generated random numbers with seed 30 is:
        random.seed(30)
        random.uniform(0, 20) = 10.781631292116211
                                --> MAP_MARKET VALUE is assumed to be 20.
        random.uniform(0, 20) = 5.7839288727944105
                                --> MAP_TECH VALUE is assumed to be 20.
        random.uniform(0.0, 5.0) = 0.15018454275563531
                                --> MIN_CUM_KNOWLEDGE is assumed to be 0.0
                                and MAX_CUM_KNOWLEDGE is assumed to be 5.0
        '''


        self.sigma = Sigma()
        # 20 is given as seed. 
        random.seed(20)
        self.agent1 = Agent(0, 0, self.sigma)
        # 30 is given as seed.
        random.seed(30)
        self.agent2 = Agent(1, 1, self.sigma)

                
    def tearDown(self):
        '''
        Releases the used sources for the tests.
        t        '''
        self.sigma = None
        self.agent1 = None
        self.agent2 = None

    def test_constructor(self):
        '''
        Tests the constructor of Agent class.
        '''
        # Tests the values for agent1 with seed 20.
        self.assertEqual(0, self.agent1.agent_id)
        self.assertEqual(0, self.agent1.entry_cycle)
        self.assertEqual(1, self.agent1.is_active)
        self.assertEqual(0.06790318043362997, self.agent1.sigma_m)
        self.assertEqual(1.3511240781010534, self.agent1.sigma_k)
        self.assertEqual(18.112793523490414, self.agent1.map_market)
        self.assertEqual(13.725083140534052, self.agent1.map_knowledge)
        self.assertEqual(3.832546281813221, self.agent1.cum_knowledge)
        self.assertEqual(0, self.agent1.cycle_realized_learning)
        self.assertEqual(0, self.agent1.next_map_market)
        self.assertEqual(0, self.agent1.next_map_knowledge)
        self.assertEqual(None, self.agent1.alliance)

        # Tests the values for agent2 with seed 30.
        self.assertEqual(1, self.agent2.agent_id)
        self.assertEqual(1, self.agent2.entry_cycle)
        self.assertEqual(1, self.agent2.is_active)
        self.assertEqual(0.09231151831518464, self.agent2.sigma_m)
        self.assertEqual(2.1445491468857547, self.agent2.sigma_k)
        self.assertEqual(10.781631292116211, self.agent2.map_market)
        self.assertEqual(5.7839288727944105, self.agent2.map_knowledge)
        self.assertEqual(0.15018454275563531, self.agent2.cum_knowledge)
        self.assertEqual(0, self.agent2.cycle_realized_learning)
        self.assertEqual(0, self.agent2.next_map_market)
        self.assertEqual(0, self.agent2.next_map_knowledge)
        self.assertEqual(None, self.agent2.alliance)

    def test_reset(self):
        '''
        Tests the reset method of the Agent class.
        '''
        self.agent1.make_alliance(self.agent2)
        self.agent1.cycle_realized_learning = 10
        self.agent1.next_map_market = 0.3
        self.agent1.next_map_knowledge = 0.5
        
        self.agent1.reset()
        
        self.assertEqual(0, self.agent1.cycle_realized_learning)
        self.assertEqual(0, self.agent1.next_map_market)
        self.assertEqual(0, self.agent1.next_map_knowledge)
        self.assertEqual(None, self.agent1.alliance)
    
    def test_exit(self):
        '''
        Tests the exit method of Agent class.
        '''
        self.agent1.exit()
        
        self.assertEqual(0, self.agent1.is_active)
        
    def test_in_learning_margin(self):
        '''
        Tests the in_learning_margin method of Agent class.
        '''
        pass # since learning margin = 0 always returns 1.

    def test_in_learning_margin_exception(self):
        '''
        Tests the in_learning_margin method of Agent class for invalid input.
        '''
        self.assertRaises(InputError, Agent.in_learning_margin, self.agent1, -5)
        
    def test_make_alliance(self):
        '''
        Tests the make_alliance method of Agent class.
        '''
        self.agent1.make_alliance(self.agent2)
        self.assertEqual(self.agent2, self.agent1.alliance)
        self.assertEqual(self.agent1, self.agent2.alliance)

    def test_make_alliance_exception(self):
        '''
        Tests the make_alliance method of Agent class for invalid input.
        '''
        self.assertRaises(InputError, Agent.make_alliance, self.agent1, \
                                                           None)
        self.assertRaises(InputError, Agent.make_alliance, self.agent1, \
                                                           self.agent1)
        
    def test_calculate_next_position(self):
        '''
        Tests the calculate_next_position method of Agent class.
        MAP = 20.0, BETA = 6.0 (MAX_TIP = 9.0), ALPHA = 0.2
        
        Agent_1 (map_market, map_knowledge) =
                (18.112793523490414, 13.725083140534052)
        Agent_2 (map_market, map_knowledge) =
                (10.781631292116211, 5.7839288727944105)
        '''
        
        self.agent1.calculate_next_position()
        self.assertEqual(0, self.agent1.next_map_market)
        self.assertEqual(0, self.agent1.next_map_knowledge)
        
        self.agent1.make_alliance(self.agent2)
        self.agent1.calculate_next_position()
        self.agent2.calculate_next_position()

        # learning of the agent_1 is null so no movement for it
        self.assertAlmostEqual(18.112793523490414, self.agent1.next_map_market)
        self.assertAlmostEqual(13.725083140534052, self.agent1.next_map_knowledge)

        # learning of the agent_2 in market dimension is null
        self.assertAlmostEqual(10.781631292116211, self.agent2.next_map_market)
        self.assertAlmostEqual(5.991987079, self.agent2.next_map_knowledge)

    def test_move_next_position(self):
        '''
        Tests the move_next_position method of Agent class.
        '''
        self.agent1.make_alliance(self.agent2)
        self.agent1.calculate_next_position()
        self.agent2.calculate_next_position()
        self.agent1.move_next_position()
        self.agent2.move_next_position()
            
        self.assertAlmostEqual(18.112793523490414, self.agent1.map_market)
        self.assertAlmostEqual(13.725083140534052, self.agent1.map_knowledge)

        self.assertAlmostEqual(10.781631292116211, self.agent2.map_market)
        self.assertAlmostEqual(5.991987079, self.agent2.map_knowledge)
        
if __name__ == "__main__":
    unittest.main()
