
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/primitive'))
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/curve'))
from linear_approximate_curve import LinearApproximateCurve

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/layer'))
from layer import Layer

import model_mocks

from unittest.mock import MagicMock

import math
from enum import Enum

def create_mock_layer_set_of_cubic_bezier_curve_arc():#radius, center_point_x, center_point_y, start_angle, end_angle, num_angle_divisions):
    # CubicBezierCurve of 90degree arc (radius=100)
    p0 = model_mocks.create_mock_point(100.0,                              0.0)
    p1 = model_mocks.create_mock_point(100.0,                              400.0*( math.sqrt(2.0) - 1.0 )/3.0)
    p2 = model_mocks.create_mock_point(400.0*( math.sqrt(2.0) - 1.0 )/3.0, 100.0)
    p3 = model_mocks.create_mock_point(0.0,                                100.0)
    ctrl_p = model_mocks.create_mock_cubic_bezier_control_point(p0, p1, p2, p3)

    curve = [ctrl_p]
    layer = model_mocks.create_mock_layer([curve])
    layer_set = [layer]

    return layer_set
#end

class ArcDirection(Enum):
    CLOCKWISE = "clockwize"
    COUNTER_CLOCKWISE = "counter_clockwise"
#end

def create_mock_linear_approximate_curve_of_arc(radius, center_point_x, center_point_y, start_angle, end_angle, num_angle_divisions, arc_direction):

    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    delta_rad = end_rad - start_rad

    tmp_linear_ctrl_p_set = []
    for i in range(num_angle_divisions):
        start_theta = delta_rad *  i      / num_angle_divisions + start_rad
        end_theta   = delta_rad * (i + 1) / num_angle_divisions + start_rad
        start_p = Point(radius*math.cos(start_theta) + center_point_x, radius*math.sin(start_theta)  + center_point_y)
        end_p   = Point( radius*math.cos(end_theta)  + center_point_x, radius*math.sin(end_theta)    + center_point_y )
        tmp_linear_ctrl_p_set.append( model_mocks.create_mock_linear_approximate_curve_control_point(start_p, end_p) )
    #end

    linear_ctrl_p_set = []
    if arc_direction == ArcDirection.CLOCKWISE:
        for ctrl_p in tmp_linear_ctrl_p_set:
            linear_ctrl_p_set.append( model_mocks.create_mock_linear_approximate_curve_control_point(ctrl_p.start, ctrl_p.end) )
        #end
    elif arc_direction == ArcDirection.COUNTER_CLOCKWISE:
        tmp_linear_ctrl_p_set.reverse()
        for ctrl_p in tmp_linear_ctrl_p_set:
            linear_ctrl_p_set.append( model_mocks.create_mock_linear_approximate_curve_control_point(ctrl_p.end, ctrl_p.start) )
        #end
    #end

    linear_approximate_curve = LinearApproximateCurve()
    for ctrl_p in linear_ctrl_p_set:
        linear_approximate_curve.append(ctrl_p)
    #end
    return linear_approximate_curve
#end

def create_mock_linear_layer_set_of_arc(radius, center_point_x, center_point_y, start_angle, end_angle, num_angle_divisions):

    linear_approximate_curve = create_mock_linear_approximate_curve_of_arc(radius, center_point_x, center_point_y, start_angle, end_angle, num_angle_divisions)
    for ctrl_p in linear_ctrl_p_set:
        linear_approximate_curve.append(ctrl_p)
    #end

    layer = model_mocks.create_mock_layer([linear_approximate_curve])
    layer_set = [layer]

    return layer_set
#end
