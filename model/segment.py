
from point import Point
class Segment:
    def __init__(self, start, end):
        if not type(start) is Point:
            raise TypeError("p0 must be Point")
        if not type(end) is Point:
            raise TypeError("p1 must be Point")
        self.__start = start
        self.__end   = end
    #end

    @property
    def s(self):
        return self.__start
    #end def

    @property
    def e(self):
        return self.__end
    #end def

    def __str__(self):
        s = ""
        s += str(self.__start) + "\n"
        s += str(self.__end) + "\n"
        return s
    #end 
#end

