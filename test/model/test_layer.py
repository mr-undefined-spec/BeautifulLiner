
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))
from point import Point
from cubic_bezier_curve import CubicBezierCurve
from curve_set import CubicBezierCurveSet
from segment import Segment
from curve_set import SegmentSet
from layer import Layer
import unittest

class TestLayer(unittest.TestCase):
    def setUp(self):
        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 2.0)
        p2 = Point(10.0, 20.0)
        p3 = Point(100.0, 200.0)

        s01 = Segment(p0, p1)
        s23 = Segment(p2, p3)
        
        s_set = SegmentSet()
        s_set.append(s01)
        s_set.append(s23)

        self.s_layer = Layer()
        self.s_layer.append("s0", s_set)
        self.s_layer.append("s1", s_set)

        curve = CubicBezierCurve(p0, p1, p2, p3)
        
        c_set = CubicBezierCurveSet()
        c_set.append(curve)
        c_set.append(curve)

        self.c_layer = Layer()
        self.c_layer.append("c0", c_set)
        self.c_layer.append("c1", c_set)
    #end

    def test_init_segment_set(self):
        self.assertEqual(self.s_layer[0].path[0].s.x, 0.0)
        self.assertEqual(self.s_layer[0].path[0].s.y, 0.0)
        self.assertEqual(self.s_layer[0].path[0].e.x, 1.0)
        self.assertEqual(self.s_layer[0].path[0].e.y, 2.0)

        self.assertEqual(self.s_layer[0].path[1].s.x, 10.0)
        self.assertEqual(self.s_layer[0].path[1].s.y, 20.0)
        self.assertEqual(self.s_layer[0].path[1].e.x, 100.0)
        self.assertEqual(self.s_layer[0].path[1].e.y, 200.0)
    #end

    def test_init_cubic_bezier_curve_set(self):
        self.assertEqual(self.c_layer[0].path[0].p0.x, 0.0)
        self.assertEqual(self.c_layer[0].path[0].p0.y, 0.0)
        self.assertEqual(self.c_layer[0].path[0].p1.x, 1.0)
        self.assertEqual(self.c_layer[0].path[0].p1.y, 2.0)
        self.assertEqual(self.c_layer[0].path[0].p2.x, 10.0)
        self.assertEqual(self.c_layer[0].path[0].p2.y, 20.0)
        self.assertEqual(self.c_layer[0].path[0].p3.x, 100.0)
        self.assertEqual(self.c_layer[0].path[0].p3.y, 200.0)
    #end

    def test_append_segment_set(self):
        p4 = Point(11.0, 22.0)
        p5 = Point(111.0, 222.0)

        s45 = Segment(p4, p5)
        
        other_s_set = SegmentSet()
        other_s_set.append(s45)

        self.s_layer.append("s2", other_s_set)

        self.assertEqual(self.s_layer[2].path[0].s.x, 11.0)
        self.assertEqual(self.s_layer[2].path[0].s.y, 22.0)
        self.assertEqual(self.s_layer[2].path[0].e.x, 111.0)
        self.assertEqual(self.s_layer[2].path[0].e.y, 222.0)

        self.assertEqual(self.s_layer[0].name, "s0")
        self.assertEqual(self.s_layer[1].name, "s1")
        self.assertEqual(self.s_layer[2].name, "s2")
    #end

    def test_append_cubic_bezier_curve(self):
        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 2.0)
        p4 = Point(11.0, 22.0)
        p5 = Point(111.0, 222.0)

        curve = CubicBezierCurve(p0, p1, p4, p5)
        
        other_c_set = CubicBezierCurveSet()
        other_c_set.append(curve)

        self.c_layer.append("c2", other_c_set)
        self.assertEqual(self.c_layer[2].path[0].p2.x, 11.0)
        self.assertEqual(self.c_layer[2].path[0].p2.y, 22.0)
        self.assertEqual(self.c_layer[2].path[0].p3.x, 111.0)
        self.assertEqual(self.c_layer[2].path[0].p3.y, 222.0)

        self.assertEqual(self.c_layer[0].name, "c0")
        self.assertEqual(self.c_layer[1].name, "c1")
        self.assertEqual(self.c_layer[2].name, "c2")
    #end

    def test_iter_segment_set(self):
        s = ""
        for s_set in self.s_layer:
            for seg in s_set.path:
                s += str(seg)
            #end
        #end
        the_answer = "0.000,0.000\n1.000,2.000\n10.000,20.000\n100.000,200.000\n0.000,0.000\n1.000,2.000\n10.000,20.000\n100.000,200.000\n"
        self.assertEqual(s, the_answer)
    #end

    def test_iter_cubic_bezier_curve_set(self):
        s = ""
        for c_set in self.c_layer:
            for curve in c_set.path:
                s += str(curve)
            #end
        #end
        the_answer = "0.000,0.000\n1.000,2.000\n10.000,20.000\n100.000,200.000\n0.000,0.000\n1.000,2.000\n10.000,20.000\n100.000,200.000\n"
        the_answer += "0.000,0.000\n1.000,2.000\n10.000,20.000\n100.000,200.000\n0.000,0.000\n1.000,2.000\n10.000,20.000\n100.000,200.000\n"
        self.assertEqual(s, the_answer)
    #end


#end

if __name__ == '__main__':
    unittest.main()
#end

