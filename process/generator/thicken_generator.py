import numpy as np
from shapely.geometry import LineString, Point as ShapelyPoint

from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from model.container.layer import Layer
from model.container.canvas import Canvas


class ThickenGenerator:
    # 🌟 引き続き結果を目視確認できるよう True にしています。
    # 意図通りの形状になったら False に戻してください。
    IS_DEBUG = False

    @staticmethod
    def generate(stroke_canvas: Canvas, base_max_width: float = 4.0) -> Canvas:
        thicken_canvas = Canvas()
        thicken_canvas.set_view_box(stroke_canvas.view_box)

        # 1. 全曲線の「トリム前のID」から「現在のオブジェクト」を引ける辞書
        curve_lookup = {}
        for layer in stroke_canvas:
            for curve in layer:
                if getattr(curve, "id_before_trim", None) is not None:
                    curve_lookup[curve.id_before_trim] = curve
                #end if
            #end for
        #end for

        for stroke_layer in stroke_canvas:
            thicken_layer = Layer(f"{stroke_layer.name}_thick", stroke_layer.color)
            thicken_layer.set_write_options(True, stroke_layer.color, stroke_layer.endpoint_style)
            
            layer_thin_thin = Layer(f"{stroke_layer.name}_debug_thin_thin", "#000000")
            layer_thin_thick = Layer(f"{stroke_layer.name}_debug_thin_thick", "#FFFFFF")
            layer_thick_thick = Layer(f"{stroke_layer.name}_debug_thick_thick", "#800080")

            layer_thin_thin.set_write_options(True, "#000000", stroke_layer.endpoint_style)
            layer_thin_thick.set_write_options(True, "#FFFFFF", stroke_layer.endpoint_style)
            layer_thick_thick.set_write_options(True, "#800080", stroke_layer.endpoint_style)
            
            for curve in stroke_layer:
                if len(curve.points) < 2:
                    continue
                #end if

                coords = [(p.x, p.y) for p in curve.points]
                line = LineString(coords)
                total_length = line.length

                if total_length == 0:
                    continue
                #end if

                length_scale = min(1.0, total_length / 30.0)
                actual_max_width = base_max_width * length_scale

                # 2. トポロジーから「端点が太いか（True）細いか（False）」を判定
                start_is_thick = False
                end_is_thick = False
                edge_margin = 0.05 

                # ─── 始点側の判定 ───
                start_partner_id = getattr(curve, "start_trimmed_by", None)
                if start_partner_id is not None:
                    partner_curve = curve_lookup.get(start_partner_id)
                    if partner_curve is not None:
                        partner_orig_line = LineString([(p.x, p.y) for p in partner_curve.points])
                        my_start_pt = ShapelyPoint(coords[0])
                        partner_dist = partner_orig_line.project(my_start_pt)
                        partner_total_length = partner_orig_line.length
                        if partner_total_length > 0:
                            partner_ratio = partner_dist / partner_total_length
                            if edge_margin < partner_ratio < (1.0 - edge_margin):
                                start_is_thick = True
                            #end if
                        #end if
                    else:
                        start_is_thick = True
                    #end if
                #end if

                # ─── 終点側の判定 ───
                end_partner_id = getattr(curve, "end_trimmed_by", None)
                if end_partner_id is not None:
                    partner_curve = curve_lookup.get(end_partner_id)
                    if partner_curve is not None:
                        partner_orig_line = LineString([(p.x, p.y) for p in partner_curve.points])
                        my_end_pt = ShapelyPoint(coords[-1])
                        partner_dist = partner_orig_line.project(my_end_pt)
                        partner_total_length = partner_orig_line.length
                        if partner_total_length > 0:
                            partner_ratio = partner_dist / partner_total_length
                            if edge_margin < partner_ratio < (1.0 - edge_margin):
                                end_is_thick = True
                            #end if
                        #end if
                    else:
                        end_is_thick = True
                    #end if
                #end if

                # 左右へのオフセット頂点列の生成
                left_coords = []
                right_coords = []
                accumulated_dist = 0.0
                
                for i in range(len(coords)):
                    p_curr = np.array(coords[i])

                    if i == 0:
                        p_next = np.array(coords[i+1])
                        v_dir = p_next - p_curr
                    elif i == len(coords) - 1:
                        p_prev = np.array(coords[i-1])
                        v_dir = p_curr - p_prev
                    else:
                        p_next = np.array(coords[i+1])
                        p_prev = np.array(coords[i-1])
                        v_dir = p_next - p_prev
                    #end if

                    if i > 0:
                        p_prev_exact = np.array(coords[i-1])
                        accumulated_dist += np.linalg.norm(p_curr - p_prev_exact)
                    #end if
                    t = clip(accumulated_dist / total_length, 0.0, 1.0)

                    # 🌟 3. 新しい太さ変調ロジック（波打たずにシンプルに変形）
                    if start_is_thick and end_is_thick:
                        # 【太 ー 太】: 最初から最後までずっと100%（一定の太さ）
                        base_width_factor = 1.0

                    elif start_is_thick and (not end_is_thick):
                        # 【太 ー 細】: 始点(t=0)の1.0から、終点(t=1)の0.0へ向かって単調減少
                        base_width_factor = 1.0 - t

                    elif (not start_is_thick) and end_is_thick:
                        # 【細 ー 太】: 始点(t=0)の0.0から、終点(t=1)の1.0へ向かって単調増加
                        base_width_factor = t

                    else:
                        # 【細 ー 細】: 従来通り、中央が一番膨らむサインカーブ
                        base_width_factor = np.sin(np.pi * t)
                    #end if

                    current_width = actual_max_width * base_width_factor
                    half_w = current_width / 2.0

                    # 法線ベクトル化
                    norm_dir = np.linalg.norm(v_dir)
                    if norm_dir > 0:
                        v_dir_unit = v_dir / norm_dir
                        v_normal = np.array([-v_dir_unit[1], v_dir_unit[0]])
                    else:
                        v_normal = np.array([0.0, 0.0])
                    #end if

                    p_left = p_curr + v_normal * half_w
                    p_right = p_curr - v_normal * half_w

                    left_coords.append(p_left)
                    right_coords.insert(0, p_right)
                #end for

                poly_coords = left_coords + right_coords
                if poly_coords:
                    poly_coords.append(poly_coords[0])
                #end if

                thick_points = [Point(c[0], c[1]) for c in poly_coords]
                thick_curve = Curve(
                    points=thick_points,
                    curve_type=CurveType.LINEAR_APPROXIMATE,
                    is_broad=False
                )

                # 4. 【デバッグ振り分け】
                if ThickenGenerator.IS_DEBUG:
                    if (not start_is_thick) and (not end_is_thick):
                        layer_thin_thin.append(thick_curve)     # 細 ー 細 (黒)
                    elif start_is_thick and end_is_thick:
                        layer_thick_thick.append(thick_curve)   # 太 ー 太 (紫)
                    else:
                        layer_thin_thick.append(thick_curve)    # 細 ー 太 / 太 ー 細 (白)
                    #end if
                else:
                    thicken_layer.append(thick_curve)
                #end if
            #end for

            if not ThickenGenerator.IS_DEBUG:
                thicken_canvas.append(thicken_layer)
            else:
                if len(layer_thin_thin) > 0: thicken_canvas.append(layer_thin_thin)
                if len(layer_thin_thick) > 0: thicken_canvas.append(layer_thin_thick)
                if len(layer_thick_thick) > 0: thicken_canvas.append(layer_thick_thick)
            #end if
        #end for

        return thicken_canvas
    #end

def clip(n, smallest, largest):
    return max(smallest, min(n, largest))
#end