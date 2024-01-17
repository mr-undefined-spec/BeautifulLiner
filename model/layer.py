
from curve_set import CurveSet
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

    def append(self, curve_set):
        if not isinstance(curve_set, CurveSet):
            raise TypeError("The argument of the append method must be a CurveSet")
        #end if
        self._data.append(curve_set)
    #end def
#end

