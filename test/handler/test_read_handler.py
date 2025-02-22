
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/curve'))
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from cubic_bezier_curve import CubicBezierCurve
from linear_approximate_curve import LinearApproximateCurve
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../../handler'))
from read_handler import ReadHandler

import numpy as np
import math

class TestReadHandler(unittest.TestCase):
    def test_read(self):
        self.layer_set = ReadHandler.create_layer_set_from_file("data/test.svg")

        the_answer = [[402.67,127.291],
                    [399.823,128.714],
                    [393.001,175.251],
                    [392.271,181.822],
                    [392.271,181.822],
                    [386.945,229.751],
                    [389.765,292.499],
                    [404.953,338.063],
                    [404.953,338.063],
                    [408.446,348.544],
                    [420.484,380.166],
                    [433.613,380.166],
                    [404.732,288.481],
                    [404.732,308.04],
                    [406.168,339.391],
                    [415.213,357.48],
                    [415.213,357.48],
                    [420.015,367.085],
                    [423.805,376.613],
                    [429.187,386.302],
                    [429.187,386.302],
                    [429.783,387.375],
                    [430.352,389.796],
                    [430.352,389.796]]

        the_answer_index = 0

        for layer in self.layer_set:
            for curve in layer:
                for ctrl_p in curve:
                    for point in ctrl_p:
                        self.assertEqual([point.x, point.y], the_answer[the_answer_index])
                        the_answer_index += 1
                    #end
                #end
            #end
        #end
        
    #end


#end

if __name__ == '__main__':
    unittest.main()
#end

