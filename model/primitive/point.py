
import math

class Point:
    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)
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


    def distance(self, other_point):
        delta_x = self.__x - other_point.x
        delta_y = self.__y - other_point.y
        return math.sqrt( delta_x*delta_x + delta_y*delta_y )
    #end 

    def get_midpoint(self, other_point):
        return Point( (self.__x + other_point.x) / 2.0, (self.__y + other_point.y) / 2.0 )
    #end
        
#end

