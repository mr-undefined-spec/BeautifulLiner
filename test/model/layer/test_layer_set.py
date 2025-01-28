import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../utils'))
import mocks

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/layer'))
from layer_set import LayerSet
from layer import Layer

import unittest

import numpy as np
import math

class TestLayerSet(unittest.TestCase):
    def setUp(self):
        layer = mocks.create_mock_layer()

        self.layer_set = LayerSet()
        self.layer_set.append(layer)
    #end

    def test_init_and_getitem(self):
        self.assertEqual(isinstance(self.layer_set[0], Layer), True)
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end