
import math

from point import Point

class Vector:
    def __init__(self, start, end):
        if not type(start) is Point:
            raise TypeError("p0 must be Point")
        #end if
        if not type(end) is Point:
            raise TypeError("p1 must be Point")
        #end if
        self.__x = end.x - start.x
        self.__y = end.y - start.y
    #end

    @property
    def x(self):
        return self.__x
    #end def

    @property
    def y(self):
        return self.__y
    #end def

    def __str__(self):
        s = ""
        s += "{:.3f} {:.3f}".format( self.__x, self.__y )
        return s
    #end 

    def __eq__(self, other):
        return (self.__x == other.x) and (self.__y == other.y)
    #end

    def dot(self, other):
        return self.__x * other.x + self.__y * other.y
    #end

    def abs(self):
        return math.sqrt( self.__x*self.__x + self.__y*self.__y )
    #end

    def calc_angle(self, other):
        return math.acos( self.dot(other) / (self.abs() * other.abs()) )
    #end


        
#end

