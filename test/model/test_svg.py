
import os
import sys

import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/primitive'))

from point import Point
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

        the_answer_x = [402.67, 399.823, 393.001, 392.271, 392.271, 386.945, 389.765, 404.953, 404.953, 408.446, 420.484, 433.613, 404.732, 404.732, 406.168, 415.213, 415.213, 420.015, 423.805, 429.187, 429.187, 429.783, 430.352, 430.352]
        the_answer_y = [127.291, 128.714, 175.251, 181.822, 181.822, 229.751, 292.499, 338.063, 338.063, 348.544, 380.166, 380.166, 288.481, 308.04, 339.391, 357.48, 357.48, 367.085, 376.613, 386.302, 386.302, 387.375, 389.796, 389.796]

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

        the_answer_x = [402.67, 399.823, 393.001, 392.271, 392.271, 386.945, 389.765, 404.953, 404.953, 408.446, 420.484, 433.613, 404.732, 404.732, 406.168, 415.213, 415.213, 420.015, 423.805, 429.187, 429.187, 429.783, 430.352, 430.352]
        the_answer_y = [127.291, 128.714, 175.251, 181.822, 181.822, 229.751, 292.499, 338.063, 338.063, 348.544, 380.166, 380.166, 288.481, 308.04, 339.391, 357.48, 357.48, 367.085, 376.613, 386.302, 386.302, 387.375, 389.796, 389.796]

        self.assertEqual(xs, the_answer_x)
        self.assertEqual(ys, the_answer_y)
    #end
#end

if __name__ == '__main__':
    unittest.main()
#end
