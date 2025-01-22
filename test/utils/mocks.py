
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/primitive'))
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint

from unittest.mock import MagicMock

def create_mock_point(x, y):
    point = MagicMock(spec=Point, x=x, y=y)
    point.__str__.return_value = "{:.3f} {:.3f}".format( x, y )
    return point
#end

def create_mock_cubic_bezier_control_point():
    p0 = create_mock_point(0.0, 0.0)
    p1 = create_mock_point(1.0, 2.0)
    p2 = create_mock_point(10.0, 20.0)
    p3 = create_mock_point(100.0, 200.0)

    bezier_ctrl_p = MagicMock(spec=CubicBezierCurveControlPoint, p0=p0, p1=p1, p2=p2, p3=p3)
    s = ""
    for p in [p0, p1, p2, p3]:
        s += str(p) + "\n"
    #end
    bezier_ctrl_p.__str__.return_value = s
    #point.__str__.return_value = "{:.3f} {:.3f}".format( x, y )
    return bezier_ctrl_p
#end
