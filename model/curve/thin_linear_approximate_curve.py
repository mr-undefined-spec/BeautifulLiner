# model/curve/thin_linear_approximate_curve.py
from shapely.geometry import LineString
from model.primitive.point import Point
from model.curve.curve import Curve

class ThinLinearApproximateCurve(Curve):
    def __init__(self, points: list[Point]):
        if len(points) < 2:
            raise ValueError("直線近似曲線には最低2つの点が必要です")
        #end if

        self._points: list[Point] = [Point(p.x, p.y) for p in points]
        self._shapely_cache = None
    #end def

    @property
    def points(self) -> list[Point]:
        return self._points
    #end def

    @property
    def is_broad(self) -> bool:
        return False
    #end def

    @property
    def shapely(self) -> LineString:
        """点列から一瞬でShapelyのLineStringを生成（初回のみ）してキャッシュ"""
        if self._shapely_cache is None:
            # 各Pointの座標ペアのリストから LineString を構築
            coords = [(p.x, p.y) for p in self._points]
            self._shapely_cache = LineString(coords)
        #end if
        return self._shapely_cache
    #end def

    def to_str(self) -> str:
        """点列からSVGのパス文字列（M x y L x y ...）を生成"""
        if not self._points:
            return ""
        #end if
        
        # 最初の点だけ M、残りは L で繋ぐ
        segments = [f"M {self._points[0]}"]
        for p in self._points[1:]:
            segments.append(f"L {p}")
        #end for
        
        # 末尾に半角スペースを空ける旧実装の癖（to_strの仕様）を継承
        return " ".join(segments) + " "
    #end def
#end class