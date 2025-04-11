import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../model/layer'))
from layer import Layer
from canvas import Canvas

sys.path.append(os.path.join(os.path.dirname(__file__), '../handler'))
from linearize_handler import LinearizeHandler

from basic_controller import BasicController

class LinearizeController(BasicController):
    def __init__(self, total_step_num):
        self.total_step_num = total_step_num
    #end

    def process(self, cubic_bezier_canvas, linear_approximate_length):

        # initialize handlers
        linearize_handler = LinearizeHandler()

        # linearize
        linearize_canvas = Canvas()
        for cubic_bezier_layer in cubic_bezier_canvas:
            tmp_layer = Layer(cubic_bezier_layer.name)
            for i, cubic_bezier_curve in enumerate(cubic_bezier_layer):
                self.print_step("linearize", i)
                linearized_curve = LinearizeHandler.process(cubic_bezier_curve, 0.1)
                tmp_layer.append(linearized_curve)
            #end
            linearize_canvas.append(tmp_layer)
        #end

        linearize_canvas.set_view_box( cubic_bezier_canvas.view_box )

        return linearize_canvas
    #end
#end
