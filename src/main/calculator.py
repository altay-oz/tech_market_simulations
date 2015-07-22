import math
from twisted.python.formmethod import InputError
from global_values import MIN_SIGMA, MAX_SIGMA, MAP_MARKET,MAP_TECH, BETA, MAX_TIP

class Calculator(object):
    '''
    Calculator class is a static class to make calculations of the network 
    alliances.
    '''
    
    @staticmethod
    def distance(distance, sigma):
        k = Calculator.parabola_distance(distance, sigma)
        if k < 0:
            k = 0.0
        return k

    @staticmethod
    def parabola_distance(distance, sigma):
        """ 
        The result of the parabola distribution function for given distance and
        sigma values.
        """
        if (distance < 0):
            raise(InputError("Error: Calculator.parabola_distance method cannot have negative distance."))
        if (sigma <= MIN_SIGMA) or (sigma >= MAX_SIGMA):
            raise(InputError("Error: Calculator.parabolo_distance method cannot have sigma out of range (MIN_SIGMA, MAX_SIGMA)."))
        return  ( BETA * (distance - sigma) - (distance - sigma)**2 )

    @staticmethod
    def normal_distance(distance, mu):
        """ 
        The result of the normal distribution function for given distance and
        mu values.
        """
        if (distance < 0):
            raise(InputError("Error: Calculator.normal_distance method cannot have negative distance."))
        if (mu <= MIN_SIGMA) or (mu >= MAX_SIGMA):
            raise(InputError("Error: Calculator.normal_distance method cannot have mu out of range \
                (MIN_SIGMA, MAX_SIGMA)."))
        std_dev = 1.0
        return  ( 1.0 / (std_dev * math.sqrt(2.0*math.pi))) * (math.exp((-1.0 / 2.0) * ((distance - mu) / std_dev)**2))


    @staticmethod
    def calculate_expected_learning(sigma_m, sigma_k, self_market, self_knowledge, \
                                  partner_market, partner_knowledge):
        '''
        Calculation of the expected learning using distance function on a torus.
        calculate_expected_learning is calculated by summing market distance
        and knowledge distance.
        '''
        if (sigma_m <= MIN_SIGMA) or (sigma_k <= MIN_SIGMA) or (sigma_m >= MAX_SIGMA) or (sigma_k >= MAX_SIGMA):
            raise InputError("Error: Calculator.calculate_expected_learning method cannot have sigma_m or \
                            sigma_k value out of range (MIN_SIGMA,MAX_SIGMA).")
        if (self_market < 0) or (self_market > MAP_MARKET) or (partner_market < 0) or (partner_market > MAP_MARKET) or \
            (self_knowledge < 0) or (self_knowledge > MAP_TECH) or (partner_knowledge < 0) or (partner_knowledge > MAP_TECH):
            raise InputError("Error: Calculator.calculate_expected_learning method cannot have self_market or \
                            partner_market out of range [0,MAP_MARKET] and self_knowledge or partner_knowledge \
                            out of range [0,MAP_TECH].")
        
        market_distance = Calculator.get_torus_distance(self_market, partner_market, MAP_MARKET)
        knowledge_distance = Calculator.get_torus_distance(self_knowledge,partner_knowledge, MAP_TECH)

        return Calculator.distance(market_distance, sigma_m) \
             + Calculator.distance(knowledge_distance, sigma_k)

    @staticmethod
    def calculate_next_position(self_value, partner_value, map_range, alpha, sigma):
        '''
        Calculates the next position for the first point depending on its distance
        from a second point within a given map range. The movement is assumed to be on 
        torus.
        Added the sigma value. alpha should be multiplied by r(d) / r(sigma)
        '''
        if (self_value < 0) or (self_value > map_range) or (partner_value < 0) or (partner_value > map_range):
            raise InputError("Error: Calculator.calculate_next_position method cannot have self_value \
                            or partner_value out of range [0,map_range].")
        if (map_range <= 0):
            raise InputError("Error: Calculator.calculate_next_position method cannot have non-positive map_range.")
        if (alpha <= 0):
            raise InputError("Error: Calculator.calculate_next_position method cannot have non-positive alpha.")
        next_value = 0.0
        distance = Calculator.get_torus_distance(self_value, partner_value, map_range) 
        
        half_range = map_range / 2.0
        difference = self_value - partner_value
        
        # this inverted u value is r(d) / r(sigma)
        dividend_u = MAX_TIP
        inverted_u = 0.0
        
        if dividend_u != 0:
            inverted_u = Calculator.distance(distance, sigma) / dividend_u
        
        if (difference > 0 and difference < half_range) or (difference < 0 and (abs(difference) > half_range)):
            next_value = self_value - (distance * alpha * inverted_u)
        else:
            next_value = self_value + (distance * alpha * inverted_u)
        if next_value < 0:
            next_value = next_value + map_range
        elif next_value > map_range:
            next_value = next_value - map_range
    
        return next_value
    
    @staticmethod
    def get_torus_distance(self_value, partner_value, map_range):
        '''
        Calculates the distance between two points on a torus in a given
        map range.
        '''
        if (map_range <= 0):
            raise InputError("Error: Calculator.get_torus_distance method cannot have non-positive map_range.")
        if (self_value < 0) or (self_value > map_range) or (partner_value < 0) or (partner_value > map_range):
            raise InputError("Error: Calculator.get_torus_distance method cannot have self_value \
                            or partner_value out of range [0,map_range].")
        distance = abs(self_value - partner_value)
        if distance > (map_range / 2.0):
            distance = map_range - distance
        return distance

    @staticmethod
    def is_in_torus_radius(self_x, partner_x, self_y, partner_y, radius, x_range, y_range):
        '''
        Returns 1 if the distance partner is within radius distance on torus from self;
        0 otherwise.
        '''
        if (self_x < 0) or (self_x > x_range) or (partner_x < 0) or (partner_x > x_range):
            raise InputError("Error : Calculator.is_in_radius method cannot have self_x or \
                        partner_x out of range [0, x_range]." + str(self_x) + " " + str(partner_x))
        if (self_y < 0) or (self_y > y_range) or (partner_y < 0) or (partner_y > y_range):
            raise InputError("Error : Calculator.is_in_radius method cannot have self_y or \
                        partner_y out of range [0, y_range]." + str(self_y) + " " + str(partner_y))
        if (radius < 0):
            raise InputError("Error : Calculator.is_in_radius method cannot have radius \
                             value less than 0.")
        distance = (Calculator.get_torus_distance(self_x, partner_x, x_range)) ** 2 + \
                   (Calculator.get_torus_distance(self_y, partner_y, y_range)) ** 2
        distance = math.sqrt(distance)
        return distance <= radius

    @staticmethod
    def is_in_radius(self_x, partner_x, self_y, partner_y, radius):
        '''
        Returns 1 if the distance partner is within radius distance from self;
        0 otherwise.
        '''
        if (self_x < 0) or (partner_x < 0) or (self_y < 0) or (partner_y < 0) or (radius < 0):
            raise InputError("Error : Calculator.is_in_radius method cannot have self_x,\
                         self_y, partner_x, partner_y, radius value less than 0.")
        distance = (partner_x - self_x) ** 2 + (partner_y - self_y) ** 2
        distance = math.sqrt(distance)
        return distance <= radius

    @staticmethod
    def get_difference_percentage(value1, value2):
        """
        Calculates and returns the difference percentage of value1 and
        value2.
        """
        if (value1 < 0) or (value2 < 0):
            raise InputError("Error: Calculator.get_learning_percentage cannot have negative input")
            
        higher_learning = max(value1, value2)
        learning_difference = abs(value1 - value2)
        percentage_difference = 0.0
        if higher_learning:
            percentage_difference = (learning_difference / higher_learning) * 100
        return percentage_difference
                    
    @staticmethod
    def init_matrix(size, value):
        """
        Create a fresh matrix with full of value given.
        """ 
        if (size < 0):
            raise IndexError("Error: Calculator.init_matrix cannot have negative size as input.")
        return [ [value] * size for i in range(size) ]

    @staticmethod
    def reset_row_column(index1, index2, matrix):
        '''
        Reset the values for given index rows and columns to 0 in the specified matrix.
        '''
        if (matrix == None):
            raise InputError("Error : Calculator.reset_row_column method cannot have None as matrix parameter.")
        length = len(matrix)
        try:
            column = len(matrix[0]) 
            if (column != length):
                raise InputError
        except:
            raise InputError("Error : Calculator.reset_row_column method accepts only square matrix as parameter.") 
        
        if (index1 < 0) or (index2 < 0) or (index1 >= length) or (index2 >= length):
            raise InputError("Error : Calculator.reset_row_column method cannot have index1 or index2 \
                    out of the bounds of matrix size.")
        matrix[index1] = [0] * length
        matrix[index2] = [0] * length
        
        for k in range(0, length):
            matrix[k][index1] = 0
            matrix[k][index2] = 0
