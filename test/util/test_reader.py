# test/util/test_reader.py
import unittest
import os
import sys

# プロジェクトルートへのパスを確保
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
#end if

from util.reader import Reader
from model.primitive.curve import CurveType

class TestReader(unittest.TestCase):
    def test_read(self):
        # プロジェクトルート基準でパスを指定
        svg_path = os.path.join("data", "test.svg")
        canvas = Reader.create_canvas_from_file(svg_path)

        # ---------------------------------------------------------------------
        # 1. 全体構造の検証
        # ---------------------------------------------------------------------
        # gengaレイヤーはパスがないため除外され、Hair, Body, Cloth の3つになるはず
        self.assertEqual(len(canvas), 3)

        # ---------------------------------------------------------------------
        # 2. 各レイヤー名と含まれる曲線数の検証
        # ---------------------------------------------------------------------
        expected_structure = [
            {"name": "Hair",  "curve_count": 2},
            {"name": "Body",  "curve_count": 2},
            {"name": "Cloth", "curve_count": 2}
        ]

        for i, layer_info in enumerate(expected_structure):
            layer = canvas[i]
            self.assertEqual(layer.name, layer_info["name"])
            self.assertEqual(len(layer), layer_info["curve_count"])
            
            # すべて直線近似曲線（LINEAR_APPROXIMATE）として生成されているか確認
            for curve in layer:
                self.assertEqual(curve.curve_type, CurveType.LINEAR_APPROXIMATE)
            #end for
        #end for

        # ---------------------------------------------------------------------
        # 3. 代表的な座標のピンポイント検証
        # ---------------------------------------------------------------------
        hair_layer = canvas[0]
        first_hair_curve = hair_layer[0]
        
        # 始点は M コマンドそのものの座標
        self.assertAlmostEqual(first_hair_curve.points[0].x, 227.192, places=3)
        self.assertAlmostEqual(first_hair_curve.points[0].y, 66.1948, places=3)
        
        # 【修正】Reader側で重複点を削ったため、末尾[-1]がそのまま「本来の終点」になります！
        self.assertAlmostEqual(first_hair_curve.points[-1].x, 242.993, places=3)
        self.assertAlmostEqual(first_hair_curve.points[-1].y, 153.335, places=3)

        # 2つ目のレイヤー "Body" も同様に [-1] に修正
        body_layer = canvas[1]
        first_body_curve = body_layer[0]
        
        # 始点
        self.assertAlmostEqual(first_body_curve.points[0].x, 208.695, places=3)
        self.assertAlmostEqual(first_body_curve.points[0].y, 153.833, places=3)
        
        # 本来の終点
        self.assertAlmostEqual(first_body_curve.points[-1].x, 289.084, places=3)
        self.assertAlmostEqual(first_body_curve.points[-1].y, 227.574, places=3)
    #end def
#end class

if __name__ == '__main__':
    unittest.main()
#end if