import unittest

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../helper'))
import model_mocks

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/layer'))
from layer import Layer
from canvas import Canvas

class TestCanvas(unittest.TestCase):
    def setUp(self):
        layer = model_mocks.create_mock_layer([])

        self.canvas = Canvas()
        self.canvas.append(layer)
    #end

    def test_init_and_getitem(self):
        self.assertEqual(isinstance(self.canvas[0], Layer), True)
    #end

    def test_view_box(self):
        self.canvas.set_view_box("0,0,100,100")
        self.assertEqual(self.canvas.view_box, "0,0,100,100")
    #ebd

    def test_get_total_curve_num(self):
        self.assertEqual(self.canvas.get_total_curve_num(), 0)
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end