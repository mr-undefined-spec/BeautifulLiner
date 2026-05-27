import unittest
import os
import sys

# プロジェクトのルートディレクトリ（E:\BeautifulLiner）を確実に検索パスに追加
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
#end if

# ルートからの絶対インポートで統一
from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType

class TestCurve(unittest.TestCase):

    # -------------------------------------------------------------------------
    # 線形近似曲線（LINEAR_APPROXIMATE）のテスト
    # -------------------------------------------------------------------------
    def test_linear_init_and_properties(self):
        # 一筆書きで繋がる、折れ線の点列を定義
        points = [
            Point(0.0, 0.0),
            Point(1.0, 1.0),
            Point(1.0, 0.0),
            Point(0.0, 1.0),
            Point(2.0, 1.0)
        ]
        curve = Curve(points, CurveType.LINEAR_APPROXIMATE)

        self.assertEqual(len(curve.points), 5)
        self.assertEqual(curve.curve_type, CurveType.LINEAR_APPROXIMATE)
        self.assertEqual(curve.points[0], Point(0.0, 0.0))
        self.assertEqual(curve.points[-1], Point(2.0, 1.0))
        self.assertFalse(curve.is_broad)
    #end def

    def test_linear_invalid_init(self):
        # 点が1つしかない場合はエラーになるべき
        with self.assertRaises(ValueError):
            Curve([Point(0.0, 0.0)], CurveType.LINEAR_APPROXIMATE)
        #end with
    #end def

    def test_linear_to_str(self):
        points = [
            Point(0.0, 0.0),
            Point(1.0, 1.0),
            Point(1.0, 0.0),
            Point(0.0, 1.0),
            Point(2.0, 1.0)
        ]
        curve = Curve(points, CurveType.LINEAR_APPROXIMATE)
        # SVGパス文字列の検証 (M から始まり、残りが L で繋がっているか)
        expected_str = "M 0.000 0.000 L 1.000 1.000 L 1.000 0.000 L 0.000 1.000 L 2.000 1.000 "
        self.assertEqual(curve.to_str(), expected_str)
    #end def

    def test_linear_shapely_bounds(self):
        points = [
            Point(0.0, 0.0),
            Point(1.0, 1.0),
            Point(1.0, 0.0),
            Point(0.0, 1.0),
            Point(2.0, 1.0)
        ]
        curve = Curve(points, CurveType.LINEAR_APPROXIMATE)
        ls = curve.shapely
        self.assertEqual(ls.geom_type, "LineString")

        # 曲線全体のバウンディングボックス (minx, miny, maxx, maxy)
        minx, miny, maxx, maxy = ls.bounds
        self.assertAlmostEqual(minx, 0.0)
        self.assertAlmostEqual(miny, 0.0)
        self.assertAlmostEqual(maxx, 2.0)
        self.assertAlmostEqual(maxy, 1.0)
    #end def

    # -------------------------------------------------------------------------
    # 3次ベジェ曲線（CUBIC_BEZIER）のテスト
    # -------------------------------------------------------------------------
    def test_bezier_init_and_properties(self):
        # 1区間分のベジエ曲線（4点）
        points = [
            Point(0.0, 0.0),  # 始点
            Point(1.0, 2.0),  # 制御点1
            Point(2.0, 2.0),  # 制御点2
            Point(3.0, 0.0)   # 終点
        ]
        curve = Curve(points, CurveType.CUBIC_BEZIER)

        self.assertEqual(len(curve.points), 4)
        self.assertEqual(curve.curve_type, CurveType.CUBIC_BEZIER)
        self.assertFalse(curve.is_broad)
    #end def

    def test_bezier_invalid_points_count(self):
        # 5点は 3N+1 を満たさないのでエラーになるべき
        invalid_points = [Point(0,0), Point(1,1), Point(2,2), Point(3,3), Point(4,4)]
        with self.assertRaises(ValueError):
            Curve(invalid_points, CurveType.CUBIC_BEZIER)
        #end with
    #end def

    def test_bezier_to_str(self):
        points = [
            Point(0.0, 0.0),
            Point(1.0, 2.0),
            Point(2.0, 2.0),
            Point(3.0, 0.0)
        ]
        curve = Curve(points, CurveType.CUBIC_BEZIER)
        # SVGの 'C' コマンド表現の検証
        expected = "M 0.000 0.000 C 1.000 2.000, 2.000 2.000, 3.000 0.000 "
        self.assertEqual(curve.to_str(), expected)
    #end def

    def test_bezier_shapely_integration(self):
        points = [
            Point(0.0, 0.0),
            Point(1.0, 2.0),
            Point(2.0, 2.0),
            Point(3.0, 0.0)
        ]
        curve = Curve(points, CurveType.CUBIC_BEZIER)
        ls = curve.shapely
        self.assertEqual(ls.geom_type, "LineString")
        
        # 境界ボックスの妥当性チェック
        minx, miny, maxx, maxy = ls.bounds
        self.assertAlmostEqual(minx, 0.0)
        self.assertAlmostEqual(maxx, 3.0)
        # 制御点が y=2.0 にあるので、ベジエ曲線は y=0.0 〜 1.5（付近）に収まるはず
        self.assertTrue(0.0 <= miny <= maxy <= 2.0)
    #end def

    # -------------------------------------------------------------------------
    # 共通機能（キャッシュなど）のテスト
    # -------------------------------------------------------------------------
    def test_shapely_cached(self):
        # どちらのタイプでも2回目以降のアクセスで同じインスタンスが返るか
        points_linear = [Point(0.0, 0.0), Point(1.0, 1.0)]
        curve_linear = Curve(points_linear, CurveType.LINEAR_APPROXIMATE)
        
        ls1_lin = curve_linear.shapely
        ls2_lin = curve_linear.shapely
        self.assertIs(ls1_lin, ls2_lin)

        points_bezier = [Point(0.0, 0.0), Point(1.0, 2.0), Point(2.0, 2.0), Point(3.0, 0.0)]
        curve_bezier = Curve(points_bezier, CurveType.CUBIC_BEZIER)

        ls1_bez = curve_bezier.shapely
        ls2_bez = curve_bezier.shapely
        self.assertIs(ls1_bez, ls2_bez)
    #end def
#end class

if __name__ == '__main__':
    unittest.main()
#end if