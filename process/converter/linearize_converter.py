import numpy as np
from shapely.geometry import LineString

from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from process.converter.converter_base import ConverterBase


class LinearizeConverter(ConverterBase):

    @staticmethod
    def convert(bezier_curve: Curve) -> Curve:
        """3次ベジェ曲線（マルチセグメント対応）を高精度な直線近似（POLYLINE）曲線に変換する"""
        src_points = bezier_curve.points
        segment_count = (len(src_points) - 1) // 3
        
        all_linearized_points = []
        
        # 分割数（サンプリング数）。旧コードの精度に合わせるか、十分滑らかな数を指定
        # ここでは1つのセグメントあたり32分割（33点）とします
        num_steps = 32
        t = np.linspace(0.0, 1.0, num_steps + 1)
        
        # 3次ベジェ曲線のバーンスタイン基底関数の係数を一括計算
        # B(t) = (1-t)^3 * P0 + 3(1-t)^2 * t * P1 + 3(1-t) * t^2 * P2 + t^3 * P3
        b0 = (1.0 - t) ** 3
        b1 = 3.0 * ((1.0 - t) ** 2) * t
        b2 = 3.0 * (1.0 - t) * (t ** 2)
        b3 = t ** 3

        for s in range(segment_count):
            idx = s * 3
            p0, p1, p2, p3 = src_points[idx:idx+4]

            # NumPyのブロードキャストでX座標、Y座標を一括計算（高速）
            xs = b0 * p0.x + b1 * p1.x + b2 * p2.x + b3 * p3.x
            ys = b0 * p0.y + b1 * p1.y + b2 * p2.y + b3 * p3.y

            # ShapelyのLineStringオブジェクトを生成して幾何構造を確定
            # (将来的にShapelyの幾何判定やオフセット等にそのまま流用可能にするため)
            shapely_line = LineString(np.column_stack((xs, ys)))
            coords = list(shapely_line.coords)

            if s == 0:
                all_linearized_points.extend([Point(c[0], c[1]) for c in coords])
            else:
                # 繋ぎ目の重複（前の終点＝次の始点）を排除
                all_linearized_points.extend([Point(c[0], c[1]) for c in coords[1:]])
            #end if
        #end for

        return Curve(
            points=all_linearized_points,
            curve_type=CurveType.LINEAR_APPROXIMATE,
            is_broad=bezier_curve.is_broad
        )
    #end
#end class