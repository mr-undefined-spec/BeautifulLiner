from shapely.geometry import LineString, Point as ShapelyPoint
from shapely.strtree import STRtree

from model.primitive.point import Point
from model.primitive.curve import Curve
from process.converter.converter_base import ConverterBase


class DeleteEdgeConverter(ConverterBase):

    def __init__(self, other_curves: list[Curve], delete_ratio: float = 0.2):
        """
        交差対象となる他の曲線リストと、切り取り比率をコンストラクタで受け取る。
        """
        self.delete_ratio = delete_ratio
        
        # 1. リストと空間インデックスの構築
        self.other_curves = other_curves
        self.shapely_lines = []
        
        for c in other_curves:
            line = LineString([(p.x, p.y) for p in c.points])
            self.shapely_lines.append(line)
            
        # STRtree を構築（内部で高速なR-Treeが作られます）
        self.tree = STRtree(self.shapely_lines)

    def convert(self, target_curve: Curve) -> Curve:
        """
        【原則準拠】1つのCurveを受け取り、端部を切り落とした新しいCurveを返す。
        """
        target_line = LineString([(p.x, p.y) for p in target_curve.points])

        # 2. 空間インデックスから、交差候補の「インデックス（整数のNumPy配列）」を爆速抽出
        candidate_indices = self.tree.query(target_line)
        
        intersect_points = []
        for idx in candidate_indices:
            # インデックスから対応する LineString の実体を取り出す
            other_line = self.shapely_lines[idx]
            
            # 自分自身の幾何構造と完全に一致する場合はスキップ
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

        # 交差点がなければ、何もせず元の曲線をそのまま返す
        if not intersect_points:
            return target_curve

        total_length = target_line.length
        start_threshold = total_length * self.delete_ratio
        end_threshold = total_length * (1.0 - self.delete_ratio)

        new_start_dist = 0.0
        new_end_dist = total_length

        # 3. 各交点が「端部」にあるかチェック
        for ip in intersect_points:
            dist = target_line.project(ip)

            if dist <= start_threshold:
                new_start_dist = max(new_start_dist, dist)
            elif dist >= end_threshold:
                new_end_dist = min(new_end_dist, dist)
            #end if
        #end for

        if new_start_dist == 0.0 and new_end_dist == total_length:
            return target_curve

        # 4. 新しい点列の再構成
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