
import os
import sys

import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/compose'))

from point import Point
from cubic_bezier_curve import CubicBezierCurve
from linear_approximate_curve import LinearApproximateCurve
from layer import Layer

from layer_set import LayerSet

import unittest

class TestLayerSetData(unittest.TestCase):
    pass
#end

if __name__ == '__main__':
    unittest.main()
#end
