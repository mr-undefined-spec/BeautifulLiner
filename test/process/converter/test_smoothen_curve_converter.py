import unittest

from process.converter.smoothen_curve_converter import SmoothenCurveConverter
from model.primitive.curve import Curve, CurveType

# Mocks のインポート経路
from test.helper import converter_mocks
from test.helper.converter_mocks import ArcDirection


class TestSmoothenCurveConverter(unittest.TestCase):
    def setUp(self):
        # 擬似的な円弧の線形近似曲線
        self.curve_1 = converter_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0,   0.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)
        self.curve_2 = converter_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0, 200.0, 180.0, 270.0, 100, ArcDirection.COUNTER_CLOCKWISE)
        self.curve_3 = converter_mocks.create_mock_linear_approximate_curve_of_arc(100.0, -200.0, 200.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)
        
        # 新しいインスタンスを生成
        self.converter = SmoothenCurveConverter()
    #end

    def _convert_curve_to_test_str(self, curve: Curve) -> str:
        """新生Curveの持つ4つのPointを、テストが期待する文字列フォーマットに変換するヘルパー"""
        result = ""
        for p in curve.points:
            result += f"{p.x:.3f} {p.y:.3f}\n"
        return result
    #end

    def test_convert_multiple_curves(self):
        # 期待する各制御点の座標文字列
        the_answer_1 = "100.000 0.000\n101.572 53.551\n53.551 101.572\n0.000 100.000\n"
        the_answer_2 = "-0.000 100.000\n-53.551 98.428\n-101.572 146.449\n-100.000 200.000\n"
        the_answer_3 = "-100.000 200.000\n-98.428 253.551\n-146.449 301.572\n-200.000 300.000\n"

        # 複数曲線のリストをまとめて1回の呼び出しで投入
        input_curves = [self.curve_1, self.curve_2, self.curve_3]
        output_curves = self.converter.convert(input_curves)

        # 戻り値の要素数検証
        self.assertEqual(len(output_curves), 3)

        # 各要素の検証
        smoothened_curve_1 = output_curves[0]
        smoothened_curve_2 = output_curves[1]
        smoothened_curve_3 = output_curves[2]

        # 戻り値の型とCurveTypeが正しく設定されているか検証
        self.assertEqual(smoothened_curve_1.curve_type, CurveType.CUBIC_BEZIER)
        self.assertEqual(len(smoothened_curve_1.points), 4)

        # 座標の文字列一致テスト
        self.assertEqual(self._convert_curve_to_test_str(smoothened_curve_1), the_answer_1)
        self.assertEqual(self._convert_curve_to_test_str(smoothened_curve_2), the_answer_2)
        self.assertEqual(self._convert_curve_to_test_str(smoothened_curve_3), the_answer_3)
    #end
#end

if __name__ == '__main__':
    unittest.main()
#end