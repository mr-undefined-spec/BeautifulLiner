
from point import Point
class Segment:
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
    #end def

    @property
    def e(self):
        return self.__end
    #end def

    def maxX(self):
        return max(self.__start.x, self.__end.x)
    #end def
    def minX(self):
        return min(self.__start.x, self.__end.x)
    #end def
    def maxY(self):
        return max(self.__start.y, self.__end.y)
    #end def
    def minY(self):
        return min(self.__start.y, self.__end.y)
    #end def

    def dot3(self, o, a, b):
        return (a.x - o.x) * (b.x - o.x) + (a.y - o.y) * (b.y - o.y)
    #end def
    def cross3(self, o, a, b):
        return (a.x - o.x) * (b.y - o.y) - (b.x - o.x) * (a.y - o.y)
    #end def
    def dist2(self, a, b):
        return (a.x - b.x) ** 2 + (a.y - b.y) ** 2
    #end def
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
    #end def

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
            return False
        #end if
    #end def

    def __str__(self):
        s = ""
        s += str(self.__start) + "\n"
        s += str(self.__end) + "\n"
        return s
    #end 
#end

