
from control_point import CubicBezierCurveControlPoint
from control_point import LinearApproximateCurveControlPoint

class Curve:
    def __init__(self):
        self._ctrl_p_set = []
    #end

    def __getitem__(self, i):
        return self._ctrl_p_set[i]
    #end def

    def __iter__(self):
        self._index = 0
        return self
    #end def
    def __next__(self):
        if self._index >= len(self._ctrl_p_set): raise StopIteration
        self._index += 1
        return self._ctrl_p_set[self._index-1]
    #end def

#end

class CubicBezierCurve(Curve):
    def append(self, bezier_ctrl_p):
        if not type(bezier_ctrl_p) is CubicBezierCurveControlPoint:
            raise TypeError("The argument of the append method must be a CubicBezierCurveControlPoint")
        #end if
        self._ctrl_p_set.append(bezier_ctrl_p)
    #end def

    def to_svg(self):
        is_first_ctrl_p = True
        s = ""
        for ctrl_p in self._ctrl_p_set:
            s += ctrl_p.to_svg(is_first_ctrl_p)
            is_first_ctrl_p = False
        #end
        return s
    #end
#end

class LinearApproximateCurve(Curve):
    def append(self, linear_ctrl_p):
        if not type(linear_ctrl_p) is LinearApproximateCurveControlPoint:
            raise TypeError("The argument of the append method must be a LinearApproximateCurveControlPoint")
        #end if
        self._ctrl_p_set.append(linear_ctrl_p)
    #end def
#end

