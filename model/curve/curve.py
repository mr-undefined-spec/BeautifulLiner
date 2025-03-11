
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
        self._ctrl_p_set = []
        self.__intersect_judge_rectangular = None
    #end

    def __getitem__(self, i):
        return self._ctrl_p_set[i]
    #end

    def __iter__(self):
        self._index = 0
        return self
    #end
    def __next__(self):
        if self._index >= len(self._ctrl_p_set): raise StopIteration
        self._index += 1
        return self._ctrl_p_set[self._index-1]
    #end

    def __len__(self):
        return len(self._ctrl_p_set)
    #end

    @property
    def ctrl_p_set(self):
        return self._ctrl_p_set
    #end

    def to_str(self, is_first):
        s = ""
        for i, ctrl_p in enumerate(self._ctrl_p_set):
            s += ctrl_p.to_str(is_first)
        #end
        return s
    #end
#end
