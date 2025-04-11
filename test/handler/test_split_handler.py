import unittest

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../handler'))
from split_handler import SplitHandler

sys.path.append(os.path.join(os.path.dirname(__file__), '../helper'))
import model_mocks
import handler_mocks
from handler_mocks import ArcDirection


class TestSplitHandler(unittest.TestCase):

    def test_split(self):
        curve_orientations = [1, 1, 1, -1, -1, -1, 1, 1, 1]

        split_curve_ranges = SplitHandler.process(curve_orientations, 0)

        self.assertEqual(split_curve_ranges, [(0, 3), (3, 6), (6, 9)])
    #end
#end

if __name__ == '__main__':
    unittest.main()
#end

