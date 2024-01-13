
from point import Point
class CubicBezierCurve:
    def __init__(self, p0, p1, p2, p3):
        if not type(p0) is Point:
            raise TypeError("p0 must be Point")
        if not type(p1) is Point:
            raise TypeError("p1 must be Point")
        if not type(p2) is Point:
            raise TypeError("p2 must be Point")
        if not type(p3) is Point:
            raise TypeError("p3 must be Point")

        self.__p0 = Point(p0.x, p0.y)
        self.__p1 = Point(p1.x, p1.y)
        self.__p2 = Point(p2.x, p2.y)
        self.__p3 = Point(p3.x, p3.y)
    #end

    @property
    def p0(self):
        return self.__p0
    #end def

    @property
    def p1(self):
        return self.__p1
    #end def

    @property
    def p2(self):
        return self.__p2
    #end def

    @property
    def p3(self):
        return self.__p3
    #end def

    def __iter__(self):
        yield self.__p0
        yield self.__p1
        yield self.__p2
        yield self.__p3
    #end 

    def __str__(self):
        s = ""
        s += str(self.__p0) + "\n"
        s += str(self.__p1) + "\n"
        s += str(self.__p2) + "\n"
        s += str(self.__p3) + "\n"
        return s
    #end
#end

