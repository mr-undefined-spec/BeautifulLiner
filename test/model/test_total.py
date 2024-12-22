
import os
import sys
import math

import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/compose'))

from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from cubic_bezier_curve import CubicBezierCurve
from linear_approximate_curve import LinearApproximateCurve
from layer import Layer

from layer_set import LayerSet

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

        layer = Layer("TEST")
        layer.append(linear_approximate_curve)
        layer.append(lin_curve2)

        bbox = (0.0, 0.0, 180.0, 180.0)
        layer.create_intersect_judge_rectangle(bbox)
        layer.create_sequential_points()
        layer.create_continuous_curve_index_group(2.0)
        layer.create_connection_point()

        new_layer = layer.delete_edge(bbox, 0.5, 0, "TEST")

        #broad_linear_layer = new_layer.broaden(1.0, 0, "TEST")
        #broad_smooth_layer = broad_linear_layer.broad_smoothen(0, "TEST")

#        print( broad_smooth_layer.to_LayerSet() )
    #end

    def test_4_arcs(self):

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

        # LinearApproximateCurve of 180 ~ 270 degree arc ( radius=100, center=(100.0,100.0) )
        lin_curve3 = LinearApproximateCurve()
        for i in range(num_angle_divisions):
            start_theta = math.pi / 2.0 *  i      / num_angle_divisions + math.pi
            end_theta   = math.pi / 2.0 * (i + 1) / num_angle_divisions + math.pi
            start_p = Point( radius*math.cos(start_theta) + 100.0, radius*math.sin(start_theta) + 100.0)
            end_p   = Point( radius*math.cos(end_theta)   + 100.0, radius*math.sin(end_theta)   + 100.0)
            lin_curve3.append(  LinearApproximateCurveControlPoint( start_p, end_p )  )
        #end

        # LinearApproximateCurve of 270 ~ 360 degree arc ( radius=100, center=(0.0,100.0) )
        lin_curve4 = LinearApproximateCurve()
        for i in range(num_angle_divisions):
            start_theta = math.pi / 2.0 *  i      / num_angle_divisions + 1.5*math.pi
            end_theta   = math.pi / 2.0 * (i + 1) / num_angle_divisions + 1.5*math.pi
            start_p = Point( radius*math.cos(start_theta), radius*math.sin(start_theta) + 100.0)
            end_p   = Point( radius*math.cos(end_theta)  , radius*math.sin(end_theta)   + 100.0)
            lin_curve4.append(  LinearApproximateCurveControlPoint( start_p, end_p )  )
        #end

        layer = Layer("TEST")
        layer.append(linear_approximate_curve)
        layer.append(lin_curve2)
        layer.append(lin_curve3)
        layer.append(lin_curve4)

        bbox = (0.0, 0.0, 180.0, 180.0)
        layer.create_intersect_judge_rectangle(bbox)
        layer.create_sequential_points()
        layer.create_continuous_curve_index_group(2.0)
        layer.create_connection_point()

        new_layer = layer.delete_edge(bbox, 0.5, 0, "TEST")

        #broad_linear_layer = new_layer.broaden(1.0, 0, "TEST")
        #broad_smooth_layer = broad_linear_layer.broad_smoothen(0, "TEST")

#        print( broad_smooth_layer.to_LayerSet(False) )
    #end
#end

if __name__ == '__main__':
    unittest.main()
#end
