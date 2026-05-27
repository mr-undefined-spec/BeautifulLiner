import unittest
from model.primitive.point import Point
from model.container.layer import Layer, EndpointStyle
from model.primitive.curve import Curve, CurveType  # CurveTypeをインポートに追加

class TestLayer(unittest.TestCase):
    def setUp(self):
        points = [Point(0.0, 0.0), Point(1.0, 1.0), Point(2.0, 1.0)]
        # 引数に CurveType.LINEAR_APPROXIMATE を追加して修正
        linear_curve = Curve(points, CurveType.LINEAR_APPROXIMATE)

        self.layer = Layer("layer_name", "black")
        self.layer.append(linear_curve)
    #end def

    def test_init_and_getitem(self):
        # インデックスアクセスの検証
        self.assertIsInstance(self.layer[0], Curve)
        self.assertEqual(len(self.layer), 1)
    #end def

    def test_set_write_options(self):
        self.layer.set_write_options(True, "#000000", EndpointStyle.BOTH_POINTED)
        self.assertEqual(self.layer.is_fill, True)
        self.assertEqual(self.layer.color, "#000000")
        self.assertEqual(self.layer.endpoint_style, EndpointStyle.BOTH_POINTED)
    #end def

    def test_invalid_init(self):
        with self.assertRaises(TypeError):
            Layer(123, "black")
        #end with
        with self.assertRaises(TypeError):
            Layer("name", 123)
        #end with
    #end def
#end class

if __name__ == '__main__':
    unittest.main()
#end if