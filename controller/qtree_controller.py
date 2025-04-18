import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/primitive'))
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/curve'))
from linear_approximate_curve import LinearApproximateCurve
from cubic_bezier_curve import CubicBezierCurve

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/layer'))
from layer import Layer
from canvas import Canvas

from basic_controller import BasicController

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class QtreeController(BasicController):
    def process(self, linearize_canvas):
        new_linear_canvas = Canvas()

        bbox = linearize_canvas.get_bbox()
        # create qtree
        for layer in linearize_canvas:
            tmp_layer = Layer(layer.name)
            for step_num, curve in enumerate(layer):
                curve.create_qtree_going_ctrl_p_list(bbox)
                tmp_layer.append(curve)
                self.print_step("create qtree", step_num)
            #end
            new_linear_canvas.append(tmp_layer)
        #end
        new_linear_canvas.set_view_box( linearize_canvas.view_box )

        return new_linear_canvas
    #end
#end