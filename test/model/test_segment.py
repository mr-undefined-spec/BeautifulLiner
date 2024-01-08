
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
        self.seg_2_4 = Segment(p2, p4)
    #end

    def test_init(self):
        self.assertEqual(self.seg_0_1.s.x, 0.0)
        self.assertEqual(self.seg_0_1.s.y, 0.0)
        self.assertEqual(self.seg_0_1.e.x, 1.0)
        self.assertEqual(self.seg_0_1.e.y, 1.0)
    #end

    def test_max_min(self):
        self.assertEqual(self.seg_0_1.maxX(), 1.0)
        self.assertEqual(self.seg_0_1.minX(), 0.0)
        self.assertEqual(self.seg_0_1.maxY(), 1.0)
        self.assertEqual(self.seg_0_1.minY(), 0.0)
    #end


    def test_intersection(self):
        inter_p_01_23 = self.seg_0_1.intersection(self.seg_2_3)
        self.assertAlmostEqual(inter_p_01_23.x, 0.5)
        self.assertAlmostEqual(inter_p_01_23.y, 0.5)

        inter_p_01_24 = self.seg_0_1.intersection(self.seg_2_4)
        self.assertEqual(inter_p_01_24, False)
    #end



#end

if __name__ == '__main__':
    unittest.main()
#end

