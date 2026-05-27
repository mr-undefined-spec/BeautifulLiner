import unittest
from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from process.converter.smoother.split_co_converter import SplitCoConverter

# 先ほど綺麗にした本物のデータファクトリ（旧モック）を利用
from test.helper import converter_mocks
from test.helper.converter_mocks import ArcDirection


class TestSplitCoConverter(unittest.TestCase):
    def setUp(self):
        # 3つの異なる向きの円弧（直線近似曲線オブジェクト）を生成
        curve_1 = converter_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0,   0.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)
        curve_2 = converter_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0, 200.0, 180.0, 270.0, 100, ArcDirection.COUNTER_CLOCKWISE)
        curve_3 = converter_mocks.create_mock_linear_approximate_curve_of_arc(100.0, -200.0, 200.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)

        # Curve内部の .points（list[Point]）を結合する
        combined_points = []
        combined_points.extend(curve_1.points)
        combined_points.extend(curve_2.points)
        combined_points.extend(curve_3.points)

        # テスト対象となる「1本の非常に長くて複雑な、変曲点を含む曲線」を生成
        self.long_curve = Curve(
            points=combined_points, 
            curve_type=CurveType.LINEAR_APPROXIMATE
        )
    #end

    def test_convert_to_multiple(self):
        # SplitCoConverterを実行（長い1本の曲線が、適切な変曲点で複数に切り分断される）
        split_curves = SplitCoConverter.convert_to_multiple(self.long_curve)

        # 【検証1】元の3つの円弧に対応して、正しく3本の独立したCurveに分割されているか
        self.assertEqual(len(split_curves), 3)

        # 【検証2】すべての分割された曲線が LINEAR_APPROXIMATE を維持しているか
        for curve in split_curves:
            self.assertEqual(curve.curve_type, CurveType.LINEAR_APPROXIMATE)
        #end for

        # 【検証3】各Curveに含まれる点数がインデックス範囲と完全一致しているか
        self.assertEqual(len(split_curves[0].points), 101)
        self.assertEqual(len(split_curves[1].points), 104)
        self.assertEqual(len(split_curves[2].points), 100)

        # 【検証4】幾何的な連続性の確認（1本目の終点と、2本目の始点が同じ座標を指しているか）
        self.assertAlmostEqual(split_curves[0].points[-1].x, split_curves[1].points[0].x, places=5)
        self.assertAlmostEqual(split_curves[0].points[-1].y, split_curves[1].points[0].y, places=5)
        
        self.assertAlmostEqual(split_curves[1].points[-1].x, split_curves[2].points[0].x, places=5)
        self.assertAlmostEqual(split_curves[1].points[-1].y, split_curves[2].points[0].y, places=5)
    #end
#end class

if __name__ == '__main__':
    unittest.main()