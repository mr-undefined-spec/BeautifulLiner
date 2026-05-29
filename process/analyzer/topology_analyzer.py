from dataclasses import dataclass
from shapely.geometry import LineString, Point as ShapelyPoint
from model.primitive.curve import Curve


@dataclass
class CurveEdgeTopology:
    """単一の曲線における、両端点の接続状態（トポロジー）を保持するデータ構造。"""
    curve: Curve
    start_is_thick: bool = False
    end_is_thick: bool = False
    start_partner: Curve | None = None
    end_partner: Curve | None = None
    start_partner_dist: float = 0.0
    end_partner_dist: float = 0.0
#end class


class TopologyAnalyzer:
    """キャンバスあるいはレイヤー内の曲線群の相互接続関係を診断・解析するアナライザー。"""

    @staticmethod
    def analyze(curves: list[Curve], edge_margin: float = 0.05) -> dict[int, CurveEdgeTopology]:
        """全曲線のリストを受け取り、各曲線のオブジェクトID (id(curve)) をキーとした
        トポロジー解析結果のマップを返却する。
        """
        # 1. 検索用辞書のビルド（トリム前IDからの逆引き用）
        curve_lookup = {}
        result_map: dict[int, CurveEdgeTopology] = {}

        for curve in curves:
            result_map[id(curve)] = CurveEdgeTopology(curve=curve)
            if getattr(curve, "id_before_trim", None) is not None:
                curve_lookup[curve.id_before_trim] = curve
            #end if
        #end for

        # 2. 各曲線の端部結線判定（相手のボディに刺さっているか）
        for curve in curves:
            if len(curve.points) < 2:
                continue
            #end if

            topo = result_map[id(curve)]
            coords = [(p.x, p.y) for p in curve.points]

            # ─── 始点側の判定 ───
            start_partner_id = getattr(curve, "start_trimmed_by", None)
            if start_partner_id is not None:
                partner_curve = curve_lookup.get(start_partner_id)
                if partner_curve is not None and len(partner_curve.points) >= 2:
                    partner_line = LineString([(p.x, p.y) for p in partner_curve.points])
                    my_start_pt = ShapelyPoint(coords[0])
                    dist = partner_line.project(my_start_pt)
                    total_len = partner_line.length

                    topo.start_partner = partner_curve
                    topo.start_partner_dist = dist

                    if total_len > 0:
                        ratio = dist / total_len
                        if edge_margin < ratio < (1.0 - edge_margin):
                            topo.start_is_thick = True
                        #end if
                    #end if
                else:
                    topo.start_is_thick = True
                #end if
            #end if

            # ─── 終点側の判定 ───
            end_partner_id = getattr(curve, "end_trimmed_by", None)
            if end_partner_id is not None:
                partner_curve = curve_lookup.get(end_partner_id)
                if partner_curve is not None and len(partner_curve.points) >= 2:
                    partner_line = LineString([(p.x, p.y) for p in partner_curve.points])
                    my_end_pt = ShapelyPoint(coords[-1])
                    dist = partner_line.project(my_end_pt)
                    total_len = partner_line.length

                    topo.end_partner = partner_curve
                    topo.end_partner_dist = dist

                    if total_len > 0:
                        ratio = dist / total_len
                        if edge_margin < ratio < (1.0 - edge_margin):
                            topo.end_is_thick = True
                        #end if
                    #end if
                else:
                    topo.end_is_thick = True
                #end if
            #end if
        #end for

        return result_map
    #end def
#end class