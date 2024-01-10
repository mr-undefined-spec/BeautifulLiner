
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))
from point import Point
from curve import Curve
import unittest

class TestCurve(unittest.TestCase):
    def setUp(self):
        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 2.0)
        p2 = Point(10.0, 20.0)
        p3 = Point(100.0, 200.0)

        self.curve = Curve(p0, p1, p2, p3)
    #end

    def test_init(self):
        self.assertEqual(self.curve.p0.x, 0.0)
        self.assertEqual(self.curve.p0.y, 0.0)
        self.assertEqual(self.curve.p1.x, 1.0)
        self.assertEqual(self.curve.p1.y, 2.0)
        self.assertEqual(self.curve.p2.x, 10.0)
        self.assertEqual(self.curve.p2.y, 20.0)
        self.assertEqual(self.curve.p3.x, 100.0)
        self.assertEqual(self.curve.p3.y, 200.0)
    #end

    def test_raise_error_with_set_p0_to_p3_as_int(self):
        p = Point(1.0, 2.1)

        with self.assertRaises(TypeError) as e:
            curve = Curve(0, p, p, p)
        #end with
        self.assertEqual(e.exception.args[0], 'p0 must be Point')

        with self.assertRaises(TypeError) as e:
            curve = Curve(p, 0, p, p)
        #end with
        self.assertEqual(e.exception.args[0], 'p1 must be Point')

        with self.assertRaises(TypeError) as e:
            curve = Curve(p, p, 0, p)
        #end with
        self.assertEqual(e.exception.args[0], 'p2 must be Point')

        with self.assertRaises(TypeError) as e:
            curve = Curve(p, p, p, 0)
        #end with
        self.assertEqual(e.exception.args[0], 'p3 must be Point')
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end
