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

from linearize_handler import LinearizeHandler

from basic_controller import BasicController

class LinearizeController(BasicController):
    def __init__(self, total_step_num):
        self.total_step_num = total_step_num
    #end

    def process(self, cubic_bezier_layer_set, linear_approximate_length):

        # initialize handlers
        linearize_handler = LinearizeHandler()

        # linearize
        linearize_layer_set = LayerSet()
        for cubic_bezier_layer in cubic_bezier_layer_set:
            tmp_layer = Layer(cubic_bezier_layer.name)
            for i, cubic_bezier_curve in enumerate(cubic_bezier_layer):
                self.print_step("linearize", i)
                linearized_curve = LinearizeHandler.process(cubic_bezier_curve, 0.1)
                tmp_layer.append(linearized_curve)
            #end
            linearize_layer_set.append(tmp_layer)
        #end

        linearize_layer_set.set_view_box( cubic_bezier_layer_set.view_box )

        return linearize_layer_set
    #end
#end
