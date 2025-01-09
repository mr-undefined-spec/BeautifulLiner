import os
import sys
import math

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/compose'))

from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from cubic_bezier_curve import CubicBezierCurve
from linear_approximate_curve import LinearApproximateCurve

def create_arc(radius, center_point, start_angle, end_angle, num_angle_divisions):
    linear_approximate_curve = LinearApproximateCurve()
    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    delta_rad = end_rad - start_rad
    for i in range(num_angle_divisions):
        start_theta = delta_rad *  i      / num_angle_divisions + start_rad
        end_theta   = delta_rad * (i + 1) / num_angle_divisions + start_rad
        start_p = Point( radius*math.cos(start_theta) + center_point.x, radius*math.sin(start_theta)  + center_point.y )
        end_p   = Point( radius*math.cos(end_theta)   + center_point.x, radius*math.sin(end_theta)    + center_point.y )
        linear_approximate_curve.append(  LinearApproximateCurveControlPoint( start_p, end_p )  )
    #end
    linear_approximate_curve.create_sequential_points()
    return linear_approximate_curve
#end
