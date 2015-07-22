import os
from global_values import OUTPUT_DIR, ALPHA, BETA


class CyclicData(object):
    '''
    CyclicData class is used to write the cycle values to files.
    There are six basic files that store cycle data:
    1. data_agent_exit.txt
    2. data_agent.txt
    3. data_agent_cycle.txt
    4. data_alliance.txt
    5. data_network.txt
    6. data_breakthrough.txt
    '''

    def __init__(self):
        '''
        Constructor
        '''

        # Initially sets the run number to 0. This value can be
        # changed by set_run method.
        self.run_number = 0

        # Initially sets the cycle number to 0. This value can be
        # changed by set_cycle method.
        self.cycle_number = 0

        # Deletes the files in output folder
        self.delete_files_in_output()

        # The file that stores alliance data per cycle.
        self.alliance_file = self.create_alliance_file()

        # The file that stores fixed agent data for each agent in the network.
        self.agent_file = self.create_agent_file()

        # The file that stores all data per cycle for each agent in
        # the network.
        self.agent_cycle_file = self.create_agent_cycle_file()

        # The file that stores agent exit cycle for all agents that
        # leave the network.
        self.agent_exit_file = self.create_agent_exit_file()

        # The file that stores all data per cycle for the network.
        self.network_file = self.create_network_file()

        # The file that stores agent breakthrough.
        self.agent_breakthrough_file = self.create_agent_breakthrough_file()

        # The file that stores alpha beta values
        self.create_alpha_beta_file()
        
    def set_run(self, run_number):
        '''
        Sets the current run_number
        '''
        self.run_number = run_number
    
    def set_cycle(self, cycle_number):
        '''
        Sets the current cycle_number
        '''
        self.cycle_number = cycle_number

    def create_alpha_beta_file(self):
        '''
        Creates a file which contain alpha and beta value
        alpha | beta
        '''
        data_file = self.open_file('alpha_beta_file')
        wrow = str(ALPHA)+','+ str(BETA)+ '\n'
        data_file.write(wrow)
        data_file.close()
        
    def create_alliance_file(self):
        '''
        Creates the file which stores alliance data in the form\
        run  |  cycle  |  agent1  |  agent2
        '''
        data_file = self.open_file('data_alliance')
        title = "run,cycle,agent_id1,agent_id2\n"
        data_file.write(title)
        return data_file

    def append_alliance(self, agent1, agent2):
        '''
        Appends alliance data in the form
        run  |  cycle  |  agent1  |  agent2
        Appends the alliance for agent1-agent2 and agent2-agent1.
        '''
        wrow = str(self.run_number)+','+ str(self.cycle_number)+','+ \
                    str(agent1) + ',' + str(agent2) + '\n'
        self.alliance_file.write(wrow)
        wrow = str(self.run_number)+','+ str(self.cycle_number)+','+ \
                    str(agent2) + ',' + str(agent1) + '\n'
        self.alliance_file.write(wrow)

    def create_agent_exit_file(self):
        '''
        Creates the file which stores agent exit cycle data in the form
        run  |  cycle  |  agent_id        
        '''
        data_file = self.open_file('data_agent_exit')
        title = "run,cycle,agent_id\n"
        data_file.write(title)
        return data_file
    
    def append_agent_exit(self, agent_id):
        '''
        Appends the agent exit cycle to the file in the form
        run  |  cycle  |  agent_id    
        '''
        wrow = str(self.run_number)+','+ str(self.cycle_number)+','+ \
                    str(agent_id) + '\n'
        self.agent_exit_file.write(wrow)
        
    def create_agent_file(self):
        '''
        Creates the file which stores agent data in the form
        run  |  cycle  |  agent_id  |  entry_cycle  |  sigma_m  |  sigma_k    
        '''
        data_file = self.open_file('data_agent')
        title = "run,cycle,agent_id,entry_cycle,sigma_m,sigma_k\n"
        data_file.write(title)
        return data_file
    
    def append_agent(self, agent_id, entry_cycle, sigma_m, sigma_k):
        '''
        Appends agent data in the form
        run  |  cycle  |  agent_id  |  entry_cycle  |  sigma_m  |  sigma_k  
        '''
        wrow = str(self.run_number)+','+ str(self.cycle_number)+','+ \
                str(agent_id) + ',' + str(entry_cycle) + ',' + \
                str(sigma_m) + ',' + str(sigma_k) + '\n'
        self.agent_file.write(wrow) 
        
    def create_agent_cycle_file(self):
        '''
        Creates the file which stores agent data in the form
        run  |  cycle  |  agent_id  |  map_market  |  map_tech  |  
        cum_knowledge  |  cycle_realized_learning
        '''
        data_file = self.open_file('data_agent_cycle')
        title = "run,cycle, agent_id, map_market, map_knowledge, cum_knowledge, cycle_realized_learning\n"
        data_file.write(title)
        return data_file
    
    def append_agent_cycle(self, agent_id, map_market, map_knowledge, capital, realized_learning):
        '''
        Appends agent data in the form\
        run  |  cycle  |  agent_id  |  map_market  |  map_tech    |\
        capital  |  cycle_realized_learning
        '''
        wrow = str(self.run_number)+','+ str(self.cycle_number)+','+ \
                str(agent_id) + ',' + str(map_market) + ',' + \
                str(map_knowledge) + ',' + \
                str(capital) + ',' + str(realized_learning) + '\n'
        self.agent_cycle_file.write(wrow) 

    def create_network_file(self):
        '''
        Creates the file which stores network data in the form\
        run  |  cycle  |  number_of_agents  |  network_total_knowledge  |  
        network_total_realized_learning  |  average_agent_capital  |  
        average_agent_realized_learning  |  min_agent_capital  |  
        max_agent_capital
        '''
        data_file = self.open_file('data_network')
        title = "run,cycle,number_of_agents,network_total_cum_knowledge,network_total_realized_learning,average_agent_cum_knowledge,average_agent_realized_learning,min_agent_cum_knowledge,max_agent_cum_knowledge\n"
        data_file.write(title)
        return data_file

    def append_network(self, number_of_agents, network_total_capital, network_total_realized_learning, \
                          average_agent_capital, average_agent_realized_learning, min_agent_capital, \
                          max_agent_capital):
        '''
        Appends network data in the form\
        run  |  cycle  |  number_of_agents  |  network_total_capital  |  
        network_total_realized_learning  |  average_agent_capital  |  
        average_agent_realized_learning  |  min_agent_capital  |  max_agent_capital
        '''
        wrow = str(self.run_number)+','+ str(self.cycle_number)+','+ \
               str(number_of_agents)+','+ str(network_total_capital) + \
               ',' + str(network_total_realized_learning) + ',' + \
                str(average_agent_capital) + ',' + \
                str(average_agent_realized_learning) + ',' + \
                str(min_agent_capital) + ',' + str(max_agent_capital) + '\n'
        self.network_file.write(wrow)

    def create_agent_breakthrough_file(self):
        '''
        Creates the file which stores breakthrough data in the form\
        run  |  cycle  |  agent_id  |  map_market  |  
        map_knowledge  |  new_map_market  |  new_map_knowledge
        '''
        data_file = self.open_file('data_breakthrough')
        title = "run,cycle,agent_id,map_market,map_knowledge,new_map_market,new_map_knowledge\n"
        data_file.write(title)
        return data_file

    def append_agent_breakthrough(self, agent_id, map_market, map_knowledge,  \
                                  new_map_market, new_map_knowledge):
        '''
        Appends breakthrough data in the form\
        run  |  cycle  |  agent_id  |  map_market  |  map_knowledge
        new_map_market  |  new_map_knowledge 
        '''
        wrow = str(self.run_number)+','+ str(self.cycle_number)+','+ \
               str(agent_id)+','+ str(map_market) + ',' + \
               str(map_knowledge) + ',' + str(new_map_market) + \
               ',' + str(new_map_knowledge) + '\n'
        self.agent_breakthrough_file.write(wrow)

    def open_file(self, file_name):
        '''
        Opens a file with the specified file_name in the OUTPUT_DIR directory
        '''
        output = OUTPUT_DIR + file_name + ".txt"
        return open(output, 'w')
    
    def close_all(self):
        '''
        Closes all the files.
        '''
        self.alliance_file.close()
        self.agent_file.close()
        self.agent_cycle_file.close()
        self.agent_exit_file.close()
        self.network_file.close()
        self.agent_breakthrough_file.close()

    def delete_files_in_output(self):
        """
        Delete files in the OUTPUT_DIR directory before each run.
        """
        if os.path.exists(OUTPUT_DIR):
            for file_i in os.listdir(OUTPUT_DIR):
                file_path = os.path.join(OUTPUT_DIR, file_i)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception, e:
                    print e
