
from curve_set import CubicBezierCurveSet
from curve_set import SegmentSet
class Layer:
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

class CubicBezierCurveSetLayer(Layer):
    def append(self, curve_set):
        if not type(curve_set) is CubicBezierCurveSet:
            raise TypeError("The argument of the append method must be a CubicBezierCurveSet")
        #end if
        self._data.append(curve_set)
    #end def
#end

class SegmentSetLayer(Layer):
    def append(self, segment_set):
        if not type(segment_set) is SegmentSet:
            raise TypeError("The argument of the append method must be a SegmentSet")
        #end if
        self._data.append(segment_set)
    #end def
#end

