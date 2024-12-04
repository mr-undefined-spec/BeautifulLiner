
import numpy as np
from scipy.special import comb

import math
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

from rectangular import Rectangular

from pyqtree import Index

class Curve:
    def __init__(self):
        self._going_ctrl_p_set = []
        self.__intersect_judge_rectangular = None
        self._start_index = 0
        self._end_index   = -1
    #end

    def _get_the_end(self):
        # if self._end_index is initial state, then ...
        if (self._end_index == -1):
            return len(self._going_ctrl_p_set) 
        #end
        # if self._end_index is over the array size
        if ( self._end_index >= len(self._going_ctrl_p_set) ):
            return len(self._going_ctrl_p_set)
        #end
        # others, self._end_index is correct
        return self._end_index
    #end

    def __getitem__(self, i):
        return self._going_ctrl_p_set[i]
    #end

    def __iter__(self):
        self._index = 0
        return self
    #end
    def __next__(self):
        if self._index >= len(self._going_ctrl_p_set): raise StopIteration
        self._index += 1
        return self._going_ctrl_p_set[self._index-1]
    #end

    def __len__(self):
        return len(self._going_ctrl_p_set)
    #end

    def create_intersect_judge_rectangle(self):
        min_x = self._going_ctrl_p_set[0].get_min_x()
        max_x = self._going_ctrl_p_set[0].get_max_x()
        min_y = self._going_ctrl_p_set[0].get_min_y()
        max_y = self._going_ctrl_p_set[0].get_max_y()
        for ctrl_p in self._going_ctrl_p_set:
            min_x = min( min_x, ctrl_p.get_min_x() )
            max_x = max( max_x, ctrl_p.get_max_x() )
            min_y = min( min_y, ctrl_p.get_min_y() )
            max_y = max( max_y, ctrl_p.get_max_y() )
        #end
        self.__intersect_judge_rectangular = Rectangular(min_x, max_x, min_y, max_y)
    #end

    @property
    def rect(self):
        return self.__intersect_judge_rectangular
    #end

    @property
    def going_ctrl_p_set(self):
        return self._going_ctrl_p_set
    #end

    def to_svg(self, position=None):
        s = ""
        for i, ctrl_p in enumerate(self._going_ctrl_p_set):
            s += ctrl_p.to_svg(i==0)
        #end
        return s
    #end
#end
