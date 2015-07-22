import random
from global_values import MAX_SIGMA, MIN_SIGMA

class RandomSigma(object):
    '''
    RandomSigma class returns sigma_m and sigma_k values for agents. This 
    class generates random sigma_m and sigma_k values.
        
    sigma_m stands for the coefficient that determines learning
    depending on market distance. 
    
    sigma_k stands for the coefficient that determines learning
    depending on knowledge distance.
    
    (sigma_m, sigma_k) pairs are uniformly distributed in four regions.
    
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.region = 0
              
    def get_sigma(self):
        '''
        Returns sigma_m and sigma_t value pair. If the index grows
        larger than the number of pairs in the array, index is reset 
        to zero and get_sigma method continues to return pairs.
        '''
        '''
        sigma_m = 0
        sigma_t = 0
        mid_value = (MAX_SIGMA - MIN_SIGMA) / 2
        if self.region == 0:
            sigma_m = MIN_SIGMA + (mid_value * random.random())
            sigma_t = MIN_SIGMA + (mid_value * random.random())
        elif self.region == 1:
            sigma_m = MIN_SIGMA + (mid_value * random.random())
            sigma_t = MIN_SIGMA + mid_value + (mid_value * random.random())
        elif self.region == 2:
            sigma_m = MIN_SIGMA + mid_value + (mid_value * random.random()) 
            sigma_t = MIN_SIGMA + mid_value + (mid_value * random.random())
        elif self.region == 3:
            sigma_m = MIN_SIGMA + mid_value + (mid_value * random.random())
            sigma_t = MIN_SIGMA + (mid_value * random.random())
        '''
        sigma_m = random.random() * MAX_SIGMA
        sigma_t = random.random() * MAX_SIGMA
        value = (sigma_m, sigma_t) 
        print value, 'region ', self.region + 1
        self.region = (self.region + 1) % 4
        return value
    
    def reset(self):
        '''
        Resets the region index. After resetting get_sigma method returns 
        value pairs starting from 0th region.
        '''
        self.region = 0

