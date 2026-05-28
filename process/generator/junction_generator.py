import numpy as np
from dataclasses import dataclass
from shapely.geometry import LineString, Point as ShapelyPoint

from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from model.container.layer import Layer
from model.container.canvas import Canvas


@dataclass
class JunctionData:
    """三叉路（接合部）の解析・生成用データを保持する構造体"""
    intersection_point: Point  # ぶつかっている側の太い端点座標
    target_curve: Curve        # ぶつかっている側の曲線（端点が太い線）
    base_curve: Curve          # ぶつかられている側の曲線（相手の状態は不問）
    angle_rad: float           # 2つの曲線のなす角（ラジアン）
    angle_deg: float           # 2つの曲線のなす角（度数法: 0.0 〜 180.0）


class JunctionGenerator:
    """
    肉付け前のトポロジーメタデータを利用し、三叉路（Junction）を正確にハントして
    鋭角側に赤い三角形ポリゴンを単独で生成するジェネレータークラス。
    """

    @staticmethod
    def generate(stroke_canvas: Canvas, triangle_size: float = 2000.0) -> Canvas:
        """
        肉付け前のCanvasを受け取り、検出されたすべての三叉路の鋭角側に
        赤い三角形ポリゴン（単独レイヤー）のみを格納したCanvasを返す。
        """
        # 1. 全曲線の「トリム前のID」から「現在のオブジェクト」を引ける辞書をビルド（ThickenGeneratorと完全同期）
        curve_lookup = {}
        all_curves = []
        for layer in stroke_canvas:
            for curve in layer:
                all_curves.append(curve)
                if getattr(curve, "id_before_trim", None) is not None:
                    curve_lookup[curve.id_before_trim] = curve
                #end if
            #end for
        #end for

        # 2. 三叉路トポロジーの解析
        junctions = JunctionGenerator._analyze_junctions_with_topology(all_curves, curve_lookup)

        # 3. 三叉路オブジェクト（赤い三角形）のみを格納する独立したCanvasを作成
        junction_canvas = Canvas()
        junction_canvas.set_view_box(stroke_canvas.view_box)

        junction_layer = Layer("junction_occlusion", "#FF0000")
        junction_layer.set_write_options(True, "#FF0000")

        for j in junctions:
            poly_points = JunctionGenerator._build_sharp_triangle(j, triangle_size)
            if poly_points is None:
                continue
            #end if

            triangle_curve = Curve(
                points=poly_points,
                curve_type=CurveType.LINEAR_APPROXIMATE,
                is_broad=False
            )
            junction_layer.append(triangle_curve)
        #end for

        if len(junction_layer) > 0:
            junction_canvas.append(junction_layer)
        #end if

        return junction_canvas
    #end def

    # -------------------------------------------------------------------------
    # 内部トポロジー解析ロジック
    # -------------------------------------------------------------------------

    @staticmethod
    def _analyze_junctions_with_topology(curves: list[Curve], curve_lookup: dict) -> list[JunctionData]:
        """
        ThickenGeneratorと同じ条件式で「片側が太い端点（トリム相手がもう一方の線の途中にある）」を確実に拾う
        """
        junctions = []
        edge_margin = 0.05

        for c_a in curves:
            if len(c_a.points) < 2:
                continue
            #end if

            # ─── 始点側がトリムされているか ───
            start_partner_id = getattr(c_a, "start_trimmed_by", None)
            if start_partner_id is not None:
                c_b = curve_lookup.get(start_partner_id)
                if c_b is not None and len(c_b.points) >= 2:
                    # 相手の線の「途中」に刺さっているか判定（ThickenGeneratorの start_is_thick 条件と完全一致）
                    b_line = LineString([(p.x, p.y) for p in c_b.points])
                    pt_intersect = c_a.points[0]
                    sh_pt = ShapelyPoint(pt_intersect.x, pt_intersect.y)
                    
                    partner_dist = b_line.project(sh_pt)
                    partner_total_length = b_line.length
                    
                    if partner_total_length > 0:
                        partner_ratio = partner_dist / partner_total_length
                        # 端点 margin から外れた「途中（ボディ）」に刺さっている ＝ 綺麗な三叉路
                        if edge_margin < partner_ratio < (1.0 - edge_margin):
                            # ベクトル・角度の算出
                            vec_a = np.array([c_a.points[1].x - pt_intersect.x, c_a.points[1].y - pt_intersect.y])
                            vec_b = JunctionGenerator._calculate_base_tangent(c_b, b_line, partner_dist)
                            
                            j_data = JunctionGenerator._create_junction_data(pt_intersect, c_a, c_b, vec_a, vec_b)
                            if j_data is not None:
                                junctions.append(j_data)
                            #end if
                        #end if
                    #end if
                #end if
            #end if

            # ─── 終点側がトリムされているか ───
            end_partner_id = getattr(c_a, "end_trimmed_by", None)
            if end_partner_id is not None:
                c_b = curve_lookup.get(end_partner_id)
                if c_b is not None and len(c_b.points) >= 2:
                    # 相手の線の「途中」に刺さっているか判定
                    b_line = LineString([(p.x, p.y) for p in c_b.points])
                    pt_intersect = c_a.points[-1]
                    sh_pt = ShapelyPoint(pt_intersect.x, pt_intersect.y)
                    
                    partner_dist = b_line.project(sh_pt)
                    partner_total_length = b_line.length
                    
                    if partner_total_length > 0:
                        partner_ratio = partner_dist / partner_total_length
                        if edge_margin < partner_ratio < (1.0 - edge_margin):
                            # ベクトル・角度の算出
                            vec_a = np.array([c_a.points[-2].x - pt_intersect.x, c_a.points[-2].y - pt_intersect.y])
                            vec_b = JunctionGenerator._calculate_base_tangent(c_b, b_line, partner_dist)
                            
                            j_data = JunctionGenerator._create_junction_data(pt_intersect, c_a, c_b, vec_a, vec_b)
                            if j_data is not None:
                                junctions.append(j_data)
                            #end if
                        #end if
                    #end if
                #end if
            #end if
        #end for

        return junctions
    #end def

    # -------------------------------------------------------------------------
    # 幾何ヘルパー
    # -------------------------------------------------------------------------

    @staticmethod
    def _calculate_base_tangent(c_b: Curve, b_line: LineString, dist: float) -> np.ndarray:
        dists = [b_line.project(ShapelyPoint(p.x, p.y)) for p in c_b.points]
        idx = 0
        for i in range(len(dists) - 1):
            if dists[i] <= dist <= dists[i+1]:
                idx = i
                break
            #end if
        #end for
        p1 = c_b.points[idx]
        p2 = c_b.points[idx + 1]
        return np.array([p2.x - p1.x, p2.y - p1.y])
    #end def

    @staticmethod
    def _create_junction_data(pt: Point, c_a: Curve, c_b: Curve, vec_a: np.ndarray, vec_b: np.ndarray) -> JunctionData | None:
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)

        if norm_a == 0 or norm_b == 0:
            return None
        #end if

        cos_theta = np.dot(vec_a, vec_b) / (norm_a * norm_b)
        cos_theta = np.clip(cos_theta, -1.0, 1.0)
        
        angle_rad = np.arccos(cos_theta)
        angle_deg = np.degrees(angle_rad)

        return JunctionData(
            intersection_point=pt,
            target_curve=c_a,
            base_curve=c_b,
            angle_rad=angle_rad,
            angle_deg=angle_deg
        )
    #end def

    @staticmethod
    def _build_sharp_triangle(j: JunctionData, size: float) -> list[Point] | None:
        p0 = np.array([j.intersection_point.x, j.intersection_point.y])
        
        # target_curve側の方向ベクトル
        if id(j.target_curve.points[0]) == id(j.intersection_point):
            v_target = np.array([j.target_curve.points[1].x - p0[0], j.target_curve.points[1].y - p0[1]])
        else:
            v_target = np.array([j.target_curve.points[-2].x - p0[0], j.target_curve.points[-2].y - p0[1]])
        #end if
        
        b_line = LineString([(p.x, p.y) for p in j.base_curve.points])
        v_base = JunctionGenerator._calculate_base_tangent(j.base_curve, b_line, b_line.project(ShapelyPoint(p0[0], p0[1])))
        
        norm_t = np.linalg.norm(v_target)
        norm_b = np.linalg.norm(v_base)
        if norm_t == 0 or norm_b == 0: return None
        
        u_target = v_target / norm_t
        u_base = v_base / norm_b

        # 鋭角方向を割り出す
        if j.angle_deg <= 90.0:
            direction_base = u_base
        else:
            direction_base = -u_base
        #end if

        p1 = p0 + u_target * size
        p2 = p0 + direction_base * size

        return [
            Point(p0[0], p0[1]),
            Point(p1[0], p1[1]),
            Point(p2[0], p2[1]),
            Point(p0[0], p0[1])
        ]
    #end def
#end class