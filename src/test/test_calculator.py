import unittest
from math import exp
from twisted.python.formmethod import InputError
import sys

sys.path.append("../")


from main.calculator import Calculator
from main.global_values import MAP_MARKET, MAP_TECH, \
     MIN_SIGMA, MAX_SIGMA, BETA

class TestCalculator(unittest.TestCase):
    '''
    TestCalculator is a TestCase to test Calculator class.
    '''

    def test_rayleigh_distance(self):
        '''
        Tests the rayleigh_distance method of Calculator class.
        '''
        self.assertAlmostEqual(5 * exp(-25.0 / 2.0), \
                               Calculator.rayleigh_distance(5.0, 1.0))

    def test_rayleigh_distance_exception(self):
        '''
        Tests the rayleigh_distance method of Calculator class for
        invalid input.
        '''
        # Tests for invalid distance values
        self.assertRaises(InputError, Calculator.rayleigh_distance, -1, 2)
        # Tests for invalid sigma values
        self.assertRaises(InputError, \
                          Calculator.rayleigh_distance, 1, MIN_SIGMA)
        self.assertRaises(InputError, \
                          Calculator.rayleigh_distance, 1, MIN_SIGMA - 1)
        self.assertRaises(InputError, \
                          Calculator.rayleigh_distance, 1, MAX_SIGMA)
        self.assertRaises(InputError, \
                          Calculator.rayleigh_distance, 1, MAX_SIGMA + 1)

    def test_parabola_distance(self):
        '''
        Tests the parabola_distance method of Calculator class.
        '''
        self.assertAlmostEqual(((BETA * 4.0) - 16), \
                               Calculator.parabola_distance(5.0, 1.0))

    def test_parabola_distance_exception(self):
        '''
        Tests the parabola_distance method of Calculator class for
        invalid input.
        '''
        # Tests for invalid distance values
        self.assertRaises(InputError, \
                          Calculator.parabola_distance, -1, 2)
        # Tests for invalid sigma values
        self.assertRaises(InputError, \
                          Calculator.parabola_distance, 1, MIN_SIGMA)
        self.assertRaises(InputError, \
                          Calculator.parabola_distance, 1, MIN_SIGMA - 1)
        self.assertRaises(InputError, \
                          Calculator.parabola_distance, 1, MAX_SIGMA)
        self.assertRaises(InputError, \
                          Calculator.parabola_distance, 1, MAX_SIGMA + 1)
        
    def test_calculate_expected_learning(self):
        '''
        Tests the calculate_expected_learning method of Calculator
        class using torus distance for calculating market and
        knowledge distance and parabola distance for distance between
        agents.
        '''
        # FOR  BETA = 6, MAP = 20
        self.assertAlmostEquals(0.0, \
          Calculator.calculate_expected_learning(2.0, 2.0, 1.0, 1.0, 1.0, 9.0))
        self.assertAlmostEquals(0.0, \
          Calculator.calculate_expected_learning(2.0, 2.0, 1.0, 1.0, 9.0, 1.0))

        # distances are the same for the following two examples
        # testing the torus shape for distance calculations.
        self.assertAlmostEquals(10.0, \
          Calculator.calculate_expected_learning(2.0, 2.0, 1.0, 1.0, 4.0, 4.0))
        self.assertAlmostEquals(10.0, \
          Calculator.calculate_expected_learning(2.0, 2.0, 1.0, 1.0, 18.0, 18.0))
        
    def test_calculate_expected_learning_exception(self):
        '''
        Tests the calculate_expected_learning method of Calculator
        class for invalid input.
        '''
        # Tests for invalid sigma_m values
        self.assertRaises(InputError, \
         Calculator.calculate_expected_learning, \
         MIN_SIGMA, 1, 2, 1, 10, 0.5)
        self.assertRaises(InputError, \
         Calculator.calculate_expected_learning, \
         MAX_SIGMA, 1, 2, 1, 10, 0.5)
        self.assertRaises(InputError, \
         Calculator.calculate_expected_learning, \
         MAX_SIGMA + 1, 1, 2, 1, 10, 0.5)
        # Tests for invalid sigma_k values
        self.assertRaises(InputError, \
         Calculator.calculate_expected_learning, \
         1, MIN_SIGMA, 1, 2, 10, 0.5)
        self.assertRaises(InputError, \
         Calculator.calculate_expected_learning, \
         1, MIN_SIGMA - 2 , 1, 2, 10, 0.5)
        self.assertRaises(InputError, \
         Calculator.calculate_expected_learning, \
         1, MAX_SIGMA, 1, 2, 1, 0.5)
        # Tests for invalid self_market values
        self.assertRaises(InputError, \
         Calculator.calculate_expected_learning, \
         1, 1.5, -1, 2, 10, 0.5)
        self.assertRaises(InputError, \
         Calculator.calculate_expected_learning, \
         1, 1.5, MAP_MARKET + 1, 2, 11, 0.5)
        # Tests for invalid self_knowledge values
        self.assertRaises(InputError, \
         Calculator.calculate_expected_learning, \
         1, 1.5, 1, -2, 10, 0.5)
        self.assertRaises(InputError, \
         Calculator.calculate_expected_learning, \
         1, 1.5, 1, MAP_TECH + 1, 11, 0.5)
        # Tests for invalid partner_market values
        self.assertRaises(InputError, \
         Calculator.calculate_expected_learning, \
         1, 1.5, 1, 2, -11, 0.5)
        self.assertRaises(InputError, \
         Calculator.calculate_expected_learning, \
         1, 1.5, 1, 2, MAP_MARKET + 1, 0.5)
        # Tests for invalid partner_knowledge values
        self.assertRaises(InputError, \
         Calculator.calculate_expected_learning, \
         1, 1.5, 1, 2, 1, -0.5)
        self.assertRaises(InputError, \
         Calculator.calculate_expected_learning, \
         1, 1.5, 1, 2, 3, MAP_TECH + 0.5)
        
    def test_calculate_next_position(self):
        '''
        Tests the calculate_next_position method of Calculator class.
        '''
        alpha = 0.05
        test_map = 20.0
        
        self.assertEqual(1, \
             Calculator.calculate_next_position(1.0, 9.0, \
                                                test_map, alpha, 2.0))

        self.assertAlmostEqual(1.08333, \
             Calculator.calculate_next_position(1.0, 4.0, \
                                                test_map, alpha, 2.0), \
                               places=5)

        # testing the torus points 2 and 19
        self.assertAlmostEqual(1.916666, \
              Calculator.calculate_next_position(2.0, 19.0, \
                                                 test_map, alpha, 2.0), \
                               places=5)
        
    def test_calculate_next_position_exception(self):
       '''
       Tests the calculate_next_position method of Calculator class
       for invalid inputs.
       '''
       # Tests for invalid values for agents on the map.
       alpha = 0.05
       test_map = 20.0
       sigma = 2
        
       self.assertRaises(InputError, \
                         Calculator.calculate_next_position, \
                         -3, 7, test_map, alpha, sigma)
       self.assertRaises(InputError, \
                         Calculator.calculate_next_position, \
                         3, -7, test_map, alpha, sigma)
       self.assertRaises(InputError, \
                         Calculator.calculate_next_position, \
                         21, 7, test_map, alpha, sigma)
       self.assertRaises(InputError, \
                         Calculator.calculate_next_position, \
                         3, 23, test_map, alpha, sigma)
     
    def test_get_torus_distance(self):
        '''
        Tests the get_torus_distance method of Calculator class.
        FOR MAP = 20
        '''
        self.assertEqual(3.0, Calculator.get_torus_distance(2.0, 5.0, 10.0))
        self.assertEqual(4.0, Calculator.get_torus_distance(8.0, 2.0, 10.0))
        self.assertEqual(5.0, Calculator.get_torus_distance(0.0, 5.0, 10.0))
        self.assertEqual(5.0, Calculator.get_torus_distance(1.0, 6.0, 10.0))
        self.assertEqual(0.0, Calculator.get_torus_distance(10.0, 10.0, 10.0))
        self.assertEqual(0, Calculator.get_torus_distance(10.0, 0.0, 10.0))
        
    def test_get_torus_distance_exception(self):
        '''
        Tests the get_torus_distance method of Calculator class for
        invalid input.
        '''
        # Tests for invalid self_value values
        self.assertRaises(InputError, Calculator.get_torus_distance, -1, 2, 5)
        self.assertRaises(InputError, Calculator.get_torus_distance, 6, 2, 5)
        # Tests for invalid partner_value values
        self.assertRaises(InputError, Calculator.get_torus_distance, 1, -2, 5)
        self.assertRaises(InputError, Calculator.get_torus_distance, 1, 7, 5)
        # Tests for invalid map_range values
        self.assertRaises(InputError, Calculator.get_torus_distance, 0, 0, 0)
        self.assertRaises(InputError, Calculator.get_torus_distance, 0, 0, -5)
    
    def test_is_in_torus_radius(self):
        '''
        Tests the is_in_radius method of the Calculator.
        '''
        # Tests the values also valid for 2D map.
        self.assertEqual(1, \
                         Calculator.is_in_torus_radius(2, 4, 5, 3, 4, 10, 10))
        self.assertEqual(0, \
                         Calculator.is_in_torus_radius(2, 4, 5, 3, 2, 10, 10))
        self.assertEqual(1, \
                         Calculator.is_in_torus_radius(2, 2, 0, 1, 1, 10, 10))
        self.assertEqual(0, \
                         Calculator.is_in_torus_radius(2, 2, 0, 1, 0, 10, 10))
        
        # Tests the values valid only on torus
        self.assertEqual(1, \
                      Calculator.is_in_torus_radius(1, 10, 1, 1, 2, 10, 10))
        self.assertEqual(1, \
                      Calculator.is_in_torus_radius(1, 10, 1, 10, 2, 10, 10))
        self.assertEqual(1, \
                      Calculator.is_in_torus_radius(0, 10, 10, 0, 2, 10, 10))
        self.assertEqual(1,
                      Calculator.is_in_torus_radius(3, 3, 10, 1, 2, 10, 10))

    def test_is_in_torus_radius_exception(self):
        '''
        Tests the is_in_torus_radius method of the Calculator class
        for invalid input.
        '''
        self.assertRaises(InputError, \
                          Calculator.is_in_torus_radius, -1, 3, 2, 2, 2, 4, 3)
        self.assertRaises(InputError, \
                          Calculator.is_in_torus_radius, 6, 3, 2, 2, 5, 3, 5)
        self.assertRaises(InputError, \
                          Calculator.is_in_torus_radius, 1, -3, 2, 2, 2, 4, 6)
        self.assertRaises(InputError, \
                          Calculator.is_in_torus_radius, 1, 3, -2, 2, 2, 5, 2)
        self.assertRaises(InputError, \
                          Calculator.is_in_torus_radius, 1, 3, 2, -2, 2, 6, 7)
        self.assertRaises(InputError, \
                          Calculator.is_in_torus_radius, 1, 3, 4, 2, 1, 4, 3)
        self.assertRaises(InputError, \
                          Calculator.is_in_torus_radius, 1, 3, 2, -1, 2, 5, 5)
        self.assertRaises(InputError, \
                          Calculator.is_in_torus_radius, 0, 3, 2, 7, 0, 6, 6)
        self.assertRaises(InputError, \
                          Calculator.is_in_torus_radius, 0, 7, 2, 2, -3, 6, 9)
        self.assertRaises(InputError, \
                          Calculator.is_in_torus_radius, 0, 7, 2, 2, 1, -6, 9)
        self.assertRaises(InputError, \
                          Calculator.is_in_torus_radius, 0, 7, 2, 2, 1, 6, -9)
            
    def test_is_in_radius(self):
        '''
        Tests the is_in_radius method of the Calculator class.
        '''
        self.assertEqual(1, Calculator.is_in_radius(2, 4, 5, 3, 4))
        self.assertEqual(0, Calculator.is_in_radius(2, 4, 5, 3, 2))
        self.assertEqual(1, Calculator.is_in_radius(2, 2, 0, 1, 1))
        self.assertEqual(0, Calculator.is_in_radius(2, 2, 0, 1, 0)) 
        
    def test_is_in_radius_exception(self):
        '''
        Tests the is_in_radius method of the Calculator class for
        invalid input.
        '''
        self.assertRaises(InputError, Calculator.is_in_radius, -1, 3, 2, 2, 1)
        self.assertRaises(InputError, Calculator.is_in_radius, 1, -3, 2, 2, 1)
        self.assertRaises(InputError, Calculator.is_in_radius, 1, 3, -2, 2, 1)
        self.assertRaises(InputError, Calculator.is_in_radius, 1, 3, 2, -2, 1)
        self.assertRaises(InputError, Calculator.is_in_radius, 1, 3, 2, 2, -1)


    def test_get_difference_percentage(self):
        '''
        Tests the get_difference_percentage method of the Calculator class.
        '''
        self.assertEqual(0.0, Calculator.get_difference_percentage(0.0, 0.0))
        self.assertEqual(50.0, Calculator.get_difference_percentage(1.0, 2.0))
        self.assertEqual(80.0, Calculator.get_difference_percentage(10.0, 2.0))

    def test_get_difference_percentage_exception(self):
        '''
        Tests the get_difference_percentage method of the Calculator
        class for invalid input.
        '''
        self.assertRaises(InputError, \
                          Calculator.get_difference_percentage, -1.0, 2.0)
        self.assertRaises(InputError, \
                          Calculator.get_difference_percentage, 1.0, -2.0)

    def test_init_matrix(self):
        '''
        Tests the init_matrix method of the Calculator class.
        '''
        matrix = Calculator.init_matrix(3, 1)
        self.assertEqual(1, matrix[0][0])
        self.assertEqual(1, matrix[0][1])
        self.assertEqual(1, matrix[0][2])
        self.assertEqual(1, matrix[1][0])
        self.assertEqual(1, matrix[1][1])
        self.assertEqual(1, matrix[1][2])
        self.assertEqual(1, matrix[2][0])
        self.assertEqual(1, matrix[2][1])
        self.assertEqual(1, matrix[2][2])
        
    def test_reset_row_column(self):
        '''
        Tests the reset_row_column method of the Calculator class.
        '''
        matrix = [[1, 2, 3, 6] , [2, 4, 5, 4], [5, 7, 9, 3], [6, 3, 9, 1]]
        Calculator.reset_row_column(0, 2, matrix)
        # Tests the row and column values for index1
        self.assertEqual(0, matrix[0][0])
        self.assertEqual(0, matrix[0][1])
        self.assertEqual(0, matrix[0][2])
        self.assertEqual(0, matrix[0][3])
        self.assertEqual(0, matrix[1][0])
        self.assertEqual(0, matrix[2][0])
        self.assertEqual(0, matrix[3][0])
        
        # Tests the row and column values for index2
        self.assertEqual(0, matrix[2][0])
        self.assertEqual(0, matrix[2][1])
        self.assertEqual(0, matrix[2][2])
        self.assertEqual(0, matrix[2][3])
        self.assertEqual(0, matrix[0][2])
        self.assertEqual(0, matrix[1][2])
        self.assertEqual(0, matrix[2][2])
        self.assertEqual(0, matrix[3][2])
        
    def test_reset_row_column_exception(self):
        '''
        Tests the reset_row_column method of the Calculator class for
        invalid input.
        '''
        self.assertRaises(InputError, \
                          Calculator.reset_row_column, 2, 3, None)
        self.assertRaises(InputError, \
                          Calculator.reset_row_column, 2, 1, [1, 2, 3])
        self.assertRaises(InputError, \
                          Calculator.reset_row_column, 0, 0, [[1, 2, 3]])
        self.assertRaises(InputError, \
                          Calculator.reset_row_column, 1, 4,\
                          [[1, 2, 3] , [2, 4, 5], [3, 5, 7]])
        self.assertRaises(InputError, \
                          Calculator.reset_row_column, 3, 0, \
                          [[1, 2, 3] , [2, 4, 5], [3, 5, 7]])
    
if __name__ == "__main__":
    unittest.main()
