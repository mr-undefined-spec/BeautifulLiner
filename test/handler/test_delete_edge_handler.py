
import os
import sys




import unittest


sys.path.append(os.path.join(os.path.dirname(__file__), '../../handler'))
from delete_edge_handler import DeleteEdgeHandler

sys.path.append(os.path.join(os.path.dirname(__file__), '../helper'))
import model_mocks
import handler_mocks
from handler_mocks import ArcDirection

from unittest.mock import MagicMock

import numpy as np
import math

class TestDeleteEdgeHandler(unittest.TestCase):
    def test_delete_edge(self):
        curve_1 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0,    0.0,   0.0,   0.0,  90.0, 100, ArcDirection.CLOCKWISE)
        curve_2 = handler_mocks.create_mock_linear_approximate_curve_of_arc(100.0,  100.0,   0.0,  90.0, 180.0, 100, ArcDirection.CLOCKWISE)

        bbox = ( 0.0, 0.0, 200.0, 200.0 )
        curve_1.create_qtree_going_ctlr_p_list(bbox)
        curve_2.create_qtree_going_ctlr_p_list(bbox)

        self.assertEqual(curve_1.end_index, -1)
        edge_deleted_curve = DeleteEdgeHandler.process(curve_1, curve_2, 0.5)
        self.assertEqual(edge_deleted_curve.end_index, 66)
    #end



#end

if __name__ == '__main__':
    unittest.main()
#end

