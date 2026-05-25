# test/model/curve/test_thin_linear_approximate_curve.py
import unittest
import os
import sys

# プロジェクトのルートディレクトリ（E:\BeautifulLiner）を確実に検索パスに追加
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(PROJECT_ROOT)

# ルートからの絶対インポートで美しく統一
from model.primitive.point import Point
from model.curve.thin_linear_approximate_curve import ThinLinearApproximateCurve

class TestThinLinearApproximateCurve(unittest.TestCase):
    def setUp(self):
        # 一筆書きで繋がる、折れ線の点列を定義
        # (0,0) -> (1,1) -> (1,0) -> (0,1) -> (2,1)
        self.points = [
            Point(0.0, 0.0),
            Point(1.0, 1.0),
            Point(1.0, 0.0),
            Point(0.0, 1.0),
            Point(2.0, 1.0)
        ]
        self.curve = ThinLinearApproximateCurve(self.points)
    #end def

    def test_init_and_properties(self):
        # 正しく点列が保持されているか
        self.assertEqual(len(self.curve.points), 5)
        self.assertEqual(self.curve.points[0], Point(0.0, 0.0))
        self.assertEqual(self.curve.points[-1], Point(2.0, 1.0))
        self.assertFalse(self.curve.is_broad)
    #end def

    def test_invalid_init(self):
        # 点が1つしかない場合はエラーになるべき
        with self.assertRaises(ValueError):
            ThinLinearApproximateCurve([Point(0.0, 0.0)])
        #end with
    #end def

    def test_to_str(self):
        # SVGパス文字列の検証 (M から始まり、残りが L で繋がっているか)
        expected_str = "M 0.000 0.000 L 1.000 1.000 L 1.000 0.000 L 0.000 1.000 L 2.000 1.000 "
        self.assertEqual(self.curve.to_str(), expected_str)
    #end def

    def test_shapely_bounds(self):
        # ShapelyのLineStringが正しく生成されているか
        ls = self.curve.shapely
        self.assertEqual(ls.geom_type, "LineString")

        # 曲線全体のバウンディングボックス (minx, miny, maxx, maxy)
        # 点列全体の最小/最大は x: 0.0~2.0, y: 0.0~1.0
        minx, miny, maxx, maxy = ls.bounds
        self.assertAlmostEqual(minx, 0.0)
        self.assertAlmostEqual(miny, 0.0)
        self.assertAlmostEqual(maxx, 2.0)
        self.assertAlmostEqual(maxy, 1.0)
    #end def

    def test_shapely_cached(self):
        # 2回目以降のアクセスで同じインスタンスが返る（キャッシュ効いている）か
        ls1 = self.curve.shapely
        ls2 = self.curve.shapely
        self.assertIs(ls1, ls2)
    #end def
#end class

if __name__ == '__main__':
    unittest.main()
#end if