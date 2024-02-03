
from point import Point
class Rectangular:
    """
    Rectangular has 4 points

      q ------------------- p
      |                     |
      |                     |
      |                     |
      z ------------------- m

    The characters (q, p, z and m) is the keys in the four corners of a "qwerty" keyboard.

    """
    def __init__(self, min_x, max_x, min_y, max_y):
        self.__q = Point(min_x, min_y)
        self.__p = Point(max_x, min_y)
        self.__z = Point(min_x, max_y)
        self.__m = Point(max_x, max_y)
        self.__center = Point( (max_x + min_x)/2.0, (max_y + min_y)/2.0)

        self.__width  = max_x - min_x
        self.__height = max_y - min_y
    #end

    @property
    def q(self):
        return self.__q
    #end
    @property
    def p(self):
        return self.__p
    #end
    @property
    def z(self):
        return self.__z
    #end
    @property
    def m(self):
        return self.__m
    #end

    @property
    def center(self):
        return self.__center
    #end
    @property
    def width(self):
        return self.__width
    #end
    @property
    def height(self):
        return self.__height
    #end

    def test_collision(self, other_rect):
        delta_x = abs( other_rect.center.x - self.__center.x )
        delta_y = abs( other_rect.center.y - self.__center.y )

        sum_half_width  = ( other_rect.width  + self.__width  ) / 2.0
        sum_half_height = ( other_rect.height + self.__height ) / 2.0

        if ( (delta_x < sum_half_width) & (delta_y < sum_half_height) ):
            return True
        else:
            return False
        #end if
    #end

#end
