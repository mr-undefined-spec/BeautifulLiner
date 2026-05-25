# model/curve/thin_cubic_bezier_curve.py
from shapely.geometry import LineString
import numpy as np
from model.primitive.point import Point
from model.curve.curve import Curve

class ThinCubicBezierCurve(Curve):
    def __init__(self, points: list[Point]):
        # 3次ベジエの連続は、必ず 4, 7, 10, 13... (3N + 1) 点になる
        if len(points) < 4 or (len(points) - 1) % 3 != 0:
            raise ValueError("3次ベジエ曲線の点列は、4点以上かつ「3N + 1」の個数である必要があります")
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
        """
        ベジエ曲線を適度な細かさで直線近似した LineString を生成してキャッシュします。
        ステップ5（美しい線を再度直線近似する）の処理にそのまま直結します。
        """
        if self._shapely_cache is None:
            sampled_coords = []
            num_segments = (len(self._points) - 1) // 3

            for i in range(num_segments):
                idx = i * 3
                p0 = self._points[idx]
                p1 = self._points[idx + 1]
                p2 = self._points[idx + 2]
                p3 = self._points[idx + 3]

                # 各区間を30分割してサンプリング（必要に応じて調整可能）
                # 最初の区間だけ t=0 を含め、以降は終点重複を避けるため t>0 からサンプリング
                t_steps = np.linspace(0.0, 1.0, 30) if i == 0 else np.linspace(1.0/30, 1.0, 29)
                
                for t in t_steps:
                    # 3次ベジエのバーンスタイン基底関数による座標計算
                    x = (1-t)**3 * p0.x + 3*(1-t)**2 * t * p1.x + 3*(1-t) * t**2 * p2.x + t**3 * p3.x
                    y = (1-t)**3 * p0.y + 3*(1-t)**2 * t * p1.y + 3*(1-t) * t**2 * p2.y + t**3 * p3.y
                    sampled_coords.append((x, y))
                #end for
            #end for
            self._shapely_cache = LineString(sampled_coords)
        #end if
        return self._shapely_cache
    #end def

    def to_str(self) -> str:
        """SVGのパス文字列（M... C...）を生成"""
        if not self._points:
            return ""
        #end if

        segments = [f"M {self._points[0]}"]
        num_segments = (len(self._points) - 1) // 3

        for i in range(num_segments):
            idx = i * 3
            cp1 = self._points[idx + 1]
            cp2 = self._points[idx + 2]
            end = self._points[idx + 3]
            # 三次ベジエコマンド 'C' を使って制御点と終点を記述
            segments.append(f"C {cp1}, {cp2}, {end}")
        #end for

        return " ".join(segments) + " "
    #end def
#end class