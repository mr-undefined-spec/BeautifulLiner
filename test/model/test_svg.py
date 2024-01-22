
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))
from svg import Svg

from point import Point
from cubic_bezier_curve import CubicBezierCurve
from curve_set import CubicBezierCurveSet
from segment import Segment
from curve_set import SegmentSet
from layer import Layer

import unittest

class TestSvgData(unittest.TestCase):
    def setUp(self):
        self.svg = Svg()

        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 2.0)
        p2 = Point(10.0, 20.0)
        p3 = Point(100.0, 200.0)

        s01 = Segment(p0, p1)
        s23 = Segment(p2, p3)
        
        curve = CubicBezierCurve(p0, p1, p2, p3)
        
        c_set = CubicBezierCurveSet()
        c_set.append(curve)
        c_set.append(curve)

        c_layer = Layer()
        c_layer.append("c0", c_set)
        c_layer.append("c1", c_set)

        self.svg.append(c_layer)
        self.svg.append(c_layer)
    #end

    def test_read(self):
        svg_from_file = Svg()
        svg_from_file.read("data/test.svg")

        for group_paths_set in svg_from_file.get_group_paths_tuple():
            group = group_paths_set[0]
            paths = group_paths_set[1]
            self.assertEqual(group.getAttributeNode('id').nodeValue, 'senga')
            self.assertEqual(paths[0].getAttributeNode('d').nodeValue, 'M532.031 499.344L531.844 499.438C532.649 500.227 533.803 501.251 534.688 502.094C533.871 501.215 532.761 500.17 532.031 499.344ZM534.688 502.094C555.617 524.626 604.021 563.031 653.625 555.281C653.826 555.221 654.089 555.187 654.281 555.125C654.289 555.102 654.286 555.069 654.312 555.062C654.4 555.04 654.467 555.01 654.562 554.969C654.884 554.829 655.271 554.459 655.656 554.125C605.701 561.662 557.416 523.748 534.688 502.094Z')
        #end
    #end

    def test_raise_error_with_set_file_name_as_int(self):
        raise_error_svg = Svg()

        with self.assertRaises(ValueError) as e:
            error = raise_error_svg.read(1)
        #end with
        self.assertEqual(e.exception.args[0], 'file_name must be str')
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end
