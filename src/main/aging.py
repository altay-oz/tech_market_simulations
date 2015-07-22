from numpy import *
from network import Network
from global_values import START_NUM_AGENT, NUMBER_OF_CYCLES, LAMBDA_POISSON

class Aging(object):
    '''
    classdocs
    '''

    def __init__(self, run_num, cyclic_data):
        '''
        Aging class manages network through cycles.
        '''
        # The network of this aging instance.
        self.network = Network(START_NUM_AGENT, cyclic_data)
        # The instance that stores the cycle values for a network for all cycles.
        # The array that keeps the number of agents to be added to the network for each cycle. 
        # The number of agents is determined randomly by poisson distribution.
        self.agent_entry_array = random.poisson(LAMBDA_POISSON, NUMBER_OF_CYCLES + 1)
        self.run_cycles(run_num, cyclic_data)
        
    def run_cycles(self, run_num, cyclic_data):
        for cycle in range(1, NUMBER_OF_CYCLES + 1):
            cyclic_data.set_cycle(cycle)
            self.network.plot_map(run_num, cycle - 1)
            print "============== cycle =", cycle,", run =", str(run_num),"=================\r\r"
            self.network.calculate_network()
#            self.network.manage_exit()
            number_entering_agents = self.agent_entry_array[cycle]
            self.network.manage_breakthrough(number_entering_agents)
#            print "POISSON = ", number_entering_agents
#            self.network.manage_entry(number_entering_agents, cycle)
            self.network.reset()
        self.network.plot_map(run_num, cycle)
            
        
