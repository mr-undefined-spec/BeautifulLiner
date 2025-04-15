from pyqtree import Index
import numpy as np

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../primitive'))
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from rectangular import Rectangular

from curve import Curve

class LinearApproximateCurve(Curve):
    def __init__(self):
        super().__init__()

        self.min_x = 999999
        self.max_x = -999999
        self.min_y = 999999
        self.max_y = -999999
    #end

    def append(self, linear_ctrl_p):
        if not isinstance(linear_ctrl_p, LinearApproximateCurveControlPoint):
            raise TypeError("The argument of the append method must be a LinearApproximateCurveControlPoint")
        #end

        self.min_x = min(self.min_x, linear_ctrl_p.start.x, linear_ctrl_p.end.x)
        self.max_x = max(self.max_x, linear_ctrl_p.start.x, linear_ctrl_p.end.x)
        self.min_y = min(self.min_y, linear_ctrl_p.start.y, linear_ctrl_p.end.y)
        self.max_y = max(self.max_y, linear_ctrl_p.start.y, linear_ctrl_p.end.y)

        self._going_ctrl_p_list.append(linear_ctrl_p)
    #end

    def to_str(self):
        s = ""
        the_end = self._get_the_end()
        for i in range( self._start_index, the_end ):
            ctrl_p = self._going_ctrl_p_list[i]
            s += ctrl_p.to_str(i==self._start_index)
        #end
        return s
    #end

    @property
    def rect(self):
        return Rectangular(self.min_x, self.max_x, self.min_y, self.max_y)
    #end


    def copy(self, other_linear_approximate_curve):
        for ctrl_p in other_linear_approximate_curve:
            self.append(ctrl_p)
        #end
        self._start_index = other_linear_approximate_curve.start_index
        self._end_index = other_linear_approximate_curve.end_index
        self._split_ranges = other_linear_approximate_curve.split_ranges
    #end

    def get_bounding_boxes(self):
        """各線分に対し、軸平行境界ボックス(AABB)を取得"""
        return [
            (min(ctrl_p.start.x, ctrl_p.end.x), min(ctrl_p.start.y, ctrl_p.end.y), 
             max(ctrl_p.start.x, ctrl_p.end.x), max(ctrl_p.start.y, ctrl_p.end.y))
            for ctrl_p in self._going_ctrl_p_list
        ]
    #end

    def get_going_ctrl_p_list(self):
        return_going_ctrl_p_list = []
        the_end = self._get_the_end()
        for i in range( self._start_index, the_end ):
            return_going_ctrl_p_list.append( self._going_ctrl_p_list[i] )
        #end
        return return_going_ctrl_p_list
    #end

    def create_qtree_going_ctrl_p_list(self, bbox):
        
        self.qtree_going_ctrl_p_list = Index(bbox=bbox)

        for ctrl_p in self._going_ctrl_p_list:
            rect_tuple = ctrl_p.get_rect_tuple()
            self.qtree_going_ctrl_p_list.insert(ctrl_p, rect_tuple)
        #end
    #end

    def get_intersect_segment_set(self, target_rect_tuple):
        return self.qtree_going_ctrl_p_list.intersect(target_rect_tuple)
    #end





#end