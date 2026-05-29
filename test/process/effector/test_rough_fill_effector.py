import unittest
from PIL import Image

from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from process.effector.rough_fill_effector import RoughFillEffector


class TestRoughFillEffector(unittest.TestCase):

    def test_apply_single_closed_polygon(self):
        """4本の線分が交差してできる、中央の閉じられた1つの正方形領域が正しく抽出されるか検証"""
        # 横線1: Y=10 (X: 0 -> 30)
        line_h1 = Curve(points=[Point(0.0, 10.0), Point(30.0, 10.0)], curve_type=CurveType.LINEAR_APPROXIMATE)
        # 横線2: Y=20 (X: 0 -> 30)
        line_h2 = Curve(points=[Point(0.0, 20.0), Point(30.0, 20.0)], curve_type=CurveType.LINEAR_APPROXIMATE)
        # 縦線1: X=10 (Y: 0 -> 30)
        line_v1 = Curve(points=[Point(10.0, 0.0), Point(10.0, 30.0)], curve_type=CurveType.LINEAR_APPROXIMATE)
        # 縦線2: X=20 (Y: 0 -> 30)
        line_v2 = Curve(points=[Point(20.0, 0.0), Point(20.0, 30.0)], curve_type=CurveType.LINEAR_APPROXIMATE)

        input_curves = [line_h1, line_h2, line_v1, line_v2]

        # view_box を指定してエフェクターを初期化
        effector = RoughFillEffector(view_box="0 0 100 100")
        fill_parts = effector.apply(input_curves)

        # 検証：外枠との衝突も含めるといくつかのポリゴンが生成されますが、
        # 4本の交差から生まれる「中央の正方形 (10,10)-(20,20)」の幾何形状を持ったCurveが確実に含まれているかを探します。
        target_poly = None
        expected_coords = {(10.0, 10.0), (20.0, 10.0), (20.0, 20.0), (10.0, 20.0)}

        for poly_curve in fill_parts:
            self.assertEqual(poly_curve.curve_type, CurveType.LINEAR_APPROXIMATE)
            actual_coords = {(p.x, p.y) for p in poly_curve.points}
            if expected_coords.issubset(actual_coords) and len(poly_curve.points) == 5:
                target_poly = poly_curve
                break
            #end if
        #end for

        self.assertIsNotNone(target_poly, "中央の正方形を構成するポリゴンCurveが抽出されていない")
        self.assertIsNone(target_poly.color, "参照画像がない場合はcolor属性がNoneであるべき")
    #end def

    def test_apply_with_reference_image(self):
        """カラー参照用画像を与えた場合、その領域内の最頻色がcolor属性に文字列として入ることを検証"""
        # 10x10の領域を囲む小さな閉じたポリゴン
        curve = Curve(points=[Point(0.0, 0.0), Point(10.0, 0.0), Point(10.0, 10.0), Point(0.0, 10.0), Point(0.0, 0.0)], curve_type=CurveType.LINEAR_APPROXIMATE)

        # 10x10 の赤い単色画像を生成
        ref_img = Image.new("RGB", (10, 10), (255, 0, 0))

        effector = RoughFillEffector(view_box="0 0 10 10", reference_image=ref_img)
        fill_parts = effector.apply([curve])

        self.assertTrue(len(fill_parts) > 0)
        # 確実に該当するポリゴンを確認
        has_red_poly = False
        for p in fill_parts:
            if p.color == "rgb(255,0,0)":
                has_red_poly = True
                break
            #end if
        #end for
        self.assertTrue(has_red_poly, "ポリゴンの色サンプリングが正しく機能していない")
    #end def
#end class


if __name__ == '__main__':
    unittest.main()
#end