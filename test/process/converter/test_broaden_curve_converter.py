import unittest
from unittest.mock import patch
import numpy as np

from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from process.analyzer.topology_analyzer import CurveEdgeTopology
from process.converter.broaden_curve_converter import BroadenCurveConverter


class TestBroadenCurveConverter(unittest.TestCase):

    @patch('process.analyzer.topology_analyzer.TopologyAnalyzer.analyze')
    def test_convert_with_mocked_thin_thin_topology(self, mock_analyze):
        """【細ー細】のトポロジー診断書が与えられたとき、両端が幅0に収束するポリゴンが生成されること。"""
        curve = Curve(
            points=[Point(0.0, 0.0), Point(40.0, 0.0)],
            curve_type=CurveType.LINEAR_APPROXIMATE
        )

        fake_topology = CurveEdgeTopology(curve=curve, start_is_thick=False, end_is_thick=False)
        mock_analyze.return_value = {id(curve): fake_topology}

        converter = BroadenCurveConverter(base_max_width=4.0)
        output = converter.convert([curve])

        self.assertEqual(len(output), 1)
        poly_curve = output[0]
        
        self.assertAlmostEqual(poly_curve.points[0].y, 0.0)
        self.assertAlmostEqual(poly_curve.points[-1].y, 0.0)
    #end def

    @patch('process.analyzer.topology_analyzer.TopologyAnalyzer.analyze')
    def test_convert_with_mocked_thick_thin_topology(self, mock_analyze):
        """【太ー細】のトポロジー診断書が与えられたとき、始点から終点へ単調減少するポリゴンが生成されること。"""
        curve = Curve(
            points=[Point(50.0, 100.0), Point(50.0, 60.0)],
            curve_type=CurveType.LINEAR_APPROXIMATE
        )

        fake_topology = CurveEdgeTopology(curve=curve, start_is_thick=True, end_is_thick=False)
        mock_analyze.return_value = {id(curve): fake_topology}

        converter = BroadenCurveConverter(base_max_width=4.0)
        output = converter.convert([curve])

        poly_curve = output[0]

        pt_left_start  = poly_curve.points[0]
        pt_left_end    = poly_curve.points[1]
        pt_right_end   = poly_curve.points[2]
        pt_right_start = poly_curve.points[3]

        self.assertAlmostEqual(pt_left_start.x, 52.0)
        self.assertAlmostEqual(pt_right_start.x, 48.0)
        self.assertAlmostEqual(pt_left_end.x, 50.0)
        self.assertAlmostEqual(pt_right_end.x, 50.0)
    #end def
#end class


if __name__ == '__main__':
    unittest.main()
#end