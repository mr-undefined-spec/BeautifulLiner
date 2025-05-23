import unittest

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/layer'))
from layer import Layer
from canvas import Canvas

sys.path.append(os.path.join(os.path.dirname(__file__), '../../handler'))
from write_handler import WriteHandler

sys.path.append(os.path.join(os.path.dirname(__file__), '../helper'))
import model_mocks
import handler_mocks
from handler_mocks import ArcDirection

from unittest.mock import MagicMock

class TestWriteHandler(unittest.TestCase):
    def test_write(self):
        curve_1 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0,   0.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)
        curve_2 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0, 200.0, 180.0, 270.0, 100, ArcDirection.COUNTER_CLOCKWISE)
        curve_3 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0, -200.0, 200.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)

        layer = model_mocks.create_mock_layer([curve_1, curve_2, curve_3])
        self.canvas = MagicMock(spec=Canvas)
        self.canvas.get_bbox.return_value = [0, 0, 100, 100]
        self.canvas.view_box = "0,0,100,100"
        self.canvas.__iter__.return_value = iter([layer])

        WriteHandler.process(self.canvas, "out.svg")

    #end


#end

if __name__ == '__main__':
    unittest.main()
#end

