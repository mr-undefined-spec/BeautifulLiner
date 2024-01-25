
from control_point import CubicBezierCurveControlPoint
from control_point import LinearApproximateCurveControlPoint

class Curve:
    def __init__(self):
        self._data = []
    #end

    def __getitem__(self, i):
        return self._data[i]
    #end def

    def __iter__(self):
        self._index = 0
        return self
    #end def
    def __next__(self):
        if self._index >= len(self._data): raise StopIteration
        self._index += 1
        return self._data[self._index-1]
    #end def

#end

class CubicBezierCurve(Curve):
    def append(self, bezier_ctrl_p):
        if not type(bezier_ctrl_p) is CubicBezierCurveControlPoint:
            raise TypeError("The argument of the append method must be a CubicBezierCurveControlPoint")
        #end if
        self._data.append(bezier_ctrl_p)
    #end def
#end

class LinearApproximateCurve(Curve):
    def append(self, linear_ctrl_p):
        if not type(linear_ctrl_p) is LinearApproximateCurveControlPoint:
            raise TypeError("The argument of the append method must be a LinearApproximateCurveControlPoint")
        #end if
        self._data.append(linear_ctrl_p)
    #end def
#end

