import os
import sys

import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/compose'))

sys.path.append(os.path.join(os.path.dirname(__file__), '../../utils'))

import reader

from point import Point
from cubic_bezier_curve import CubicBezierCurve
from linear_approximate_curve import LinearApproximateCurve
from layer import Layer

from layer_set import LayerSet

import unittest

class TestLayerSetData(unittest.TestCase):
    def test_create_layer_set_from_file(self):
        layer_set_from_file = reader.create_layer_set_from_file("data/test.svg", 0, "TEST")

        xs = []
        ys = []

        for layer in layer_set_from_file:
            for curve_set in layer:
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
