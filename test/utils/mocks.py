
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/primitive'))
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

from unittest.mock import MagicMock

def create_mock_point(x, y):
    point = MagicMock(spec=Point, x=x, y=y)
    point.__str__.return_value = "{:.3f} {:.3f}".format( x, y )
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
    return linear_ctrl_p
#end

def create_mock_linear_approximate_curve_control_point_set():
    p0 = create_mock_point(0.0, 0.0)
    p1 = create_mock_point(1.0, 1.0)
    p2 = create_mock_point(1.0, 0.0)
    p3 = create_mock_point(0.0, 1.0)
    p4 = create_mock_point(2.0, 1.0)

    linear_ctrl_p_set = []

    for p_set in [ [p0, p1], [p2, p3], [p2,p4] ]:
        tmp_linear_ctrl_p = create_mock_linear_approximate_curve_control_point(p_set[0], p_set[1])
        s = ""
        for p in p_set:
            s += str(p) + "\n"
        #end
        tmp_linear_ctrl_p.__str__.return_value = s
        linear_ctrl_p_set.append(tmp_linear_ctrl_p)
    #end
    return linear_ctrl_p_set
#end
