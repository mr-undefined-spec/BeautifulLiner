
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
        self._going_ctrl_p_list = []
        self._returning_ctrl_p_list = []
    #end

    @property
    def going_ctrl_p_list(self):
        return self._going_ctrl_p_list
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

    def get_points(self):
        points = []
        points.append(self._going_ctrl_p_list[self._start_index].start)

        the_end = self._get_the_end()
        for i in range( self._start_index, the_end ):
            points.append(self._going_ctrl_p_list[i].end)
        #end
        return points
    #end

#end