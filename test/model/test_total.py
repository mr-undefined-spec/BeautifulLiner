
import os
import sys
import math

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

class TestTotal(unittest.TestCase):
    def test(self):

        num_angle_divisions = 100
        # LinearApproximateCurve of 0 ~ 90degree arc ( radius=100, center=(0.0,0.0) )
        radius = 100.0
        linear_approximate_curve = LinearApproximateCurve()
        for i in range(num_angle_divisions):
            start_theta = math.pi / 2.0 *  i      / num_angle_divisions
            end_theta   = math.pi / 2.0 * (i + 1) / num_angle_divisions
            start_p = Point( radius*math.cos(start_theta), radius*math.sin(start_theta) )
            end_p   = Point( radius*math.cos(end_theta),   radius*math.sin(end_theta) )
            linear_approximate_curve.append(  LinearApproximateCurveControlPoint( start_p, end_p )  )
        #end

        # LinearApproximateCurve of 90 ~ 180 degree arc ( radius=100, center=(100.0,0.0) )
        lin_curve2 = LinearApproximateCurve()
        for i in range(num_angle_divisions):
            start_theta = math.pi / 2.0 *  i      / num_angle_divisions + math.pi / 2.0
            end_theta   = math.pi / 2.0 * (i + 1) / num_angle_divisions + math.pi / 2.0
            start_p = Point( radius*math.cos(start_theta) + 100.0, radius*math.sin(start_theta) )
            end_p   = Point( radius*math.cos(end_theta)   + 100.0, radius*math.sin(end_theta) )
            lin_curve2.append(  LinearApproximateCurveControlPoint( start_p, end_p )  )
        #end

        layer = Layer()
        layer.append(linear_approximate_curve)
        layer.append(lin_curve2)

        new_layer = layer.delete_edge(0.5)

        broad_linear_layer = new_layer.broaden(1.0)
        broad_smooth_layer = broad_linear_layer.smoothen()

        print( broad_smooth_layer.to_svg() )
    #end
#end

if __name__ == '__main__':
    unittest.main()
#end
