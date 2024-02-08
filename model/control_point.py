
from point import Point
class ControlPoint:
    def __init__(self):
        pass
    #end
#end

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

class LinearApproximateCurveControlPoint(ControlPoint):
    def __init__(self, start, end):
        if not type(start) is Point:
            raise TypeError("p0 must be Point")
        #end if
        if not type(end) is Point:
            raise TypeError("p1 must be Point")
        #end if
        self.__start = start
        self.__end   = end
    #end

    @property
    def s(self):
        return self.__start
    #end

    @property
    def e(self):
        return self.__end
    #end

    def get_max_x(self):
        return max(self.__start.x, self.__end.x)
    #end
    def get_min_x(self):
        return min(self.__start.x, self.__end.x)
    #end
    def get_max_y(self):
        return max(self.__start.y, self.__end.y)
    #end
    def get_min_y(self):
        return min(self.__start.y, self.__end.y)
    #end

    def dot3(self, o, a, b):
        return (a.x - o.x) * (b.x - o.x) + (a.y - o.y) * (b.y - o.y)
    #end
    def cross3(self, o, a, b):
        return (a.x - o.x) * (b.y - o.y) - (b.x - o.x) * (a.y - o.y)
    #end
    def dist2(self, a, b):
        return (a.x - b.x) ** 2 + (a.y - b.y) ** 2
    #end

    def is_intersection(self, other_segment):
        c0 = self.cross3(self.__start, self.__end, other_segment.s)
        c1 = self.cross3(self.__start, self.__end, other_segment.e)
        d0 = self.cross3(other_segment.s, other_segment.e, self.__start)
        d1 = self.cross3(other_segment.s, other_segment.e, self.__end)
        if c0 == d1 == 0:
            e0 = self.dot3(self.__start, self.__end, other_segment.s)
            e1 = self.dot3(self.__start, self.__end, other_segment.e)
            if not e0 < e1:
                e0, e1 = e1, e0
            return e0 <= self.dist2(self.__start, self.__end) and 0 <= e1
        return c0 * c1 <= 0 and d0 * d1 <= 0
    #end

    def intersection(self, other_segment):
        if self.is_intersection(other_segment):
            a_self  = self.__end.x - self.__start.x
            b_self  = self.__end.y - self.__start.y
            a_other = other_segment.e.x - other_segment.s.x
            b_other = other_segment.e.y - other_segment.s.y

            d = a_self*b_other - a_other*b_self
            t = b_other * (other_segment.s.x - self.__start.x) - a_other * (other_segment.s.y - self.__start.y)
            return Point(self.__start.x + a_self*t/d, self.__start.y + b_self*t/d)
        else:
            raise ValueError("ERROR. Not intersect. Please use \"is_intersection\" method before calling \"intersection\" method.")
        #end if
    #end

    def __str__(self):
        s = ""
        s += str(self.__start) + "\n"
        s += str(self.__end) + "\n"
        return s
    #end 
    def to_svg(self, is_first_ctrl_p):
        s = ""
        if is_first_ctrl_p:
            s += "M " + str(self.__start) + " "
        #end
        s += "L " + str(self.__end) + " "
        return s
    #end
#end

