
import os
import sys

#sys.path.append(os.path.join(os.path.dirname(__file__), '../model/primitive'))
#from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/curve'))
from linear_approximate_curve import LinearApproximateCurve
from broad_cubic_bezier_curve import BroadCubicBezierCurve

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
class BroadSmoothenController(BasicController):
    def __init__(self, total_step_num):
        self.total_step_num = total_step_num
    #end

    def process(self, linearize_canvas):
        smooth_canvas = Canvas()

        for layer in linearize_canvas:
            tmp_layer = Layer(layer.name)
            for step_num, curve in enumerate(layer):
                self.print_step("broad smoothen", step_num)

                curve_orientations = CurveOrientationHandler.process(curve)

                split_curve_ranges = SplitHandler.process(curve_orientations, curve.start_index)
                last_index = split_curve_ranges[-1][1]

                tmp_going_smooth_curve_list = []
                for split_curve_range in split_curve_ranges:
                    tmp_linearized_curve = LinearApproximateCurve()
                    for j in range(split_curve_range[0], split_curve_range[1] - 1):
                        tmp_linearized_curve.append(curve.going_ctrl_p_list[j])
                    #end
                    tmp_going_smooth_curve_list.append( SmoothenHandler.process(tmp_linearized_curve) )
                #end

                tmp_returning_smooth_curve_list = []
                for split_curve_range in reversed(split_curve_ranges):
                    tmp_linearized_curve = LinearApproximateCurve()
                    start = last_index - split_curve_range[1] 
                    end = last_index - split_curve_range[0] - 1
                    for j in range(start, end):
                        tmp_linearized_curve.append(curve.returning_ctrl_p_list[j])
                    #end
                    tmp_returning_smooth_curve_list.append( SmoothenHandler.process(tmp_linearized_curve) )
                #end
                

                combined_smooth_curve = BroadCubicBezierCurve()
                for tmp_going in tmp_going_smooth_curve_list:
                    combined_smooth_curve.append_going(tmp_going[0])
                #end
                for tmp_returning in tmp_returning_smooth_curve_list:
                    combined_smooth_curve.append_returning(tmp_returning[0])
                #end
                tmp_layer.append(combined_smooth_curve)

            #end
            smooth_canvas.append(tmp_layer)
        #end

        smooth_canvas.set_view_box( linearize_canvas.view_box )

        return smooth_canvas
    #end
#end