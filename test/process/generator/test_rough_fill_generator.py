import unittest

from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from model.container.layer import Layer
from model.container.canvas import Canvas
from process.generator.rough_fill_generator import RoughFillGenerator


class TestRoughFillGenerator(unittest.TestCase):

    def test_generate_single_closed_polygon(self):
        """4本の線分が交差してできる、中央の閉じられた1つの正方形領域が正しく抽出されるか検証"""
        
        # 1. テスト用の線画レイヤーとキャンバスを構築
        # 4本の線をクロスさせて、中央に (10, 10) から (20, 20) の正方形を作ります
        #
        #       |      |
        #    ---(10,20)(20,20)---
        #       |      |
        #    ---(10,10)(20,10)---
        #       |      |
        
        # 横線1: Y=10 (X: 0 -> 30)
        line_h1 = Curve(
            points=[Point(0.0, 10.0), Point(30.0, 10.0)],
            curve_type=CurveType.LINEAR_APPROXIMATE
        )
        # 横線2: Y=20 (X: 0 -> 30)
        line_h2 = Curve(
            points=[Point(0.0, 20.0), Point(30.0, 20.0)],
            curve_type=CurveType.LINEAR_APPROXIMATE
        )
        # 縦線1: X=10 (Y: 0 -> 30)
        line_v1 = Curve(
            points=[Point(10.0, 0.0), Point(10.0, 30.0)],
            curve_type=CurveType.LINEAR_APPROXIMATE
        )
        # 縦線2: X=20 (Y: 0 -> 30)
        line_v2 = Curve(
            points=[Point(20.0, 0.0), Point(20.0, 30.0)],
            curve_type=CurveType.LINEAR_APPROXIMATE
        )

        stroke_layer = Layer("line_art", "#000000")
        stroke_layer.append(line_h1)
        stroke_layer.append(line_h2)
        stroke_layer.append(line_v1)
        stroke_layer.append(line_v2)

        stroke_canvas = Canvas()
        stroke_canvas.set_view_box((0.0, 0.0, 100.0, 100.0))
        stroke_canvas.append(stroke_layer)

        # 2. ジェネレータを実行して塗りキャンバスを生成
        fill_canvas = RoughFillGenerator.generate(stroke_canvas)

        # 3. 検証
        self.assertIsInstance(fill_canvas, Canvas)
        self.assertEqual(len(fill_canvas), 1, "レイヤー数が一致すること")
        
        fill_layer = fill_canvas[0]
        self.assertEqual(fill_layer.name, "line_art_fill")
        
        # 4本の交差から生まれる閉領域（Polygon）は中央の1つだけのはず
        self.assertEqual(len(fill_layer), 1, "抽出された閉領域の数が1つであること")

        poly_curve = fill_layer[0]
        self.assertIsInstance(poly_curve, Curve)
        self.assertEqual(poly_curve.curve_type, CurveType.LINEAR_APPROXIMATE, "CurveTypeがLINEAR_APPROXIMATEであること")

        # 4. 抽出された面の幾何学的な正しさを検証
        # ShapelyのPolygonの外周（exterior.coords）は、始点に戻るため4頂点+終点=5点になります
        self.assertEqual(len(poly_curve.points), 5, "閉じられたポリゴンの点列（始点重複含む）の数が5であること")

        # 中央の正方形の4つの角 (10,10), (20,10), (20,20), (10,20) が含まれているか（順不同）
        expected_coords = {(10.0, 10.0), (20.0, 10.0), (20.0, 20.0), (10.0, 20.0)}
        actual_coords = {(p.x, p.y) for p in poly_curve.points}

        # 集合演算で、期待する4つの角の座標がすべて含まれているかチェック
        self.assertTrue(expected_coords.issubset(actual_coords), f"正方形の角の座標が正しく抽出されていること: {actual_coords}")
    #end def
#end class

if __name__ == '__main__':
    unittest.main()