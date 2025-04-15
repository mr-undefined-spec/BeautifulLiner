
import os
import sys

#sys.path.append(os.path.join(os.path.dirname(__file__), '../model/primitive'))
#from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/curve'))
from linear_approximate_curve import LinearApproximateCurve
from cubic_bezier_curve import CubicBezierCurve

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/layer'))
from layer import Layer
from canvas import Canvas

sys.path.append(os.path.join(os.path.dirname(__file__), '../handler'))
from curve_orientation_handler import CurveOrientationHandler
from split_handler import SplitHandler
from smoothen_handler import SmoothenHandler

from basic_controller import BasicController

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class SplitController(BasicController):
    def __init__(self, total_step_num):
        self.total_step_num = total_step_num
    #end

    def process(self, linearize_canvas):
        new_canvas = Canvas()

        for layer in linearize_canvas:
            tmp_layer = Layer(layer.name)
            for step_num, curve in enumerate(layer):
                self.print_step("split", step_num)

                curve_orientations = CurveOrientationHandler.process(curve)

                split_curve_ranges = SplitHandler.process(curve_orientations, curve.start_index)

                #new_curve = LinearApproximateCurve()
                #new_curve.copy(curve)
                new_curve = curve
                new_curve.set_split_ranges( split_curve_ranges )
                tmp_layer.append(new_curve)

            #end
            new_canvas.append(tmp_layer)
        #end

        new_canvas.set_view_box( linearize_canvas.view_box )

        return new_canvas
    #end
#end