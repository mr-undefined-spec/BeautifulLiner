import numpy as np
from shapely.geometry import LineString

from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from process.converter.curve_list_converter_base import CurveListConverterBase
from process.analyzer.topology_analyzer import TopologyAnalyzer


class ThickenCurveConverter(CurveListConverterBase):
    """トポロジー解析結果に基づき、各曲線の法線方向へ幅変調（肉付け）を行い、
    閉じられたポリゴン（輪郭線）へと一括変換するコンバーター。
    """

    def __init__(self, base_max_width: float = 4.0):
        """
        :param base_max_width: 肉付け時の最大幅の基準値
        """
        self.base_max_width = base_max_width
    #end def

    def convert(self, curves: list[Curve]) -> list[Curve]:
        """受け取ったすべての単線曲線を解析し、肉付けされた閉じたポリゴン曲線のリストを返す。"""
        if not curves:
            return []
        #end if

        # 1. 共通アナライザーを呼び出してトポロジー診断書（マップ）を一括取得
        topo_map = TopologyAnalyzer.analyze(curves)
        output_curves = []

        # 2. 各曲線の肉付けポリゴン化
        for curve in curves:
            if len(curve.points) < 2:
                continue
            #end if

            coords = [(p.x, p.y) for p in curve.points]
            line = LineString(coords)
            total_length = line.length

            if total_length == 0:
                continue
            #end if

            # 線の長さに応じて最大幅をスケール（短い線は細くする）
            length_scale = min(1.0, total_length / 30.0)
            actual_max_width = self.base_max_width * length_scale

            # 診断書からこの曲線に対応するトポロジーデータを安全に引き出す
            topo = topo_map[id(curve)]
            start_is_thick = topo.start_is_thick
            end_is_thick = topo.end_is_thick

            left_coords = []
            right_coords = []
            accumulated_dist = 0.0

            # 左右への法線オフセット点列を生成
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
                
                t = max(0.0, min(accumulated_dist / total_length, 1.0))

                # 太さ変調のスイッチング（波打たずに綺麗なテーパーを保証）
                if start_is_thick and end_is_thick:
                    # 【太 ー 太】: 一定の太さ
                    base_width_factor = 1.0
                elif start_is_thick and (not end_is_thick):
                    # 【太 ー 細】: 始点から終点へ向かって単調減少
                    base_width_factor = 1.0 - t
                elif (not start_is_thick) and end_is_thick:
                    # 【細 ー 太】: 始点から終点へ向かって単調増加
                    base_width_factor = t
                else:
                    # 【細 ー 細】: 中央が一番膨らむサインカーブ
                    base_width_factor = np.sin(np.pi * t)
                #end if

                current_width = actual_max_width * base_width_factor
                half_w = current_width / 2.0

                # 法線ベクトルの算出
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
                right_coords.insert(0, p_right)  # 右側は逆順に詰めることで反時計回りのポリゴンにする
            #end for

            poly_coords = left_coords + right_coords
            if poly_coords:
                poly_coords.append(poly_coords[0])  # 輪郭の始点と終点を繋いで閉じる
            #end if

            thick_points = [Point(c[0], c[1]) for c in poly_coords]
            thick_curve = Curve(
                points=thick_points,
                curve_type=CurveType.LINEAR_APPROXIMATE,
                is_broad=False
            )

            # 💡 後続のパイプライン（デバッグ色分け用のPostProcessModeなど）が
            # 「このポリゴンがどういう理由で生成されたか」を識別したい場合のための使い捨てカンペ属性
            thick_curve.debug_start_thick = start_is_thick
            thick_curve.debug_end_thick = end_is_thick

            output_curves.append(thick_curve)
        #end for

        return output_curves
    #end def
#end class