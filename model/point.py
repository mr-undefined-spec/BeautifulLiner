
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
#end

