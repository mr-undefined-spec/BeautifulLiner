from enum import Enum, auto
from shapely.geometry import LineString
from shapely.geometry.base import BaseGeometry
import numpy as np
from model.primitive.point import Point

class CurveType(Enum):
    CUBIC_BEZIER = auto()       # 3次ベジェ曲線 (制御点を含む)
    LINEAR_APPROXIMATE = auto() # 線形近似曲線 (実点のみ)
#end class

class Curve:
    def __init__(self, points: list[Point], curve_type: CurveType, is_broad: bool = False):
        """
        整合性チェック（バリデーション）
        """
        if curve_type == CurveType.CUBIC_BEZIER:
            if len(points) < 4 or (len(points) - 1) % 3 != 0:
                raise ValueError("3次ベジエ曲線の点列は、4点以上かつ「3N + 1」の個数である必要があります")
            #end if
        elif curve_type == CurveType.LINEAR_APPROXIMATE:
            if len(points) < 2:
                raise ValueError("直線近似曲線には最低2つの点が必要です")
            #end if
        #end if

        # 内部データの保持
        self._points: list[Point] = [Point(p.x, p.y) for p in points]
        self._curve_type: CurveType = curve_type
        self._is_broad: bool = is_broad
        self._shapely_cache = None

        # 🌟 幾何トポロジー連携用のメタデータ（初期値はすべて None）
        self._id_before_trim: int | None = None
        self._start_trimmed_by: int | None = None
        self._end_trimmed_by: int | None = None
    #end def

    @property
    def points(self) -> list[Point]:
        return self._points
    #end def

    @property
    def curve_type(self) -> CurveType:
        return self._curve_type
    #end def

    @property
    def is_broad(self) -> bool:
        """厚みがある（面表現である）かどうかのフラグ"""
        return self._is_broad
    #end def

    # 🌟 トポロジー解析用のプロパティ群（Getter / Setter）

    @property
    def id_before_trim(self) -> int | None:
        """トリム前（DeleteEdge適用前）の元のCurveオブジェクトの id()"""
        return self._id_before_trim
    @id_before_trim.setter
    def id_before_trim(self, value: int | None):
        self._id_before_trim = value

    @property
    def start_trimmed_by(self) -> int | None:
        """始点側のトリム原因となった相方のCurveオブジェクトの id()"""
        return self._start_trimmed_by
    @start_trimmed_by.setter
    def start_trimmed_by(self, value: int | None):
        self._start_trimmed_by = value

    @property
    def end_trimmed_by(self) -> int | None:
        """終点側のトリム原因となった相方のCurveオブジェクトの id()"""
        return self._end_trimmed_by
    @end_trimmed_by.setter
    def end_trimmed_by(self, value: int | None):
        self._end_trimmed_by = value


    @property
    def shapely(self) -> BaseGeometry:
        """Shapelyの幾何オブジェクト（LineString または Polygon）を返す"""
        if self._shapely_cache is None:
            if self._curve_type == CurveType.CUBIC_BEZIER:
                self._shapely_cache = self._generate_bezier_shapely()
            elif self._curve_type == CurveType.LINEAR_APPROXIMATE:
                self._shapely_cache = self._generate_linear_shapely()
            #end if
        #end if
        
        return self._shapely_cache
    #end def

    def to_str(self) -> str:
        """SVGのパスデータ文字列を返す"""
        if not self._points:
            return ""
        #end if

        if self._curve_type == CurveType.CUBIC_BEZIER:
            return self._to_bezier_str()
        elif self._curve_type == CurveType.LINEAR_APPROXIMATE:
            return self._to_linear_str()
        #end if
        
        return ""
    #end def

    # -------------------------------------------------------------------------
    # 内部ヘルパーメソッド
    # -------------------------------------------------------------------------

    def _generate_bezier_shapely(self) -> LineString:
        """ベジェ曲線をサンプリングして LineString を生成"""
        sampled_coords = []
        num_segments = (len(self._points) - 1) // 3

        for i in range(num_segments):
            idx = i * 3
            p0 = self._points[idx]
            p1 = self._points[idx + 1]
            p2 = self._points[idx + 2]
            p3 = self._points[idx + 3]

            # 各区間を30分割してサンプリング
            t_steps = np.linspace(0.0, 1.0, 30) if i == 0 else np.linspace(1.0 / 30, 1.0, 29)
            
            for t in t_steps:
                x = (1 - t)**3 * p0.x + 3 * (1 - t)**2 * t * p1.x + 3 * (1 - t) * t**2 * p2.x + t**3 * p3.x
                y = (1 - t)**3 * p0.y + 3 * (1 - t)**2 * t * p1.y + 3 * (1 - t) * t**2 * p2.y + t**3 * p3.y
                sampled_coords.append((x, y))
            #end for
        #end for
                
        return LineString(sampled_coords)
    #end def

    def _generate_linear_shapely(self) -> LineString:
        """点列から直接 LineString を生成"""
        coords = [(p.x, p.y) for p in self._points]
        return LineString(coords)
    #end def

    def _to_bezier_str(self) -> str:
        """3次ベジェのSVGパス文字列生成"""
        segments = [f"M {self._points[0]}"]
        num_segments = (len(self._points) - 1) // 3

        for i in range(num_segments):
            idx = i * 3
            cp1 = self._points[idx + 1]
            cp2 = self._points[idx + 2]
            end = self._points[idx + 3]
            segments.append(f"C {cp1}, {cp2}, {end}")
        #end for

        return " ".join(segments) + " "
    #end def

    def _to_linear_str(self) -> str:
        """直線近似のSVGパス文字列生成"""
        segments = [f"M {self._points[0]}"]
        for p in self._points[1:]:
            segments.append(f"L {p}")
        #end for
            
        return " ".join(segments) + " "
    #end def
#end class