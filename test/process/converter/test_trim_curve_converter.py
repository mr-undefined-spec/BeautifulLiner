import unittest
import math

from model.primitive.curve import Curve
from process.converter.trim_curve_converter import TrimCurveConverter
from test.helper.converter_mocks import create_mock_linear_approximate_curve_of_arc, ArcDirection


class TestTrimCurveConverter(unittest.TestCase):

    def test_convert_mutual_intersection(self):
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

        original_point_count_1 = len(curve_1.points)
        original_id_1 = id(curve_1)
        original_id_2 = id(curve_2)

        # 2. コンバーターを初期化
        converter = TrimCurveConverter(delete_ratio=0.5)
        
        # 3. 一括変換へ投入
        input_curves = [curve_1, curve_2]
        output_curves = converter.convert(input_curves)

        # 4. 検証
        self.assertEqual(len(output_curves), 2)
        trimmed_curve_1 = output_curves[0]
        trimmed_curve_2 = output_curves[1]

        self.assertIsInstance(trimmed_curve_1, Curve)
        self.assertEqual(trimmed_curve_1.curve_type, curve_1.curve_type)
        self.assertLess(len(trimmed_curve_1.points), original_point_count_1)

        # 交点座標検証
        last_point = trimmed_curve_1.points[-1]
        self.assertAlmostEqual(last_point.x, 50.0, places=1)
        self.assertAlmostEqual(last_point.y, 50.0 * math.sqrt(3.0), places=1)

        # トポロジーメタデータ検証
        self.assertEqual(trimmed_curve_1.id_before_trim, original_id_1)
        self.assertEqual(trimmed_curve_1.end_trimmed_by, original_id_2)
    #end def
#end class

if __name__ == '__main__':
    unittest.main()
#end