import os
from aging import Aging
from global_values import START_NUM_AGENT, NUMBER_OF_RUNS, OUTPUT_DIR
from cyclic_data import CyclicData


if __name__ == "__main__":
    
    print '------------------',OUTPUT_DIR
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # stop the execution of the program 
    # if the number of agents is not even.
    if ((START_NUM_AGENT % 2) != 0):
        exit("Error: Choose even number of agents!")

    print "\n* ***************************************************\n*"
    print "*\n*                 STARTING                         *\n*"
    print "*\n****************************************************\n"

    cyclic_data = CyclicData()
    for i in range(1, NUMBER_OF_RUNS + 1):
        #print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n"
        print "$$$$$$$$$$$$$$$$  RUN NUMBER = ", i, "  $$$$$$$$$$$$$$$$$\n"
        #print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n"
        cyclic_data.set_run(i) 
        Aging(i, cyclic_data)
    cyclic_data.close_all()    
    print '\n *********************** the close_all *************************\n\n\n\n'


