
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

        self._start_index = 0
        self._end_index   = -1
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

    def update_start_index(self, start_index):
        if( self._start_index < start_index ):
            self._start_index = start_index
        #end
    #end

    def update_end_index(self, end_index):
        if( self._end_index == -1):
            self._end_index = end_index
        elif( end_index < self._end_index ):
            self._end_index = end_index
        #end
    #end

    @property
    def start_index(self):
        return self._start_index
    #end
    @property
    def end_index(self):
        return self._end_index
    #end

    def _get_the_end(self):
        # if self._end_index is initial state, then ...
        if (self._end_index == -1):
            return len(self._going_ctrl_p_list) 
        #end
        # if self._end_index is over the array size
        if ( self._end_index >= len(self._going_ctrl_p_list) ):
            return len(self._going_ctrl_p_list)
        #end
        # others, self._end_index is correct
        return self._end_index
    #end

#end