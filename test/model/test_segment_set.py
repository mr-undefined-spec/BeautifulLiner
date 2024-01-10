
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))
from point import Point
from segment import Segment
from segment_set import SegmentSet
import unittest

class TestSegmentSet(unittest.TestCase):
    def setUp(self):
        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 2.0)
        p2 = Point(10.0, 20.0)
        p3 = Point(100.0, 200.0)

        s01 = Segment(p0, p1)
        s23 = Segment(p2, p3)
        
        self.s_set = SegmentSet()
        self.s_set.append(s01)
        self.s_set.append(s23)

    def test_init(self):
        self.assertEqual(self.s_set[0].s.x, 0.0)
        self.assertEqual(self.s_set[0].s.y, 0.0)
        self.assertEqual(self.s_set[0].e.x, 1.0)
        self.assertEqual(self.s_set[0].e.y, 2.0)

        self.assertEqual(self.s_set[1].s.x, 10.0)
        self.assertEqual(self.s_set[1].s.y, 20.0)
        self.assertEqual(self.s_set[1].e.x, 100.0)
        self.assertEqual(self.s_set[1].e.y, 200.0)
    #end

    def test_append(self):
        p4 = Point(11.0, 22.0)
        p5 = Point(111.0, 222.0)

        s45 = Segment(p4, p5)
        
        self.s_set.append(s45)
        self.assertEqual(self.s_set[2].s.x, 11.0)
        self.assertEqual(self.s_set[2].s.y, 22.0)
        self.assertEqual(self.s_set[2].e.x, 111.0)
        self.assertEqual(self.s_set[2].e.y, 222.0)
    #end

    def test_iter(self):
        s = ""
        for seg in self.s_set:
            s += str(seg)
        #end
        the_answer = "0.000,0.000\n1.000,2.000\n10.000,20.000\n100.000,200.000\n"
        self.assertEqual(s, the_answer)


    #end


#end

if __name__ == '__main__':
    unittest.main()
#end

