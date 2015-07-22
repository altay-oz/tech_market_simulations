from random_sigma import RandomSigma
from agent import Agent
from plotter import Plotter
from calculator import Calculator
import random
from twisted.python.formmethod import InputError
from global_values import EXIT_MARGIN, MAP_MARKET, ALPHA_MARKET,\
    MAP_TECH, ALPHA_TECH, LOSS, ALLIANCE_MARGIN, CYCLE_MAP, R

class Network(object):
    '''
    Network class creates the specified number of agents in the network 
    and organizes their relationship. 
    '''

    def __init__(self, number_of_agents, cyclic_data):
        '''
        Constructor of the Network class. Initializes the network 
        with specified number of agents.
        '''
        cyclic_data.set_cycle(0)
        # sigma is used as a parameter to create an agent. Each created agent 
        # takes the sigma instance and gets its sigma_m and sigma_k values
        # from the next value pair in sigma.
        self.sigma = RandomSigma()
        # cyclic_data is used to write the necessary values to file
        self.cyclic_data = cyclic_data
        # The list of agents in the network. Both active and inactive agents
        # are contained in this array.
        self.agents = []
        # The array that stores the expected learning of each agent in
        # the network from every other agent in the network.
        self.expected_learning_matrix = []
        # The array that stores the expected learning with LOSS of
        # each agent in the network from every other agent in the
        # network. LOSS is applied to expected learnings depending on
        # the number of agents in a specified radius for foreseen in
        # the next position. This matrix is used to decide alliances.
        self.expected_learning_matrix_with_loss = []
        # The sum of cum_knowledge of all active agents in the network.
        self.total_cum_knowledge = 0.0
        # The average cum_knowledge of agents in the network
        self.average_agent_cum_knowledge = 0.0
        # Creates the network
        self.create_initial_network(number_of_agents)
    
    def create_initial_network(self, number_of_agents):
        '''
        Creates the initial network with specified number of agents with 
        cycle number 0 and random seed.
        After creating the agents calculates the network total cum_knowledge.
        Only to be called from the constructor.
        '''
        if (number_of_agents < 0) :
            raise InputError("Error : Network.create_initial_network method  \
                              cannot have number_of_agents less than 0.")
        for i in range(number_of_agents):
            agent = Agent(i, 0, self.sigma)
            self.agents.append(agent)
            self.cyclic_data.append_agent(agent.agent_id, agent.entry_cycle, \
                                          agent.sigma_m, agent.sigma_k)
            self.cyclic_data.append_agent_cycle(agent.agent_id, \
                                                agent.map_market, \
                                                agent.map_knowledge,
                                                agent.cum_knowledge, \
                                                agent.cycle_realized_learning)
            self.total_cum_knowledge += agent.cum_knowledge
        try :
            self.average_agent_cum_knowledge = self.total_cum_knowledge / number_of_agents
        except : 
            pass
        self.cyclic_data.append_network(number_of_agents, \
                                        self.total_cum_knowledge, 0, \
                                        self.average_agent_cum_knowledge, \
                                        0, 0, 0)
            
    def reset(self):
        '''
        Resets the network values to beginning values of a cycle.
        All agent values for active agents must also be reseted. 
        '''
        num_agent = len(self.agents)
        for agent_index in range(num_agent):
            agent = self.agents[agent_index]
            if (agent.is_active):
                agent.reset()
        self.average_agent_cum_knowledge = 0.0 
        self.expected_learning_matrix = []
        self.expected_learning_matrix_with_loss = []

    def calculate_network(self):
        '''
        Creates expected_learning_matrix, expected_learning_matrix_with_loss, 
        using expected_learning_matrix_with_loss establishes alliances. 
        Depending on alliances calculates the values of new network.
        '''
        self.create_evaluation_matrices()
        # Decides alliances depending on the expected_learning_matrix_with
        # loss. If loss is not to be considered can be changed with
        # expected_learning_matrix.
        self.make_network_alliances(self.expected_learning_matrix_with_loss)
        self.calculate_realized_learning()
        
    def create_evaluation_matrices(self):
        """ 
        Creates the expected_learning_matrix and 
        expected_learning_matrix_with_loss 
        to make evaluation for alliances.
        """
        num_agent = len(self.agents)
        # first, create an empty expected_learning_matrix
        self.expected_learning_matrix = Calculator.init_matrix(num_agent, 0)
        # first, create an empty expected_learning_matrix
        self.expected_learning_matrix_with_loss = Calculator.init_matrix(num_agent, 0)

        # start the calculation for the expected_learning_matrix
        for agent_index in range(num_agent):
            for partner_index in range(num_agent):
                if (agent_index != partner_index):
                    if (self.agents[agent_index].is_active) and (self.agents[partner_index].is_active):
                        agent = self.agents[agent_index]
                        partner = self.agents[partner_index]
                        self_map_market = agent.map_market
                        self_map_knowledge = agent.map_knowledge
            
                        partner_map_market = partner.map_market
                        partner_map_knowledge = partner.map_knowledge
                        # then, expected learning calculation btw two firms 
                        # are inserted into expected_learning_matrix
                        self.expected_learning_matrix[agent_index][partner_index] = \
                        Calculator.calculate_expected_learning(agent.sigma_m, \
                                                    agent.sigma_k, \
                                                    self_map_market, \
                                                    self_map_knowledge, \
                                                    partner_map_market, \
                                                    partner_map_knowledge)
                        # prepares to calculate expected learning with loss
                        next_map_market = Calculator.calculate_next_position(self_map_market, \
                                                    partner_map_market, \
                                                    MAP_MARKET, \
                                                    ALPHA_MARKET, \
                                                    agent.sigma_m)
                        next_map_knowledge = \
                        Calculator.calculate_next_position(self_map_knowledge,\
                                                partner_map_knowledge, \
                                                MAP_TECH, \
                                                ALPHA_TECH, agent.sigma_k)
                        
                        self.expected_learning_matrix_with_loss[agent_index][partner_index] = \
                            self.calculate_learning_after_loss( \
                                        next_map_market, \
                                        next_map_knowledge, \
                                        agent_index, partner_index, \
                                        self.expected_learning_matrix[agent_index][partner_index])
                
    def make_network_alliances(self, evaluation_matrix):
        """
        Evaluate the expected learning matrix to find reasonable partnerships
        based on the max learning found within the matrix.
        """
        num_agent = len(self.agents)
        # create a local copy of the expected learning matrix
        local_expected_learning_matrix = list(evaluation_matrix)
        # find the maximum expected learning within the local matrix
        max_sys_expected_learning = max(max(l) for l in \
                                      local_expected_learning_matrix)
        while max_sys_expected_learning:
            for agent_index in range(num_agent):
                for partner_index in range(num_agent):
                    if (agent_index != partner_index):
                        agent = self.agents[agent_index]
                        partner = self.agents[partner_index]
                        if (agent.is_active) and (partner.is_active):
                            # find the placement of the max value within the expected learning
                            if local_expected_learning_matrix[agent_index][partner_index] == max_sys_expected_learning:
                                self.try_alliance(agent_index, partner_index, local_expected_learning_matrix)
            max_sys_expected_learning = max(max(l) for l in local_expected_learning_matrix)

    def calculate_realized_learning(self):
        """
        Calculates the realized learning of agents after position change 
        in the network. 
        """
        num_agent = len(self.agents)
        num_active_agents = 0
        network_total_realized_learning = 0.0
        min_agent_cum_knowledge = 10000000.0
        max_agent_cum_knowledge = 0.0
        for agent_index in range(num_agent):
            agent = self.agents[agent_index]
            if (agent.is_active):
                num_active_agents += 1
                if (agent.alliance != None):
                    agent.cycle_realized_learning = self.calculate_learning_after_loss(agent.map_market, agent.map_knowledge,\
                                                                            agent_index, agent.alliance.agent_id, 
                                                                            self.expected_learning_matrix[agent_index][agent.alliance.agent_id])
                    agent.cum_knowledge += agent.cycle_realized_learning
                    network_total_realized_learning += agent.cycle_realized_learning
                    
                self.cyclic_data.append_agent_cycle(agent.agent_id, agent.map_market, agent.map_knowledge, \
                                              agent.cum_knowledge, agent.cycle_realized_learning)
                self.average_agent_cum_knowledge += agent.cum_knowledge
                min_agent_cum_knowledge = min(min_agent_cum_knowledge, agent.cum_knowledge)
                max_agent_cum_knowledge = max(max_agent_cum_knowledge, agent.cum_knowledge)
        
        # Adds realized learnings to network's total cum_knowledge
        self.total_cum_knowledge += network_total_realized_learning
        try:
            self.average_agent_cum_knowledge /= num_active_agents
        except ZeroDivisionError:
            self.average_agent_cum_knowledge = 0 
            
        average_agent_realized_learning = 0.0
        try:
            average_agent_realized_learning = network_total_realized_learning / num_active_agents
        except ZeroDivisionError:
            pass
         
        self.cyclic_data.append_network(num_active_agents, \
                                        self.total_cum_knowledge, \
                                        network_total_realized_learning, \
                                        self.average_agent_cum_knowledge, \
                                        average_agent_realized_learning, \
                                        min_agent_cum_knowledge, \
                                        max_agent_cum_knowledge)
        print 'number_of_agents', num_active_agents
        print 'network_total_cum_knowledge', self.total_cum_knowledge
        print 'cycle_total_realized_learning', network_total_realized_learning
        print 'avegare_agent_cum_knowledge', self.average_agent_cum_knowledge
        print 'average_agent_realized_learning', average_agent_realized_learning
        print 'min_agent_cum_knowledge', min_agent_cum_knowledge
        print 'max_agent_cum_knowledge', max_agent_cum_knowledge
    
    def manage_exit(self):
        """
        Removes agents which have cum_knowledge less than 
        network_average_firm_cum_knowledge * EXIT MARGIN % from network. 
        """
        num_agent = len(self.agents)
        for agent_index in range(num_agent):
            agent = self.agents[agent_index]
            if (agent.is_active):
                if (agent.cum_knowledge < (self.average_agent_cum_knowledge \
                                           * EXIT_MARGIN / 100)):
                    agent.exit()
                    self.cyclic_data.append_agent_exit(agent.agent_id)

    def manage_entry(self, num_entry, cycle_num):
        """
        Fires NUM_ENTRY number of new agents in the network.
        """
        num_agent = len(self.agents)
        for i in range(num_entry):
            agent = Agent(num_agent, cycle_num, self.sigma)
            self.agents.append(agent)
            self.cyclic_data.append_agent(agent.agent_id, agent.entry_cycle, \
                                          agent.sigma_m, agent.sigma_k)
            self.cyclic_data.append_agent_cycle(agent.agent_id, \
                                                agent.map_market, \
                                                agent.map_knowledge, \
                                                agent.cum_knowledge, \
                                                agent.cycle_realized_learning)
            num_agent += 1
            
    def manage_breakthrough(self, num_entry):
        """
        NUM_ENTRY number of agents change their place in the map
        """
        num_agent = len(self.agents)
        for i in range(num_entry):
            agent_id = random.randint(0, num_agent - 1)
            print "breakthrough---------------", agent_id
            agent = self.agents[agent_id]
            ex_map_knowledge = agent.map_knowledge
            ex_map_market = agent.map_market
            agent.move_on_breakthrough()
            self.cyclic_data.append_agent_breakthrough(agent.agent_id, \
                ex_map_market, ex_map_knowledge, agent.map_market, \
                agent.map_knowledge)
        
    def calculate_learning_after_loss(self, map_market, map_knowledge, \
                                      agent_index, partner_index, \
                                      expected_learning):
        '''
        Returns the expected learning with loss for the agent with 
        specified index for the specified market and knowledge values 
        on the map.
        '''
        num_agent = len(self.agents)
        possible_learning = expected_learning
        for i in range(num_agent):
            # Do not cause loss if the agent is the one that this
            # agent makes alliance
            if (i != agent_index) and (i != partner_index):
                neighbor = self.agents[i]
                if (neighbor.is_active):
                    neighbor_map_market = neighbor.map_market
                    neighbor_map_knowledge = neighbor.map_knowledge
                    
                    if (Calculator.is_in_torus_radius(map_market, \
                                                      neighbor_map_market, \
                                                      map_knowledge, \
                                                      neighbor_map_knowledge,\
                                                      R, MAP_MARKET, MAP_TECH)):
                        # apply loss to the expected learning
                        possible_learning -= possible_learning * LOSS / 100
        return possible_learning
    
    def try_alliance(self, agent_index, partner_index, learning_matrix):
        '''
        Tries to make alliance between the agents in the given 
        agent_index and partner_index in the network. If it can make 
        alliance, it sets all the values in row and column agent_index
        and in row and column partner_index of the learning_matrix to 0 
        so that these two agents are not used for alliance calculations 
        anymore. If the alliance can not be made, then only sets the 
        value in agant_index, partner_index to 0 so that max_value of 
        the system is re-determined.
        '''
        if self.can_make_alliance(agent_index, partner_index, learning_matrix):
            agent = self.agents[agent_index] 
            partner = self.agents[partner_index]
            agent.make_alliance(partner)
            self.cyclic_data.append_alliance(agent_index, partner_index)
            # when the alliance deal is OK
            # nullify the agent_index and partner_index values
            Calculator.reset_row_column(agent_index, partner_index, \
                                        learning_matrix)
            
            # After making alliance calculates the next point for partners
            agent.calculate_next_position()
            partner.calculate_next_position()
            # and then moves them to their new position on the map.
            agent.move_next_position()
            partner.move_next_position()

        else:
            # if the deal fail then nullify the max value to find the next one
            learning_matrix[agent_index][partner_index] = 0
            
    def can_make_alliance(self, agent_index, partner_index, learning_matrix):
        """
        Checks if the agent with agent_index and the agent with partner_index 
        in the network can make alliance depending on two conditions evaluated
        depending on the values in learning_matrix:
        1- expected learning difference of two agents should be less than the 
        ALLIANCE_MARGIN %.
        2- learning for each agent should be higher than LEARNING_MARGIN % of 
        their accumulated cum_knowledge.
        """
        agent_expected_learning = learning_matrix[agent_index][partner_index]
        partner_expected_learning = learning_matrix[partner_index][agent_index] 
        if (agent_expected_learning == 0 and partner_expected_learning == 0):
            return 0
        else :
            return ((Calculator.get_difference_percentage(agent_expected_learning, partner_expected_learning) <= ALLIANCE_MARGIN) and \
                (self.agents[agent_index].in_learning_margin(agent_expected_learning)) and \
                (self.agents[partner_index].in_learning_margin(partner_expected_learning)))
            
    def plot_map(self, run_num, cycle_num):
        '''
        Creates an image file that shows the positions of agents in market 
        and knowledge map. Market values are shown on x-axis and knowledge 
        values are shown on y-axis. The size of the circle that represents 
        the agent is determined by the value of its cum_knowledge.
        '''
        if (run_num < 0) or (cycle_num < 0):
            raise InputError("Error : Network.plot_map method cannot have negative run_num or \
                            cycle_num")
        map_market = []
        map_knowledge = []
        cum_knowledge = []
        num_agent = 0
        
        for agent_index in range(len(self.agents)):
            agent = self.agents[agent_index]
            if (agent.is_active):
                num_agent += 1
                map_market.append(agent.map_market)
                map_knowledge.append(agent.map_knowledge)
                cum_knowledge.append(agent.cum_knowledge)

        file_name = 'RUN' + str(run_num) + "_" + CYCLE_MAP
        
        # putting file names in order 
        if cycle_num < 10:
            file_name += "000"
        elif cycle_num >= 10 and cycle_num < 100:
            file_name += "00"
        elif cycle_num >= 100 and cycle_num < 1000:
            file_name += "0"
        file_name += '%d' % cycle_num
        fig_title = str(num_agent) + " Agents, Cycle " + str(cycle_num)

        if (cycle_num % 50 == 0) or (cycle_num == 249): 
            print_pdf = 1
        else:
            print_pdf = 0
        Plotter.scatter(fig_title, file_name, map_market, \
                          map_knowledge, cum_knowledge, 'Market', 'Knowledge', \
                          MAP_MARKET, MAP_TECH, print_pdf)

    
