import unittest
import math

from model.primitive.curve import Curve
from process.converter.delete_edge_converter import DeleteEdgeConverter
from test.helper.converter_mocks import create_mock_linear_approximate_curve_of_arc, ArcDirection


class TestDeleteEdgeConverter(unittest.TestCase):

    def test_convert(self):
        # 1. 幾何学的に交差する2つの円弧を生成
        curve_1 = create_mock_linear_approximate_curve_of_arc(
            radius=100.0, center_x=0.0, center_y=0.0,
            start_angle=0.0, end_angle=90.0, num_divisions=100,
            arc_direction=ArcDirection.CLOCKWISE
        )
        
        curve_2 = create_mock_linear_approximate_curve_of_arc(
            radius=100.0, center_x=100.0, center_y=0.0,
            start_angle=90.0, end_angle=180.0, num_divisions=100,
            arc_direction=ArcDirection.CLOCKWISE
        )

        original_point_count = len(curve_1.points)

        # 2. 原則に則り、コンストラクタに交差対象（curve_2）を渡してコンバータを生成
        converter = DeleteEdgeConverter(other_curves=[curve_2], delete_ratio=0.5)
        
        # 3. 1対1（Curveを受け取りCurveを返す）の原則でコンバートを実行
        trimmed_curve = converter.convert(curve_1)

        # 4. 検証
        self.assertIsInstance(trimmed_curve, Curve)
        self.assertEqual(trimmed_curve.curve_type, curve_1.curve_type)
        self.assertLess(len(trimmed_curve.points), original_point_count)

        # 交点座標 (50.0, 50.0 * sqrt(3)) 付近になっていることを検証
        last_point = trimmed_curve.points[-1]
        self.assertAlmostEqual(last_point.x, 50.0, places=1)
        self.assertAlmostEqual(last_point.y, 50.0 * math.sqrt(3.0), places=1)
    # end def
# end class

if __name__ == '__main__':
    unittest.main()