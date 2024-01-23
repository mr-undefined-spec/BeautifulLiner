
from curve_set import CurveSet
class Layer:
    def __init__(self):
        self.__curve_set = []
    #end

    def __getitem__(self, i):
        return self.__curve_set[i]
    #end def

    def __iter__(self):
        self.__index = 0
        return self
    #end def
    def __next__(self):
        if self.__index >= len(self.__curve_set): raise StopIteration
        self.__index += 1
        return self.__curve_set[self.__index-1]
    #end def

    def append(self, curve_set):
        if not isinstance(curve_set, CurveSet):
            raise TypeError("The argument of the append method must be a CurveSet(CubicBezierCurveSet or SegmentSet)")
        #end if
        self.__curve_set.append(curve_set)
    #end def
#end

