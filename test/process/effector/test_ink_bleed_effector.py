import unittest
from unittest.mock import patch
import numpy as np

from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from process.analyzer.topology_analyzer import CurveEdgeTopology
from process.effector.ink_bleed_effector import InkBleedEffector


class TestInkBleedEffector(unittest.TestCase):

    @patch('process.analyzer.topology_analyzer.TopologyAnalyzer.analyze')
    def test_apply_no_bleed_when_thin(self, mock_analyze):
        """端点が「細」判定（結合していない）の場合は、インク溜まりポリゴンが一切生成されないこと。"""
        curve = Curve(points=[Point(0.0, 0.0), Point(50.0, 0.0)], curve_type=CurveType.LINEAR_APPROXIMATE)
        
        # 結合なし（すべてFalse）のモック診断書
        fake_topology = CurveEdgeTopology(curve=curve, start_is_thick=False, end_is_thick=False)
        mock_analyze.return_value = {id(curve): fake_topology}

        effector = InkBleedEffector(bleed_size=5.0)
        bleed_parts = effector.apply([curve])

        self.assertEqual(len(bleed_parts), 0, "結合のない場所にインクが滲んではならない")
    #end def

    @patch('process.analyzer.topology_analyzer.TopologyAnalyzer.analyze')
    def test_apply_sharp_angle_bleed_geometry(self, mock_analyze):
        """【太ー細】かつ相手が水平線、自身が斜め45度で刺さる鋭角結合のとき、
        鋭角側（なす角が90度以下になる象限）へ正しくインク溜まりポリゴンが生成されること。
        """
        # 相手の線（水平 X:0->100, Y:50）
        curve_roof = Curve(points=[Point(0.0, 50.0), Point(100.0, 50.0)], curve_type=CurveType.LINEAR_APPROXIMATE)
        
        # 自身の線（X=50, Y=50 の位置に右上から45度で刺さる。内側点は X=60, Y=60）
        curve_pillar = Curve(points=[Point(50.0, 50.0), Point(60.0, 60.0)], curve_type=CurveType.LINEAR_APPROXIMATE)

        # 始点が太、相手はroof、投影距離は50.0 という偽の診断書を注入
        fake_topology = CurveEdgeTopology(
            curve=curve_pillar,
            start_is_thick=True,
            end_is_thick=False,
            start_partner=curve_roof,
            start_partner_dist=50.0
        )
        mock_analyze.return_value = {id(curve_pillar): fake_topology}

        # サイズ10でエフェクト適用
        effector = InkBleedEffector(bleed_size=10.0)
        bleed_parts = effector.apply([curve_pillar])

        self.assertEqual(len(bleed_parts), 1)
        poly = bleed_parts[0]

        # 頂点の検証: [交差点p0, 自身側へ伸びた点p1, 相手の鋭角側へ伸びた点p2, 閉じ点p0]
        # 自身側ベクトルは (10, 10) の単位化 ➡️ (cos45, sin45) * 10 ≒ (7.07, 7.07)
        # 相手側ベクトルは右向き (1, 0) とのなす角が45度（鋭角）なので、direction_baseは右向きプラス。
        # したがって p2 は (50 + 10, 50) = (60.0, 50.0) になるべき。
        
        p0 = poly.points[0]
        p1 = poly.points[1]
        p2 = poly.points[2]

        self.assertAlmostEqual(p0.x, 50.0)
        self.assertAlmostEqual(p0.y, 50.0)
        
        # 自身側の広がり
        self.assertAlmostEqual(p1.x, 50.0 + 10.0 * (1.0 / np.sqrt(2)))
        self.assertAlmostEqual(p1.y, 50.0 + 10.0 * (1.0 / np.sqrt(2)))
        
        # 相手（鋭角）側の広がり
        self.assertAlmostEqual(p2.x, 60.0)
        self.assertAlmostEqual(p2.y, 50.0)
    #end def
#end class


if __name__ == '__main__':
    unittest.main()
#end