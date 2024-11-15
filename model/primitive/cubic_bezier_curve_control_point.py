
from point import Point
from control_point import ControlPoint

class CubicBezierCurveControlPoint(ControlPoint):
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
    #end

    @property
    def p1(self):
        return self.__p1
    #end

    @property
    def p2(self):
        return self.__p2
    #end

    @property
    def p3(self):
        return self.__p3
    #end

    def __iter__(self):
        yield self.__p0
        yield self.__p1
        yield self.__p2
        yield self.__p3
    #end 

    def get_max_x(self):
        return max(self.__p0.x, self.__p1.x, self.__p2.x, self.__p3.x)
    #end
    def get_min_x(self):
        return min(self.__p0.x, self.__p1.x, self.__p2.x, self.__p3.x)
    #end
    def get_max_y(self):
        return max(self.__p0.y, self.__p1.y, self.__p2.y, self.__p3.y)
    #end
    def get_min_y(self):
        return min(self.__p0.y, self.__p1.y, self.__p2.y, self.__p3.y)
    #end

    def __str__(self):
        s = ""
        s += str(self.__p0) + "\n"
        s += str(self.__p1) + "\n"
        s += str(self.__p2) + "\n"
        s += str(self.__p3) + "\n"
        return s
    #end

    def __eq__(self, other):
        if(self.__p0 == other.p0
            and self.__p1 == other.p1
            and self.__p2 == other.p2
            and self.__p3 == other.p3):
            return True
        else:
            return False
        #end
    #end

    def to_svg(self, is_going_first, is_returning_first=False):
        s = ""
        if is_going_first:
            s += "M " + str(self.__p0) + " "
        #end
        if is_returning_first:
            s += "L " + str(self.__p0) + " "
        #end
        s += "C " + str(self.__p1) + " "
        s += str(self.__p2) + " "
        s += str(self.__p3) + " "
        return s
    #end
#end
