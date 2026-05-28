from shapely.geometry import LineString, Point as ShapelyPoint
from shapely.strtree import STRtree

from model.primitive.point import Point
from model.primitive.curve import Curve
from process.converter.converter_base import ConverterBase


class DeleteEdgeConverter(ConverterBase):

    def __init__(self, other_curves: list[Curve], delete_ratio: float = 0.25):
        """
        交差対象となる他の曲線リストと、端部とみなす切り取り比率（閾値）を受け取る。
        """
        self.delete_ratio = delete_ratio
        self.other_curves = other_curves
        self.shapely_lines = []
        
        for c in other_curves:
            line = LineString([(p.x, p.y) for p in c.points])
            self.shapely_lines.append(line)
            
        self.tree = STRtree(self.shapely_lines)

    def convert(self, target_curve: Curve) -> Curve:
        """
        1つのCurveを受け取り、両端から delete_ratio の範囲内にある交差点のうち、
        最も本来の端点に近い位置でトリムした新しいCurveを返す。
        """
        target_line = LineString([(p.x, p.y) for p in target_curve.points])

        # 1. 空間インデックスから交差候補を抽出
        candidate_indices = self.tree.query(target_line)
        
        intersect_points = []
        for idx in candidate_indices:
            other_line = self.shapely_lines[idx]
            
            if other_line.equals(target_line):
                continue
                
            if target_line.intersects(other_line):
                intersection = target_line.intersection(other_line)
                if intersection.is_empty:
                    continue
                
                if intersection.geom_type == 'Point':
                    intersect_points.append(intersection)
                elif intersection.geom_type == 'MultiPoint':
                    intersect_points.extend(list(intersection.geoms))
        #end for

        if not intersect_points:
            return target_curve

        total_length = target_line.length
        
        # 🌟 delete_ratio から「ここより端っこ側だけを見る」という閾値を計算
        start_threshold = total_length * self.delete_ratio
        end_threshold = total_length * (1.0 - self.delete_ratio)

        # 最も端に近い（始点は最小、終点は最大）交差位置を保持する変数
        min_start_dist = None
        max_end_dist = None

        # 2. 閾値の内側（端部領域）にある交差点の中から、最も端に近いものを探索
        for ip in intersect_points:
            dist = target_line.project(ip)

            # 完全に同一の端点はノイズ防止のため除外
            eps = 1e-5
            if dist < eps or dist > total_length - eps:
                continue
            #end if

            # 【始点側】閾値（例: 全長の25%）より手前にある交差点の中から、最も0に近いものを探す
            if dist <= start_threshold:
                if min_start_dist is None or dist < min_start_dist:
                    min_start_dist = dist
                #end if
            # 【終点側】閾値（例: 全長の75%）より後ろにある交差点の中から、最もtotal_lengthに近いものを探す
            elif dist >= end_threshold:
                if max_end_dist is None or dist > max_end_dist:
                    max_end_dist = dist
                #end if
            #end if
        #end for

        # トリム位置の確定（交差点がなかった、または閾値内に無かった場合は元の端点のまま）
        new_start_dist = min_start_dist if min_start_dist is not None else 0.0
        new_end_dist = max_end_dist if max_end_dist is not None else total_length

        if new_start_dist == 0.0 and new_end_dist == total_length:
            return target_curve
        #end if

        # 3. 新しい点列の再構成
        trimmed_coords = []
        
        if new_start_dist > 0.0:
            p_start = target_line.interpolate(new_start_dist)
            trimmed_coords.append((p_start.x, p_start.y))
        #end if

        for p in target_curve.points:
            d = target_line.project(ShapelyPoint(p.x, p.y))
            if new_start_dist < d < new_end_dist:
                trimmed_coords.append((p.x, p.y))
            #end if
        #end for

        if new_end_dist < total_length:
            p_end = target_line.interpolate(new_end_dist)
            trimmed_coords.append((p_end.x, p_end.y))
        #end if

        new_points = [Point(c[0], c[1]) for c in trimmed_coords]
        
        return Curve(
            points=new_points,
            curve_type=target_curve.curve_type,
            is_broad=target_curve.is_broad
        )
    #end
#end class