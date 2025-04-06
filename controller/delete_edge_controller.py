from argparse import ArgumentParser

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'model/curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'model/layer'))
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from linear_approximate_curve import LinearApproximateCurve
from layer import Layer
from layer_set import LayerSet

sys.path.append(os.path.join(os.path.dirname(__file__), 'handler'))

from pickup_intersection_candidates_handler import PickupIntersectionCandidatesHandler
from delete_edge_handler import DeleteEdgeHandler

from basic_controller import BasicController

class DeleteEdgeController(BasicController):
    def __init__(self, total_step_num):
        self.total_step_num = total_step_num
    #end

    def process(self, linearize_layer_set, delete_ratio):

        # initialize handlers
        pickup_intersection_candidates_handler = PickupIntersectionCandidatesHandler()
        delete_edge_handler = DeleteEdgeHandler()

        delete_edge_layer_set = LayerSet()

        # delete edge
        for layer in linearize_layer_set:
            tmp_layer = Layer(layer.name)
            other_curves = layer.get_curves()
            for i, target_curve in enumerate(layer):

                self.print_step("delete edge", i)

                candidates = pickup_intersection_candidates_handler.process(target_curve, other_curves)

                tmp_curve = target_curve

                for other_curve in candidates:
                    tmp_curve = DeleteEdgeHandler.process(tmp_curve, other_curve, delete_ratio)
                #end
                
                tmp_layer.append(tmp_curve)
            #end
            delete_edge_layer_set.append(tmp_layer)
        #end
        delete_edge_layer_set.set_view_box( linearize_layer_set.view_box )

        return delete_edge_layer_set
    #end
#end
