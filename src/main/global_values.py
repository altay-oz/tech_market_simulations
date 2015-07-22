# Number of runs
NUMBER_OF_RUNS = 5
# Number of cycles in each run
NUMBER_OF_CYCLES = 500
# Initial number of agents in the network at the beginning of each run.
START_NUM_AGENT = 100

########################################
# FOR TESTING
# IT IS IMPORTANT THAT
# ALPHA = 0.2, BETA = 6.0,  MAX_TIP = 9.0, MAP = 20.0 
# LOSS = 0, R = 0
########################################

# size of the torus
# MAP / 2 is the max length that two agent can be away from each other.
MAP = 20.0

# IPR regime [weak to strong] -> [0.0 ; 0.2]
ALPHA = 0.2
# coefficient of an agent movement on market axis
ALPHA_MARKET = ALPHA
# coefficient of an agent movement on technology axis
ALPHA_TECH = ALPHA

# knowledge type [tacit to codified] -> [2.0 ; 6.0]
BETA = 4.0

# beta=[2.0, 3.0, 4.0, 5.0, 6.0] and max_tip=[1.0, 2.25, 4.0, 6.25, 9.0]
if BETA == 2.0:
    MAX_TIP = 1.0
elif BETA == 3.0:
    MAX_TIP = 2.25
elif BETA == 4.0:
    MAX_TIP = 4.0
elif BETA == 5.0:
    MAX_TIP = 6.25
elif BETA == 6.0:
    MAX_TIP = 9.0

# the minimum value for an agent's cum. knowledge at the entry.
MIN_CUM_KNOW = 0.0
# the maximum value for an agent's cum. knowledge at the entry.
MAX_CUM_KNOW = 5.0

# coefficient for agents characteristics [exploiter to explorer]
MIN_SIGMA = 0.0
MAX_SIGMA = 3.0

# market value ranges between 0 and MAP_MARKET. It is shown on x-axis.
MAP_MARKET = MAP
# knowledge value ranges between 0 and MAP_TECH.It is shown on y-axis.
MAP_TECH = MAP

# coefficient for the entry.
LAMBDA_POISSON = 0.1

# percentage for the loss function, the expected learning is subtracted
# by LOSS percent.  
LOSS = 10.0
# perimeter in which the LOSS function is valid
R = 1.0

# for an alliance to be accepted both firms' expected learning
# difference should not be less than the ALLIANCE_MARGIN percent.
# 100 -> no limit to make any alliance
# 0 -> cannot make any alliance even if firms expected learnings are same.
ALLIANCE_MARGIN = 100.0
# for an alliance to be accepted the expected learning should not be
# less than the LEARNING_MARGIN percent of the accumulated knowledge
LEARNING_MARGIN = 0.0

# if any cumulative knowledge is less than EXIT_MARGIN % of the average
# system total learning then the firm is deleted.
# to be used if there is an entry.
EXIT_MARGIN = 0.0

# File names
CYCLE_MAP = 'cycle_map'

# The path of the directory where all generated files are saved.
OUTPUT_DIR = '../../output_alpha_'+str(ALPHA)+'_beta_'+str(BETA)+'/'
