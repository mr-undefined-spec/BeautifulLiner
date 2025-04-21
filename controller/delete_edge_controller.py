import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/curve'))
from linear_approximate_curve import LinearApproximateCurve

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/layer'))
from layer import Layer
from canvas import Canvas

sys.path.append(os.path.join(os.path.dirname(__file__), '../handler'))
from pickup_intersection_candidates_handler import PickupIntersectionCandidatesHandler
from delete_edge_handler import DeleteEdgeHandler

from basic_controller import BasicController

class DeleteEdgeController(BasicController):
    def set_delete_ratio(self, delete_ratio):
        self.delete_ratio = delete_ratio
    #end

    def process(self, linearize_canvas):

        # initialize handlers
        pickup_intersection_candidates_handler = PickupIntersectionCandidatesHandler()
        delete_edge_handler = DeleteEdgeHandler()

        delete_edge_canvas = Canvas()

        # delete edge
        for layer in linearize_canvas:
            tmp_layer = Layer(layer.name, layer.color)
            other_curves = layer.get_curves()
            for i, target_curve in enumerate(layer):

                self.print_step("delete edge", i)

                candidates = pickup_intersection_candidates_handler.process(target_curve, other_curves)

                tmp_curve = target_curve

                for other_curve in candidates:
                    tmp_curve = DeleteEdgeHandler.process(tmp_curve, other_curve, self.delete_ratio)
                #end
                
                tmp_layer.append(tmp_curve)
            #end
            delete_edge_canvas.append(tmp_layer)
        #end
        delete_edge_canvas.set_view_box( linearize_canvas.view_box )

        return delete_edge_canvas
    #end
#end
