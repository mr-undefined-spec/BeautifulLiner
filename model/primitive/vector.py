# model/primitive/vector.py
import math
from point import Point

class Vector:
    def __init__(self, start: Point, end: Point):
        if not isinstance(start, Point):
            raise TypeError("start must be Point")
        #end if
        if not isinstance(end, Point):
            raise TypeError("end must be Point")
        #end if
        
        self._x = end.x - start.x
        self._y = end.y - start.y
    #end def

    @property
    def x(self) -> float:
        return self._x
    #end def

    @property
    def y(self) -> float:
        return self._y
    #end def

    def __str__(self) -> str:
        return f"{self._x:.3f} {self._y:.3f}"
    #end def

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return False
        #end if
        return (self._x == other.x) and (self._y == other.y)
    #end def

    def dot(self, other: 'Vector') -> float:
        return self._x * other.x + self._y * other.y
    #end def

    def abs(self) -> float:
        return math.sqrt(self._x * self._x + self._y * self._y)
    #end def

    def calc_angle(self, other: 'Vector') -> float:
        # ゼロ除算のバグを未然に防ぐ防護策
        denominator = self.abs() * other.abs()
        if denominator == 0.0:
            return 0.0
        #end if
        
        # 浮動小数点の演算誤差で acos の引数が 1.000000001 とかになり
        # ドメインエラー（ValueError）になるのを防ぐためのクリッピング
        cos_val = self.dot(other) / denominator
        cos_val = max(-1.0, min(1.0, cos_val))
        
        return math.acos(cos_val)
    #end def
#end class