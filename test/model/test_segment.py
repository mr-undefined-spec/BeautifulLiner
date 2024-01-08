
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))
from point import Point
from segment import Segment
import unittest

class TestSegment(unittest.TestCase):
    def setUp(self):
        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 1.0)
        p2 = Point(1.0, 0.0)
        p3 = Point(0.0, 1.0)
        p4 = Point(2.0, 1.0)

        self.seg_0_1 = Segment(p0, p1)
        self.seg_2_3 = Segment(p2, p3)
    #end

    def test_init(self):
        self.assertEqual(self.seg_0_1.s.x, 0.0)
        self.assertEqual(self.seg_0_1.s.y, 0.0)
        self.assertEqual(self.seg_0_1.e.x, 1.0)
        self.assertEqual(self.seg_0_1.e.y, 1.0)
    #end


#end

if __name__ == '__main__':
    unittest.main()
#end

