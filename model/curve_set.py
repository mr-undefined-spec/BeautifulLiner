
from segment import Segment
from cubic_bezier_curve import CubicBezierCurve
class CurveSet:
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

class CubicBezierCurveSet(CurveSet):
    def append(self, curve):
        if not type(curve) is CubicBezierCurve:
            raise TypeError("The argument of the append method must be a CubicBezierCurve")
        #end if
        self._data.append(curve)
    #end def
#end

class SegmentSet(CurveSet):
    def append(self, segment):
        if not type(segment) is Segment:
            raise TypeError("The argument of the append method must be a Segment")
        #end if
        self._data.append(segment)
    #end def
#end

