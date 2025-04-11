
import os
import sys

import math

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/primitive'))
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/curve'))
from linear_approximate_curve import LinearApproximateCurve

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/layer'))
from layer import Layer

from unittest.mock import MagicMock

def create_mock_point(x, y):
    point = MagicMock(spec=Point, x=x, y=y)
    point.__str__.return_value = "{:.3f} {:.3f}".format( x, y )
    point.distance = lambda other_p : math.sqrt( (point.x - other_p.x)*(point.x - other_p.x) + (point.y - other_p.y)*(point.y - other_p.y) )
    return point
#end

def create_mock_cubic_bezier_control_point(p0, p1, p2, p3):
    bezier_ctrl_p = MagicMock(spec=CubicBezierCurveControlPoint, p0=p0, p1=p1, p2=p2, p3=p3)
    s = ""
    for p in [p0, p1, p2, p3]:
        s += str(p) + "\n"
    #end
    bezier_ctrl_p.__str__.return_value = s
    return bezier_ctrl_p
#end

def create_mock_linear_approximate_curve_control_point(start, end):
    linear_ctrl_p = MagicMock(spec=LinearApproximateCurveControlPoint, start=start, end=end)
    s = ""
    for p in [start, end]:
        s += str(p) + "\n"
    #end
    linear_ctrl_p.__str__.return_value = s
    linear_ctrl_p.to_str.return_value = s

    min_x = min(start.x, end.x)
    max_x = max(start.x, end.x)
    min_y = min(start.y, end.y)
    max_y = max(start.y, end.y)
    linear_ctrl_p.get_rect_tuple.return_value = (min_x, min_y, max_x, max_y)

    return linear_ctrl_p
#end

def create_mock_linear_approximate_curve(linear_approximate_curve_control_point_set):
    linear_approximate_curve = MagicMock(spec=LinearApproximateCurve)
    linear_approximate_curve.__getitem__.side_effect = lambda index : linear_approximate_curve_control_point_set[index]
    linear_approximate_curve.__iter__.return_value = iter(linear_approximate_curve_control_point_set)
    return linear_approximate_curve
#end

def create_mock_layer(curve_set_list):
    layer = MagicMock(spec=Layer)
    layer.name = "test_layer"
    layer.__getitem__.side_effect = lambda index : curve_set_list[index]
    layer.__iter__.return_value = iter(curve_set_list)
    return layer
#end