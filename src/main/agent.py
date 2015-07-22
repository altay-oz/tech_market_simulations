import random
from twisted.python.formmethod import InputError
from calculator import Calculator
from global_values import MAP_MARKET, MAP_TECH, MAX_CUM_KNOW, MIN_CUM_KNOW,\
    LEARNING_MARGIN, ALPHA_TECH, ALPHA_MARKET

class Agent(object):
    '''
    Agent is the basic entity of the system. The aim of an agent is to 
    make alliances with an other agent and thereby increase its cum_knowledge. 
    Each agent measures its expected learning vis a vis to all the other 
    agents and chooses the most learningable agent to make alliance. 
    After the alliance is agreed, each side of the alliance moves 
    towards its partner.   
    '''


    def __init__(self, agent_id, entry_cycle, sigma):
        '''
        Constructor
        '''
        # Each agent has a unique id determined by the network it 
        # belongs to.
        self.agent_id = agent_id
        # Gets the next sigma_m, sigma_k value pair for this agent.
        value = sigma.get_sigma()
        # The coefficient that determines learningability depending on 
        # market distance. 
        self.sigma_m = value[0]
        # The coefficient that determines learningability depending on 
        # knowledge distance.
        self.sigma_k = value[1]
        # The cycle that this agent enters the network.
        self.entry_cycle = entry_cycle
        # The value that indicates if this agent is still active in the network or left the network.
        self.is_active = 1
        # The initial market position of the agent on the system map. 
        # It is determined randomly for each agent.
        self.map_market = random.uniform(0, MAP_MARKET)
        # The initial knowledge position of the agent on the system map.
        # It is determined randomly for each agent.
        self.map_knowledge = random.uniform(0, MAP_TECH)
        # Current cumulative knowledge of the agent. It is determined randomly at 
        # at the entry in the system and updated in each cycle depending 
        # on the alliance established.
        self.cum_knowledge = random.uniform(MIN_CUM_KNOW, MAX_CUM_KNOW)
        # Realized learning if there is an alliance during a cycle.
        self.cycle_realized_learning = 0.0  
        # The agent that this agent makes alliance.
        self.alliance = None
        # The next map_market position for this agent to be used when new network will be calculated. 
        self.next_map_market = 0.0
        # The next map_knowledge position for this agent to be used when new network will be calculated.
        self.next_map_tech = 0.0
        
    def reset(self):
        '''
        Resets the cycle_realised_learning for the agent to 0.0.
        '''
        self.cycle_realized_learning = 0.0
        self.alliance = None
        self.next_map_market = 0.0
        self.next_map_tech = 0.0

    def exit(self):
        '''
        Makes the agent leave the network. When an agent leaves 
        the network, the agent's is_active attribute is set to 0.
        '''
        self.is_active = 0

    def in_learning_margin(self, expected_learning):
        """ 
        Checks whether the expected learning is within the LEARNING_MARGIN of the
        agent's cumulative knowledge. Return 1 if in margin; 0 otherwise.
        """
        if (expected_learning < 0):
            raise InputError("Error : Agent.in_learning_margin method cannot have negative expected_learning \
                            as input.")
        if ((self.cum_knowledge * LEARNING_MARGIN) < expected_learning):
            return 1
        else:
            return 0 
    
    def make_alliance(self, partner):
        '''
        Sets the alliance to specified partner and calls partner.make_alliance(self). An agent cannot
        make alliance with None partner or itself.
        '''
        if (partner == None):
            raise InputError("Error : Agent.make_alliance method cannot have None partner as input.")
        if (partner == self):
            raise InputError("Error : Agent.make_alliance method cannot have itself as partner in input.")
        if (self.alliance != partner):
            self.alliance = partner
            partner.make_alliance(self)
            
            
    def calculate_next_position(self):
        """
        Calculate the agent's next position depending on the alliance decided.
        Changed after Muge, added sigma_m/sigma_k values.
        """
        if (self.alliance != None): # if there is a link
            self.next_map_market = Calculator.calculate_next_position(self.map_market, \
                                                                         self.alliance.map_market, \
                                                                         MAP_MARKET, \
                                                                         ALPHA_MARKET, 
                                                                         self.sigma_m)
            self.next_map_tech = Calculator.calculate_next_position(self.map_knowledge, \
                                                                         self.alliance.map_knowledge, \
                                                                         MAP_TECH, \
                                                                         ALPHA_TECH, 
                                                                         self.sigma_k)
            
    def move_next_position(self):
        '''
        Moves the agent to the calculated next position on the map if
        the next position is different then 0.0.
        '''
        if self.next_map_tech or self.next_map_market:
            self.map_knowledge = self.next_map_tech
            self.map_market = self.next_map_market 
            self.next_map_tech = 0.0
            self.next_map_market = 0.0
    
    def move_on_breakthrough(self):
        '''
        Randomly move the agent on the map, agent makes a breakthrough
        '''
        self.map_knowledge = random.uniform(0, MAP_TECH)
        self.map_market = random.uniform(0, MAP_MARKET)
        
    def print_agent_data(self):
        """ 
        Print all data of the agent, used for debugging.
        """
        print "coord  = ", self.map_knowledge, ";", self.map_market
        if self.alliance != None:
            print "alliance coord = ", self.alliance.map_knowledge, ";", self.alliance.map_market
        else:
            print "no alliance" 
        print "cumulative knowledge  = ", self.cum_knowledge
        print "cycle realized learning = ", self.cycle_realized_learning
        print "sigma m = ", self.sigma_m
        print "sigma k = ", self.sigma_k
        print "entry_cycle =", self.entry_cycle
        print "--------------------------\n"
