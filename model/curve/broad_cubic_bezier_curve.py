
import numpy as np
from scipy.special import comb

import math
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

from cubic_bezier_curve import CubicBezierCurve

from rectangular import Rectangular

from pyqtree import Index

from curve import Curve
class BroadCubicBezierCurve(CubicBezierCurve):
    def __init__(self):
        Curve.__init__(self)
        self._returning_ctrl_p_set = []
    #end

    def set_ctrl_p(self, going_ctrl_p, returning_ctrl_p):
        """ Curve has many control points, but BroadCubicBezierCurve has ONLY ONE control point in each going & returning."""
        self._going_ctrl_p_set     = [going_ctrl_p]
        self._returning_ctrl_p_set = [returning_ctrl_p]
    #end

    def to_svg(self):
        s = ""
        s += self._going_ctrl_p_set[0].to_svg(True)
        if(self._going_ctrl_p_set[0].p3 == self._returning_ctrl_p_set[0].p0 ):
            s += self._returning_ctrl_p_set[0].to_svg(False, False)
        else:
            s += self._returning_ctrl_p_set[0].to_svg(False, True)
        #end
        s += "Z"
        return s
    #end
#end
