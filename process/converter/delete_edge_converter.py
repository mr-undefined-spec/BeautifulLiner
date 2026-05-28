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
        #end for
            
        self.tree = STRtree(self.shapely_lines)
    #end def

    def convert(self, target_curve: Curve) -> Curve:
        """
        1つのCurveを受け取り、両端から delete_ratio の範囲内にある交差点のうち、
        最も本来の端点に近い位置でトリムし、さらにトポロジー情報(メタデータ)を付与した新しいCurveを返す。
        """
        target_line = LineString([(p.x, p.y) for p in target_curve.points])

        # 1. 空間インデックスから交差候補を抽出
        candidate_indices = self.tree.query(target_line)
        
        # 🌟 後続で相方を特定するため、(ShapelyPoint, other_curve_obj) のタプルで管理する
        intersect_data: list[tuple[ShapelyPoint, Curve]] = []
        
        for idx in candidate_indices:
            other_line = self.shapely_lines[idx]
            other_curve = self.other_curves[idx] # 相方のCurveオブジェクトを取得
            
            if other_line.equals(target_line):
                continue
            #end if
                
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

        # 🌟 後続処理で条件判定に使うため、トリム前の自身のIDを確保
        current_curve_id = id(target_curve)

        if not intersect_data:
            # トリムされなかった場合も、元のIDだけは引き継ぐ
            new_curve = Curve(
                points=[Point(p.x, p.y) for p in target_curve.points],
                curve_type=target_curve.curve_type,
                is_broad=target_curve.is_broad
            )
            new_curve.id_before_trim = current_curve_id
            return new_curve
        #end if

        total_length = target_line.length
        
        # delete_ratio から閾値を計算
        start_threshold = total_length * self.delete_ratio
        end_threshold = total_length * (1.0 - self.delete_ratio)

        # 最も端に近い交差位置と、その原因となった相方のCurveを保持する変数
        min_start_dist = None
        start_partner_curve = None

        max_end_dist = None
        end_partner_curve = None

        # 2. 閾値の内側（端部領域）にある交差点の中から、最も端に近いものを探索
        for ip, other_curve in intersect_data:
            dist = target_line.project(ip)

            # 完全に同一の端点はノイズ防止のため除外
            eps = 1e-5
            if dist < eps or dist > total_length - eps:
                continue
            #end if

            # 【始点側】最も0に近いものを探す
            if dist <= start_threshold:
                if min_start_dist is None or dist < min_start_dist:
                    min_start_dist = dist
                    start_partner_curve = other_curve
                #end if
            # 【終点側】最もtotal_lengthに近いものを探す
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

        if new_start_dist == 0.0 and new_end_dist == total_length:
            # トリム領域内に交差点がなかった場合も、元のIDだけは引き継ぐ
            new_curve = Curve(
                points=[Point(p.x, p.y) for p in target_curve.points],
                curve_type=target_curve.curve_type,
                is_broad=target_curve.is_broad
            )
            new_curve.id_before_trim = current_curve_id
            return new_curve
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
        
        # 4. 新しいCurveオブジェクトの構築とトポロジーメタデータの注入
        new_curve = Curve(
            points=new_points,
            curve_type=target_curve.curve_type,
            is_broad=target_curve.is_broad
        )
        
        # 🌟 後続のThicken判定で相互参照できるように各種メタデータを注入
        new_curve.id_before_trim = current_curve_id
        new_curve.start_trimmed_by = id(start_partner_curve) if start_partner_curve is not None else None
        new_curve.end_trimmed_by = id(end_partner_curve) if end_partner_curve is not None else None
        
        return new_curve
    #end
#end class