import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../model/layer'))
from layer import Layer
from canvas import Canvas

sys.path.append(os.path.join(os.path.dirname(__file__), '../handler'))
from linearize_handler import LinearizeHandler

from basic_controller import BasicController

class LinearizeController(BasicController):
    def set_linear_approximate_length(self, linear_approximate_length):
        self.linear_approximate_length = linear_approximate_length
    #end

    def process(self, cubic_bezier_canvas):

        # initialize handlers
        linearize_handler = LinearizeHandler()

        # linearize
        linearize_canvas = Canvas()
        for cubic_bezier_layer in cubic_bezier_canvas:
            tmp_layer = Layer(cubic_bezier_layer.name, cubic_bezier_layer.color)
            for i, cubic_bezier_curve in enumerate(cubic_bezier_layer):
                self.print_step("linearize", i)
                linearized_curve = LinearizeHandler.process(cubic_bezier_curve, self.linear_approximate_length)
                if len(linearized_curve) < 3:
                    continue
                #end
                tmp_layer.append(linearized_curve)
            #end
            linearize_canvas.append(tmp_layer)
        #end

        linearize_canvas.set_view_box( cubic_bezier_canvas.view_box )

        return linearize_canvas
    #end
#end
