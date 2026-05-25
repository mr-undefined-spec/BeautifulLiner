# test/model/container/test_canvas.py
import unittest
from model.container.layer import Layer
from model.container.canvas import Canvas

class TestCanvas(unittest.TestCase):
    def setUp(self):
        # 本物の Layer を素直に生成
        layer = Layer("test_layer", "#000000")

        self.canvas = Canvas()
        self.canvas.append(layer)
    #end def

    def test_init_and_getitem(self):
        self.assertIsInstance(self.canvas[0], Layer)
        self.assertEqual(len(self.canvas), 1)
    #end def

    def test_view_box(self):
        # カンマ区切りのテスト
        self.canvas.set_view_box("0,0,100,200")
        self.assertEqual(self.canvas.view_box, "0,0,100,200")
        self.assertEqual(self.canvas.get_bbox(), (0.0, 0.0, 100.0, 200.0))

        # スペース区切りのテスト
        self.canvas.set_view_box("10 20 300 400")
        self.assertEqual(self.canvas.get_bbox(), (10.0, 20.0, 300.0, 400.0))
    #end def

    def test_get_total_curve_num(self):
        # 初期状態（セットアップで入れた空のLayerが1つ）なので、曲線の合計は0
        self.assertEqual(self.canvas.get_total_curve_num(), 0)
    #end def

    def test_invalid_append(self):
        with self.assertRaises(TypeError):
            self.canvas.append("not a layer")
        #end with
    #end def
#end class

if __name__ == '__main__':
    unittest.main()
#end if