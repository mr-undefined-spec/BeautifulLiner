
from curve import Curve
class CurveSet:
    def __init__(self):
        self.__data = []
    #end

    def append(self, curve):
        if not type(curve) is Curve:
            raise TypeError("The argument of the append method must be a Curve")
        #end if
        self.__data.append(curve)
    #end def

    def __getitem__(self, i):
        return self.__data[i]
    #end def

    def __iter__(self):
        self._index = 0
        return self
    #end def
    def __next__(self):
        if self._index >= len(self.__data): raise StopIteration
        self._index += 1
        return self.__data[self._index-1]
    #end def

#end


