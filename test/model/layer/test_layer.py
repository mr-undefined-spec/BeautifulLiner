import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../utils'))
import mocks

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/layer'))
from layer import Layer
from layer import EndpointStyle
from curve_set import CurveSet

import unittest

import numpy as np
import math

class TestLayer(unittest.TestCase):
    def setUp(self):
        curve_set = mocks.create_mock_curve_set()

        self.layer = Layer("layer_name")
        self.layer.append(curve_set)
    #end

    def test_init_and_getitem(self):
        self.assertEqual(isinstance(self.layer[0], CurveSet), True)
    #end

    def test_set_write_options(self):
        self.layer.set_write_options(True, "#000000", EndpointStyle.BOTH_POINTED)
        self.assertEqual(self.layer.is_fill, True)
        self.assertEqual(self.layer.color, "#000000")
        self.assertEqual(self.layer.endpoint_style, EndpointStyle.BOTH_POINTED)
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end