import numpy as np
from shapely.geometry import LineString, Point as ShapelyPoint

from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from process.analyzer.topology_analyzer import TopologyAnalyzer, CurveEdgeTopology


class InkBleedEffector:
    """線画の結合部（交差点）を検出し、インクの滲み・溜まり（環境光遮蔽）を表現する
    追加のポリゴン形状（エフェクトパーツ）を生成するエフェクター。
    """

    def __init__(self, bleed_size: float = 2.0):
        """
        :param bleed_size: インク溜まりのサイズ（三角形の広がりの基準値）
        """
        self.bleed_size = bleed_size
    #end def

    def apply(self, curves: list[Curve]) -> list[Curve]:
        """受け取った単線リスト全体のトポロジーを解析し、
        結合部の鋭角側に発生させるインク溜まりポリゴン（Curve）のリストを新規に生成して返す。
        """
        if not curves:
            return []
        #end if

        # 1. 共通アナライザーの診断書（マップ）を取得
        topo_map = TopologyAnalyzer.analyze(curves)
        bleed_curves = []

        # 2. 診断書を走査してインク溜まりをハント
        for curve in curves:
            if len(curve.points) < 2:
                continue
            #end if

            topo = topo_map[id(curve)]

            # ─── 始点側のインク溜まり生成 ───
            if topo.start_is_thick and topo.start_partner is not None:
                p0 = curve.points[0]
                p1_next = curve.points[1]
                poly_pts = self._build_bleed_triangle(p0, p1_next, topo.start_partner, topo.start_partner_dist)
                if poly_pts:
                    bleed_curves.append(self._create_poly_curve(poly_pts))
                #end if
            #end if

            # ─── 終点側のインク溜まり生成 ───
            if topo.end_is_thick and topo.end_partner is not None:
                p0 = curve.points[-1]
                p1_next = curve.points[-2]  # 終点から内側へ向かうベクトル用
                poly_pts = self._build_bleed_triangle(p0, p1_next, topo.end_partner, topo.end_partner_dist)
                if poly_pts:
                    bleed_curves.append(self._create_poly_curve(poly_pts))
                #end if
            #end if
        #end for

        return bleed_curves
    #end def

    # -------------------------------------------------------------------------
    # 幾何エフェクト計算ヘルパー
    # -------------------------------------------------------------------------

    def _build_bleed_triangle(self, p0_node: Point, p1_inner: Point, partner_curve: Curve, partner_dist: float) -> list[Point] | None:
        """交差点、自身の内側点、衝突相手の線情報から、鋭角側を埋めるインク溜まり点列を計算する。"""
        np_p0 = np.array([p0_node.x, p0_node.y])

        # 自身側の方向ベクトル
        v_target = np.array([p1_inner.x - p0_node.x, p1_inner.y - p0_node.y])
        
        # 相手側の接線ベクトルを算出
        partner_line = LineString([(p.x, p.y) for p in partner_curve.points])
        v_base = self._calculate_tangent(partner_curve, partner_line, partner_dist)

        norm_t = np.linalg.norm(v_target)
        norm_b = np.linalg.norm(v_base)
        if norm_t == 0 or norm_b == 0:
            return None
        #end if

        u_target = v_target / norm_t
        u_base = v_base / norm_b

        # なす角から鋭角の向きをジャッジ
        cos_theta = np.clip(np.dot(u_target, u_base), -1.0, 1.0)
        angle_deg = np.degrees(np.arccos(cos_theta))

        direction_base = u_base if angle_deg <= 90.0 else -u_base

        # インク溜まりの頂点を展開
        p1 = np_p0 + u_target * self.bleed_size
        p2 = np_p0 + direction_base * self.bleed_size

        return [
            Point(np_p0[0], np_p0[1]),
            Point(p1[0], p1[1]),
            Point(p2[0], p2[1]),
            Point(np_p0[0], np_p0[1])  # 閉じる
        ]
    #end def

    @staticmethod
    def _calculate_tangent(curve: Curve, line: LineString, dist: float) -> np.ndarray:
        """指定された投影距離が属する線分セグメントを探索し、その方向ベクトルを返す。"""
        dists = [line.project(ShapelyPoint(p.x, p.y)) for p in curve.points]
        idx = 0
        for i in range(len(dists) - 1):
            if dists[i] <= dist <= dists[i+1]:
                idx = i
                break
            #end if
        #end for
        p1 = curve.points[idx]
        p2 = curve.points[idx + 1]
        return np.array([p2.x - p1.x, p2.y - p1.y])
    #end def

    @staticmethod
    def _create_poly_curve(points: list[Point]) -> Curve:
        return Curve(
            points=points,
            curve_type=CurveType.LINEAR_APPROXIMATE,
            is_broad=False
        )
    #end def
#end class