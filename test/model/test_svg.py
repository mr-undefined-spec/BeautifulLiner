
import os
import sys

import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))

from point import Point
from control_point import CubicBezierCurveControlPoint
from control_point import LinearApproximateCurveControlPoint
from curve import CubicBezierCurve
from curve import LinearApproximateCurve
from layer import Layer

from svg import Svg

import unittest

class TestSvgData(unittest.TestCase):
    def test_read(self):
        svg_from_file = Svg(0, "TEST")
        svg_from_file.read("data/test.svg")

        xs = []
        ys = []

        for layer in svg_from_file:
            for curve_set in layer.path_data:
                for curve in curve_set:
                    for ctrl_p in curve:
                        xs.append( ctrl_p.x )
                        ys.append( ctrl_p.y )
                    #end
                #end
            #end
        #end

        the_answer_x = [40.8691, 38.5707, 35.1518, 33.9258, 33.9258, 31.6384, 32.5195, 32.5195, 22.5, 23.8877, 45.2065, 48.1641, 48.1641, 68.5839, 88.8765, 109.336, 109.336, 118.233, 129.572, 137.812, 107.49, 127.674, 125.433, 120.498]
        the_answer_y = [47.5488, 56.5236, 66.0395, 75.2344, 75.2344, 92.3896, 111.423, 128.76, 68.3789, 66.9912, 65.9304, 65.5664, 65.5664, 63.0532, 63.8199, 65.2148, 65.2148, 65.8215, 64.5223, 68.6426, 47.373, 64.4515, 109.947, 132.979]

        self.assertEqual(xs, the_answer_x)
        self.assertEqual(ys, the_answer_y)
    #end

    def test_raise_error_with_set_file_name_as_int(self):
        raise_error_svg = Svg(0, "TEST")

        with self.assertRaises(ValueError) as e:
            error = raise_error_svg.read(1)
        #end with
        self.assertEqual(e.exception.args[0], 'file_name must be str')
    #end

    def test_write(self):
        svg_from_file = Svg(0, "TEST")
        # just read
        svg_from_file.read("data/test.svg")

        # just write
        svg_from_file.write("data/write_test.svg")

        reread_svg = Svg(0, "TEST")
        reread_svg.read("data/write_test.svg")
        xs = []
        ys = []

        for layer in reread_svg:
            for curve_set in layer.path_data:
                for curve in curve_set:
                    for ctrl_p in curve:
                        xs.append( ctrl_p.x )
                        ys.append( ctrl_p.y )
                    #end
                #end
            #end
        #end

        the_answer_x = [40.869, 38.571, 35.152, 33.926, 33.926, 31.638, 32.52, 32.52, 22.5, 23.888, 45.206, 48.164, 48.164, 68.584, 88.876, 109.336, 109.336, 118.233, 129.572, 137.812, 107.49, 127.674, 125.433, 120.498]
        the_answer_y = [47.549, 56.524, 66.04, 75.234, 75.234, 92.39, 111.423, 128.76, 68.379, 66.991, 65.93, 65.566, 65.566, 63.053, 63.82, 65.215, 65.215, 65.822, 64.522, 68.643, 47.373, 64.451, 109.947, 132.979]

        self.assertEqual(xs, the_answer_x)
        self.assertEqual(ys, the_answer_y)
    #end
#end

if __name__ == '__main__':
    unittest.main()
#end
