
from segment import Segment
class SegmentSet:
    def __init__(self):
        self.__data = []
    #end

    def append(self, segment):
        if not type(segment) is Segment:
            raise TypeError("The argument of the append method must be a Segment")
        #end if
        self.__data.append(segment)
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


