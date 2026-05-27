import unittest
import os
import sys

from process.converter.smoothen_converter import SmoothenConverter
from model.primitive.curve import Curve, CurveType

# Mocks のインポート経路は現在のプロジェクト配置に合わせて適宜調整してください
from test.helper import converter_mocks
from test.helper.converter_mocks import ArcDirection


class TestSmoothenConverter(unittest.TestCase):
    def setUp(self):
        # 擬似的な円弧の線形近似曲線（旧環境のモックをそのまま活用）
        self.curve_1 = converter_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0,   0.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)
        self.curve_2 = converter_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0, 200.0, 180.0, 270.0, 100, ArcDirection.COUNTER_CLOCKWISE)
        self.curve_3 = converter_mocks.create_mock_linear_approximate_curve_of_arc(100.0, -200.0, 200.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)
    #end

    def _convert_curve_to_test_str(self, curve: Curve) -> str:
        """新生Curveの持つ4つのPointを、旧テストが期待する文字列フォーマットに変換するヘルパー"""
        result = ""
        for p in curve.points:
            # 各点の座標を "X.XXX Y.YYY\n" の形式で結合
            result += f"{p.x:.3f} {p.y:.3f}\n"
        return result
    #end

    def test_convert(self):
        # 期待する各制御点の座標文字列
        the_answer_1 = "100.000 0.000\n101.572 53.551\n53.551 101.572\n0.000 100.000\n"
        the_answer_2 = "-0.000 100.000\n-53.551 98.428\n-101.572 146.449\n-100.000 200.000\n"
        the_answer_3 = "-100.000 200.000\n-98.428 253.551\n-146.449 301.572\n-200.000 300.000\n"

        # SmoothenConverter.convert を実行）
        smoothened_curve_1 = SmoothenConverter.convert(self.curve_1)
        smoothened_curve_2 = SmoothenConverter.convert(self.curve_2)
        smoothened_curve_3 = SmoothenConverter.convert(self.curve_3)

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