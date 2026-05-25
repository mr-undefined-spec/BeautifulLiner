# test/model/curve/test_thin_cubic_bezier_curve.py
import unittest
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(os.path.join(__file__, "../../../")))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
#end if

from model.primitive.point import Point
from model.curve.thin_cubic_bezier_curve import ThinCubicBezierCurve

class TestThinCubicBezierCurve(unittest.TestCase):
    def setUp(self):
        # 1区間分のベジエ曲線（4点）
        self.points = [
            Point(0.0, 0.0),  # 始点
            Point(1.0, 2.0),  # 制御点1
            Point(2.0, 2.0),  # 制御点2
            Point(3.0, 0.0)   # 終点
        ]
        self.curve = ThinCubicBezierCurve(self.points)
    #end def

    def test_init_and_properties(self):
        self.assertEqual(len(self.curve.points), 4)
        self.assertFalse(self.curve.is_broad)
    #end def

    def test_invalid_points_count(self):
        # 5点は 3N+1 を満たさないのでエラーになるべき
        invalid_points = [Point(0,0), Point(1,1), Point(2,2), Point(3,3), Point(4,4)]
        with self.assertRaises(ValueError):
            ThinCubicBezierCurve(invalid_points)
        #end with
    #end def

    def test_to_str(self):
        # SVGの 'C' コマンド表現の検証
        expected = "M 0.000 0.000 C 1.000 2.000, 2.000 2.000, 3.000 0.000 "
        self.assertEqual(self.curve.to_str(), expected)
    #end def

    def test_shapely_integration(self):
        ls = self.curve.shapely
        self.assertEqual(ls.geom_type, "LineString")
        
        # 境界ボックスの妥当性チェック
        minx, miny, maxx, maxy = ls.bounds
        self.assertAlmostEqual(minx, 0.0)
        self.assertAlmostEqual(maxx, 3.0)
        # 制御点が y=2.0 にあるので、ベジエ曲線は y=0.0 〜 1.5（付近）に収まるはず
        self.assertTrue(0.0 <= miny <= maxy <= 2.0)
    #end def
#end class

if __name__ == "__main__":
    unittest.main()
#end if