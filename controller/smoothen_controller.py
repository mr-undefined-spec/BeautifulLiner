
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
from linearize_handler import LinearizeHandler
from curve_orientation_handler import CurveOrientationHandler
from split_handler import SplitHandler
from smoothen_handler import SmoothenHandler

from basic_controller import BasicController

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class SmoothenController(BasicController):
    def __init__(self, total_step_num):
        self.total_step_num = total_step_num
    #end

    def process(self, linearize_canvas, linear_approximate_length, eps_smooth_curve):
        smooth_canvas = Canvas()

        for layer in linearize_canvas:
            tmp_layer = Layer(layer.name)
            for step_num, curve in enumerate(layer):
                self.print_step("smoothen", step_num)

                curve_orientations = CurveOrientationHandler.process(curve)

                split_curve_ranges = SplitHandler.process(curve_orientations, curve.start_index)
                """
                if len(split_curve_ranges) > 1:
                    print(curve_orientations)
                    print(split_curve_ranges)
                """

                tmp_smooth_curve_list = []

                for split_curve_range in split_curve_ranges:
                    tmp_linearized_curve = LinearApproximateCurve()
                    for j in range(split_curve_range[0], split_curve_range[1] - 1):
                        tmp_linearized_curve.append(curve[j])
                    #end
                    tmp_smooth_curve_list.append( SmoothenHandler.process(tmp_linearized_curve) )
                #end

                combined_smooth_curve = CubicBezierCurve()
                for i, tmp_smooth_curve in enumerate(tmp_smooth_curve_list):
                    combined_smooth_curve.append(tmp_smooth_curve[0])
                #end
                tmp_layer.append(combined_smooth_curve)

            #end
            smooth_canvas.append(tmp_layer)
        #end

        smooth_canvas.set_view_box( linearize_canvas.view_box )

        return smooth_canvas
    #end
#end