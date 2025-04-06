
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/primitive'))
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/curve'))
from linear_approximate_curve import LinearApproximateCurve

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/layer'))
from layer import Layer
from layer_set import LayerSet

from basic_controller import BasicController

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class QtreeController(BasicController):
    def __init__(self, total_step_num):
        self.total_step_num = total_step_num
    #end

    def process(self, linearize_layer_set):
        new_linear_layer_set = LayerSet()

        bbox = linearize_layer_set.get_bbox()
        # create qtree
        for layer in linearize_layer_set:
            tmp_layer = Layer(layer.name)
            for step_num, curve in enumerate(layer):
                curve.create_qtree_ctrl_p_set(bbox)
                tmp_layer.append(curve)
                self.print_step("create qtree", step_num)
            #end
            new_linear_layer_set.append(tmp_layer)
        #end
        new_linear_layer_set.set_view_box( linearize_layer_set.view_box )

        return new_linear_layer_set
    #end
#end