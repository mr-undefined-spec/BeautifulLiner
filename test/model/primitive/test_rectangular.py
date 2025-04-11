import unittest

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/primitive'))
from rectangular import Rectangular

class TestRectangular(unittest.TestCase):
    def setUp(self):
        self.rect = Rectangular(10.0, 20.0, 30.0, 40.0)
    #end

    def testInit(self):
        self.assertAlmostEqual(self.rect.q.x, 10.0)
        self.assertAlmostEqual(self.rect.q.y, 30.0)
        self.assertAlmostEqual(self.rect.m.x, 20.0)
        self.assertAlmostEqual(self.rect.m.y, 40.0)
    #end

    def testCollision(self):
        collided_rect = Rectangular(15.0, 25.0, 25.0, 35.0)
        self.assertEqual( self.rect.test_collision(collided_rect), True )

        not_collided_x_over_rect = Rectangular(25.0, 35.0, 25.0, 35.0)
        self.assertEqual( self.rect.test_collision(not_collided_x_over_rect), False )

        not_collided_y_over_rect = Rectangular(15.0, 25.0, 45.0, 55.0)
        self.assertEqual( self.rect.test_collision(not_collided_y_over_rect), False )

        not_collided_x_and_y_over_rect = Rectangular(25.0, 35.0, 45.0, 55.0)
        self.assertEqual( self.rect.test_collision(not_collided_y_over_rect), False )
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end
