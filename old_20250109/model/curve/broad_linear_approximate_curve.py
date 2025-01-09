
import numpy as np
from scipy.special import comb

import math
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

from linear_approximate_curve import LinearApproximateCurve

from rectangular import Rectangular

from pyqtree import Index

from curve import Curve

class BroadLinearApproximateCurve(LinearApproximateCurve):
    def __init__(self):
        Curve.__init__(self)
        self._returning_ctrl_p_set = []
    #end

    def set_ctrl_p_set(self, going_ctrl_p_set, returning_ctrl_p_set, start_index, end_index):
        self._going_ctrl_p_set     = going_ctrl_p_set
        self._returning_ctrl_p_set = returning_ctrl_p_set
        self._start_index          = start_index
        self._end_index            = end_index
    #end

    def broad_smoothen(self):
        from broad_cubic_bezier_curve import BroadCubicBezierCurve
        """ In LinearApproximateCurve, public smoothen method calls only one protected _smoothen method
        On the other hand, in BroadLinearApproximateCurve, public smoothen method calls two protected _smoothen methods(going & returning)"""
        the_end = self._get_the_end()
        going_smooth_ctrl_p = self._smoothen(self._going_ctrl_p_set, self._start_index, the_end)

        returning_start = len(self._returning_ctrl_p_set) - the_end 
        returning_end   = len(self._returning_ctrl_p_set) - self._start_index 
        returning_smooth_ctrl_p = self._smoothen(self._returning_ctrl_p_set, returning_start, returning_end)

        broad_cubic_bezier_curve = BroadCubicBezierCurve()
        broad_cubic_bezier_curve.set_ctrl_p(going_smooth_ctrl_p, returning_smooth_ctrl_p)
        
        return broad_cubic_bezier_curve
    #end

    def special_smoothen_for_hair(self):
        from broad_cubic_bezier_curve import BroadCubicBezierCurve
        """ In LinearApproximateCurve, public smoothen method calls only one protected _smoothen method
        On the other hand, in BroadLinearApproximateCurve, public smoothen method calls two protected _smoothen methods(going & returning)"""
        the_end = self._get_the_end()
        going_smooth_ctrl_p = self._smoothen(self._going_ctrl_p_set, self._start_index, the_end)

        returning_start = len(self._returning_ctrl_p_set) - the_end 
        returning_end   = len(self._returning_ctrl_p_set) - self._start_index 
        returning_smooth_ctrl_p = self._smoothen(self._returning_ctrl_p_set, returning_start, returning_end)

        #FIXME temporary implementation
        do_check_start_index = self._going_ctrl_p_set[0].s.y > self._going_ctrl_p_set[-1].s.y

        if( do_check_start_index ):
            if( self._start_index != 0 ):
                going_smooth_ctrl_p = CubicBezierCurveControlPoint(self._going_ctrl_p_set[self._start_index].s, 
                                                                    going_smooth_ctrl_p.p1,
                                                                    going_smooth_ctrl_p.p2,
                                                                    going_smooth_ctrl_p.p3)
                returning_smooth_ctrl_p = CubicBezierCurveControlPoint(returning_smooth_ctrl_p.p0,
                                                                        returning_smooth_ctrl_p.p1,
                                                                        returning_smooth_ctrl_p.p2,
                                                                        self._going_ctrl_p_set[self._start_index].s)
            #end
        else:
            if( the_end != len(self._going_ctrl_p_set) ):
                going_smooth_ctrl_p = CubicBezierCurveControlPoint(going_smooth_ctrl_p.p0, 
                                                                    going_smooth_ctrl_p.p1,
                                                                    going_smooth_ctrl_p.p2,
                                                                    self._going_ctrl_p_set[the_end].e)
                returning_smooth_ctrl_p = CubicBezierCurveControlPoint(self._going_ctrl_p_set[the_end].e,
                                                                        returning_smooth_ctrl_p.p1,
                                                                        returning_smooth_ctrl_p.p2,
                                                                        returning_smooth_ctrl_p.p3)
            #end
        #end

        broad_cubic_bezier_curve = BroadCubicBezierCurve()
        broad_cubic_bezier_curve.set_ctrl_p(going_smooth_ctrl_p, returning_smooth_ctrl_p)
        
        return broad_cubic_bezier_curve
    #end

    def _to_str_none(self):
        s = ""
        the_end = self._get_the_end()
        for i in range( self._start_index, the_end ):
            ctrl_p = self._going_ctrl_p_set[i]
            s += ctrl_p.to_str(i==self._start_index)
        #end

        returning_start = len(self._returning_ctrl_p_set) - the_end 
        returning_end   = len(self._returning_ctrl_p_set) - self._start_index 

        #print( self._start_index, self._end_index, returning_start, returning_end )
        for i in range( returning_start, returning_end):
            if i == len(self._returning_ctrl_p_set)-1:
                break
            ctrl_p = self._returning_ctrl_p_set[i]
            s += ctrl_p.to_str(False)
        #end
        s += "Z"
        return s
    #end

    def _to_str_first(self):
        s = ""
        the_end = self._get_the_end()
        for i in range( self._start_index, the_end ):
            ctrl_p = self._going_ctrl_p_set[i]
            s += ctrl_p.to_str(i==self._start_index)
        #end

        returning_start = len(self._returning_ctrl_p_set) - the_end 
        returning_end   = len(self._returning_ctrl_p_set) - self._start_index 

        #print( self._start_index, self._end_index, returning_start, returning_end )
        for i in range( returning_start, returning_end):
            if i == len(self._returning_ctrl_p_set)-1:
                break
            ctrl_p = self._returning_ctrl_p_set[i]
            s += ctrl_p.to_str(False)
        #end
        s += "Z"
        return s
    #end

    def to_str(self, position=None):
        if position is None:
            return self._to_str_none()
        #end
        if position == "First":
            return self._to_str_first()
        else:
            return self._to_str(position)
    #end
#end

