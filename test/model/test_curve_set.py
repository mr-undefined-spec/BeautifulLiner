
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))
from point import Point
from curve import Curve
from curve_set import CurveSet
import unittest

class TestCurveSet(unittest.TestCase):
    def setUp(self):
        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 2.0)
        p2 = Point(10.0, 20.0)
        p3 = Point(100.0, 200.0)

        curve = Curve(p0, p1, p2, p3)
        
        self.c_set = CurveSet()
        self.c_set.append(curve)
        self.c_set.append(curve)

    def test_init(self):
        self.assertEqual(self.c_set[0].p0.x, 0.0)
        self.assertEqual(self.c_set[0].p0.y, 0.0)
        self.assertEqual(self.c_set[0].p1.x, 1.0)
        self.assertEqual(self.c_set[0].p1.y, 2.0)
        self.assertEqual(self.c_set[0].p2.x, 10.0)
        self.assertEqual(self.c_set[0].p2.y, 20.0)
        self.assertEqual(self.c_set[0].p3.x, 100.0)
        self.assertEqual(self.c_set[0].p3.y, 200.0)
    #end

    def test_append(self):
        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 2.0)
        p4 = Point(11.0, 22.0)
        p5 = Point(111.0, 222.0)

        curve = Curve(p0, p1, p4, p5)
        
        self.c_set.append(curve)
        self.assertEqual(self.c_set[2].p2.x, 11.0)
        self.assertEqual(self.c_set[2].p2.y, 22.0)
        self.assertEqual(self.c_set[2].p3.x, 111.0)
        self.assertEqual(self.c_set[2].p3.y, 222.0)
    #end

    def test_iter(self):
        s = ""
        for curve in self.c_set:
            s += str(curve)
        #end
        the_answer = "0.000,0.000\n1.000,2.000\n10.000,20.000\n100.000,200.000\n0.000,0.000\n1.000,2.000\n10.000,20.000\n100.000,200.000\n"
        self.assertEqual(s, the_answer)
    #end


#end

if __name__ == '__main__':
    unittest.main()
#end

