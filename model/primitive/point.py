# model/primitive/point.py
import math
from shapely.geometry import Point as ShapelyPoint

class Point:
    def __init__(self, x: float, y: float):
        # 内部データは float で保持（高速アクセス用）
        self._x = float(x)
        self._y = float(y)
        # Shapelyオブジェクトをキャッシュ（必要になったら遅延生成）
        self._shapely_cache = None
    #end def

    @property
    def x(self) -> float:
        return self._x
    #end def

    @property
    def y(self) -> float:
        return self._y
    #end def

    @property
    def shapely(self) -> ShapelyPoint:
        """Shapelyの演算にそのまま放り込めるオブジェクトを返す"""
        if self._shapely_cache is None:
            self._shapely_cache = ShapelyPoint(self._x, self._y)
        #end if
        return self._shapely_cache
    #end def

    def __str__(self) -> str:
        return f"{self._x:.3f} {self._y:.3f}"
    #end def

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        #end if
        return (self._x == other.x) and (self._y == other.y)
    #end def

    def distance(self, other_point: 'Point') -> float:
        # 2点間の距離はシンプルな数式の方が速いのでそのまま
        delta_x = self._x - other_point.x
        delta_y = self._y - other_point.y
        return math.sqrt(delta_x * delta_x + delta_y * delta_y)
    #end def

    def get_midpoint(self, other_point: 'Point') -> 'Point':
        return Point((self._x + other_point.x) / 2.0, (self._y + other_point.y) / 2.0)
    #end def
#end class