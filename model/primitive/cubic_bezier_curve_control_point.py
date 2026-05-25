# model/primitive/cubic_bezier_curve_control_point.py
from shapely.geometry import MultiPoint
from point import Point

class CubicBezierCurveControlPoint:
    def __init__(self, p0: Point, p1: Point, p2: Point, p3: Point):
        if not isinstance(p0, Point):
            raise TypeError("p0 must be Point")
        #end if
        if not isinstance(p1, Point):
            raise TypeError("p1 must be Point")
        #end if
        if not isinstance(p2, Point):
            raise TypeError("p2 must be Point")
        #end if
        if not isinstance(p3, Point):
            raise TypeError("p3 must be Point")
        #end if

        self._p0 = Point(p0.x, p0.y)
        self._p1 = Point(p1.x, p1.y)
        self._p2 = Point(p2.x, p2.y)
        self._p3 = Point(p3.x, p3.y)
        
        # ShapelyのMultiPointオブジェクトをキャッシュ用として保持（遅延生成）
        self._shapely_cache = None
    #end def

    @property
    def p0(self) -> Point:
        return self._p0
    #end def

    @property
    def p1(self) -> Point:
        return self._p1
    #end def

    @property
    def p2(self) -> Point:
        return self._p2
    #end def

    @property
    def p3(self) -> Point:
        return self._p3
    #end def

    @property
    def shapely(self) -> MultiPoint:
        """4つの制御点を内包するShapelyのMultiPointオブジェクトを返す"""
        if self._shapely_cache is None:
            self._shapely_cache = MultiPoint([
                self._p0.shapely,
                self._p1.shapely,
                self._p2.shapely,
                self._p3.shapely
            ])
        #end if
        return self._shapely_cache
    #end def

    def __iter__(self):
        yield self._p0
        yield self._p1
        yield self._p2
        yield self._p3
    #end def

    def get_max_x(self) -> float:
        return self.shapely.bounds[2]
    #end def

    def get_min_x(self) -> float:
        return self.shapely.bounds[0]
    #end def

    def get_max_y(self) -> float:
        return self.shapely.bounds[3]
    #end def

    def get_min_y(self) -> float:
        return self.shapely.bounds[0]
    #end def

    def __str__(self) -> str:
        return f"{self._p0}\n{self._p1}\n{self._p2}\n{self._p3}\n"
    #end def

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CubicBezierCurveControlPoint):
            return False
        #end if
        return (self._p0 == other.p0 and
                self._p1 == other.p1 and
                self._p2 == other.p2 and
                self._p3 == other.p3)
    #end def

    def to_str(self, is_going_first: bool, is_returning_first: bool = False) -> str:
        s = ""
        if is_going_first:
            s += f"M {self._p0} "
        #end if
        if is_returning_first:
            s += f"L {self._p0} "
        #end if
        s += f"C {self._p1} {self._p2} {self._p3} "
        return s
    #end def
#end class