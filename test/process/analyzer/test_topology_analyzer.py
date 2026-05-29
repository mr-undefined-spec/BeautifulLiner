import unittest
from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from process.analyzer.topology_analyzer import TopologyAnalyzer


class TestTopologyAnalyzer(unittest.TestCase):

    def test_analyze_isolated_curve(self):
        """交差相手のない孤立した曲線は、両端とも細（False）と判定されること。"""
        curve = Curve(
            points=[Point(0.0, 0.0), Point(40.0, 0.0)],
            curve_type=CurveType.LINEAR_APPROXIMATE
        )

        topo_map = TopologyAnalyzer.analyze([curve])

        self.assertIn(id(curve), topo_map)
        topo = topo_map[id(curve)]
        self.assertFalse(topo.start_is_thick)
        self.assertFalse(topo.end_is_thick)
        self.assertIsNone(topo.start_partner)
        self.assertIsNone(topo.end_partner)
    #end def

    def test_analyze_t_junction(self):
        """相手の曲線のボディ（途中）に刺さっている場合、正しく太（True）と判定されること。"""
        curve_roof = Curve(
            points=[Point(0.0, 50.0), Point(100.0, 50.0)],
            curve_type=CurveType.LINEAR_APPROXIMATE
        )
        curve_roof.id_before_trim = 999

        curve_pillar = Curve(
            points=[Point(50.0, 50.0), Point(50.0, 0.0)],
            curve_type=CurveType.LINEAR_APPROXIMATE
        )
        curve_pillar.start_trimmed_by = 999

        topo_map = TopologyAnalyzer.analyze([curve_roof, curve_pillar])

        topo_pillar = topo_map[id(curve_pillar)]
        self.assertTrue(topo_pillar.start_is_thick)
        self.assertFalse(topo_pillar.end_is_thick)
        self.assertEqual(id(topo_pillar.start_partner), id(curve_roof))
        self.assertAlmostEqual(topo_pillar.start_partner_dist, 50.0)
    #end def

    def test_analyze_cross_junction_at_extreme_edge(self):
        """トリム相手がいても、それが相手の端点付近（マージン外）である場合は細（False）と判定されること。"""
        curve_target = Curve(
            points=[Point(0.0, 0.0), Point(10.0, 0.0)],
            curve_type=CurveType.LINEAR_APPROXIMATE
        )
        curve_target.id_before_trim = 888

        curve_my = Curve(
            points=[Point(0.2, 0.0), Point(0.2, -10.0)],
            curve_type=CurveType.LINEAR_APPROXIMATE
        )
        curve_my.start_trimmed_by = 888

        topo_map = TopologyAnalyzer.analyze([curve_target, curve_my])

        topo_my = topo_map[id(curve_my)]
        self.assertFalse(topo_my.start_is_thick)
    #end def
#end class


if __name__ == '__main__':
    unittest.main()
#end