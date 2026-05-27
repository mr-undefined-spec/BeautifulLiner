import unittest
import math

from model.primitive.curve import Curve, CurveType
from process.converter.linearize_converter import LinearizeConverter

# 新しく作った綺麗なデータ生成関数群をインポート
from test.helper.converter_mocks import create_mock_layer_set_of_cubic_bezier_curve_arc


class TestLinearizeConverter(unittest.TestCase):
    def setUp(self):
        # 1. 3次ベジェ曲線を含んだ本物のLayerリストを取得
        layers = create_mock_layer_set_of_cubic_bezier_curve_arc()
        
        # 2. 最初のレイヤーの最初の曲線（これが3次ベジェの円弧）をテスト対象にする
        self.bezier_curve = layers[0][0]

    def test_convert(self):
        # 変換処理の実行
        linearized_curve = LinearizeConverter.convert(self.bezier_curve)

        # 戻り値の型と属性の検証
        self.assertIsInstance(linearized_curve, Curve)
        
        self.assertEqual(linearized_curve.curve_type, CurveType.LINEAR_APPROXIMATE)
        self.assertEqual(linearized_curve.is_broad, self.bezier_curve.is_broad)
        
        # 点がしっかりと生成されていること
        self.assertGreater(len(linearized_curve.points), 2)

        # 幾何学的な正しさの検証（原点から半径100の円周上にあるか）
        for point in linearized_curve.points:
            distance_from_origin = math.sqrt(point.x**2 + point.y**2)
            self.assertEqual(round(distance_from_origin), 100)
        # end for
    # end def
# end class

if __name__ == '__main__':
    unittest.main()