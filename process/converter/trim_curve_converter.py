import math
from shapely.geometry import LineString, Point as ShapelyPoint
from shapely.strtree import STRtree

from model.primitive.point import Point
from model.primitive.curve import Curve
from process.converter.curve_list_converter_base import CurveListConverterBase


class TrimCurveConverter(CurveListConverterBase):
    """入力された曲線のリスト内で相互に交差判定を行い、
    各曲線の端部領域（delete_ratio）にある交差点でトリム（カット）するコンバーター。
    後続の肉付け処理等のため、トリム前IDや交差相手のIDといったトポロジーメタデータを注入する。
    """

    def __init__(self, delete_ratio: float = 0.25):
        """
        :param delete_ratio: 各曲線の端部とみなして切り取りを許容する長さの比率（閾値）
        """
        self.delete_ratio = delete_ratio
    #end def

    def convert(self, curves: list[Curve]) -> list[Curve]:
        """受け取ったすべての曲線間で交差判定を行い、トリム処理を施した新しい曲線のリストを返す。"""
        if not curves:
            return []
        #end if

        # 1. 空間インデックス（STRtree）の一括構築
        shapely_lines = []
        for c in curves:
            line = LineString([(p.x, p.y) for p in c.points])
            shapely_lines.append(line)
        #end for
            
        tree = STRtree(shapely_lines)
        output_curves = []

        # 2. 各曲線のトリム走査
        for target_idx, target_curve in enumerate(curves):
            target_line = shapely_lines[target_idx]
            current_curve_id = id(target_curve)

            # 空間インデックスから交差候補を抽出
            candidate_indices = tree.query(target_line)
            
            # (ShapelyPoint, 交差相手の元のCurveオブジェクト) のタプルで収集
            intersect_data: list[tuple[ShapelyPoint, Curve]] = []
            
            for idx in candidate_indices:
                if idx == target_idx:
                    continue 
                #end if

                other_line = shapely_lines[idx]
                other_curve = curves[idx]
                
                if target_line.intersects(other_line):
                    intersection = target_line.intersection(other_line)
                    if intersection.is_empty:
                        continue
                    #end if
                        
                    if intersection.geom_type == 'Point':
                        intersect_data.append((intersection, other_curve))
                    elif intersection.geom_type == 'MultiPoint':
                        for geom in intersection.geoms:
                            intersect_data.append((geom, other_curve))
                        #end for
                    #end if
                #end if
            #end for

            # 交差点がない場合は元のIDを引き継いでそのまま複製
            if not intersect_data:
                new_curve = Curve(
                    points=[Point(p.x, p.y) for p in target_curve.points],
                    curve_type=target_curve.curve_type,
                    is_broad=target_curve.is_broad
                )
                new_curve.id_before_trim = current_curve_id
                output_curves.append(new_curve)
                continue
            #end if

            # 3. 閾値の内側（端部領域）にある交差点の中から、最も端に近いものを探索
            total_length = target_line.length
            start_threshold = total_length * self.delete_ratio
            end_threshold = total_length * (1.0 - self.delete_ratio)

            min_start_dist = None
            start_partner_curve = None

            max_end_dist = None
            end_partner_curve = None

            for ip, other_curve in intersect_data:
                dist = target_line.project(ip)

                # 完全に同一の端点はノイズ防止のため除外
                eps = 1e-5
                if dist < eps or dist > total_length - eps:
                    continue
                #end if

                # 【始点側】最も0に近いものを探索
                if dist <= start_threshold:
                    if min_start_dist is None or dist < min_start_dist:
                        min_start_dist = dist
                        start_partner_curve = other_curve
                    #end if
                # 【終点側】最もtotal_lengthに近いものを探索
                elif dist >= end_threshold:
                    if max_end_dist is None or dist > max_end_dist:
                        max_end_dist = dist
                        end_partner_curve = other_curve
                    #end if
                #end if
            #end for

            # トリム位置の確定
            new_start_dist = min_start_dist if min_start_dist is not None else 0.0
            new_end_dist = max_end_dist if max_end_dist is not None else total_length

            # トリム領域内に交差点がなかった場合
            if new_start_dist == 0.0 and new_end_dist == total_length:
                new_curve = Curve(
                    points=[Point(p.x, p.y) for p in target_curve.points],
                    curve_type=target_curve.curve_type,
                    is_broad=target_curve.is_broad
                )
                new_curve.id_before_trim = current_curve_id
                output_curves.append(new_curve)
                continue
            #end if

            # 4. トリム座標による点列の再構成
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
            
            # 5. 新しいCurveオブジェクトの構築とトポロジーメタデータの注入
            new_curve = Curve(
                points=new_points,
                curve_type=target_curve.curve_type,
                is_broad=target_curve.is_broad
            )
            
            new_curve.id_before_trim = current_curve_id
            new_curve.start_trimmed_by = id(start_partner_curve) if start_partner_curve is not None else None
            new_curve.end_trimmed_by = id(end_partner_curve) if end_partner_curve is not None else None
            
            output_curves.append(new_curve)
        #end for

        return output_curves
    #end def
#end class