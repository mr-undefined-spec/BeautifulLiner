
import numpy as np
from scipy.special import comb

import math
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

from rectangular import Rectangular

from pyqtree import Index

from curve import Curve

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class BroadLinearApproximateCurve(Curve):

    def __init__(self):
        super().__init__()
        self._returning_ctrl_p_list = []
    #end

    @property
    def returning_ctrl_p_list(self):
        return self._returning_ctrl_p_list
    #end

    def append_going(self, linear_ctrl_p):
        if not isinstance(linear_ctrl_p, LinearApproximateCurveControlPoint):
            raise TypeError("The argument of the append method must be a LinearApproximateCurveControlPoint")
        #end
        self._going_ctrl_p_list.append(linear_ctrl_p)
    #end

    def append_returning(self, linear_ctrl_p):
        if not isinstance(linear_ctrl_p, LinearApproximateCurveControlPoint):
            raise TypeError("The argument of the append method must be a LinearApproximateCurveControlPoint")
        #end
        self._returning_ctrl_p_list.append(linear_ctrl_p)
    #end

    def to_str(self):
        s = ""
        for i, ctrl_p in enumerate(self._going_ctrl_p_list):
            s += ctrl_p.to_str(i==0)
        #end
        for i, ctrl_p in enumerate(self._returning_ctrl_p_list):
            s += ctrl_p.to_str(False, i==0)
        #end
        return s
    #end


#end