
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/curve'))
from linear_approximate_curve import LinearApproximateCurve
from cubic_bezier_curve import CubicBezierCurve
from broad_linear_approximate_curve import BroadLinearApproximateCurve

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/layer'))
from layer import Layer
from canvas import Canvas

sys.path.append(os.path.join(os.path.dirname(__file__), '../handler'))
from split_handler import SplitHandler
from broaden_handler import BroadenHandler

from basic_controller import BasicController


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class BroadenController(BasicController):

    def set_broad_width(self, broad_width):
        self.broad_width = broad_width
    #end

    def __get_position(self, index_curve, len_curve):
        if len_curve == 1:
            return "first_last"
        #end

        if index_curve == 0:
            return "first"
        elif index_curve == len_curve - 1:
            return "last"
        else:
            return "middle"
        #end
    #end

    def process(self, linearize_canvas):
        broaden_handler = BroadenHandler()

        broad_canvas = Canvas()

        for layer in linearize_canvas:
            tmp_layer = Layer(layer.name)
            for step_num, curve in enumerate(layer):
                self.print_step("broaden", step_num)

                tmp_broad_curve_list = []

                curve_split_ranges = SplitHandler.process(curve, curve.start_index)

                for index_curve, the_range in enumerate(curve_split_ranges):
                    tmp_linearized_curve = LinearApproximateCurve()
                    for j in range(the_range[0], the_range[1] - 1):
                        tmp_linearized_curve.append(curve[j])
                    #end

                    position = self.__get_position(index_curve, len(curve_split_ranges))
                    tmp_broad_curve_list.append( BroadenHandler.process(tmp_linearized_curve, self.broad_width, position) )
                #end

                combined_broad_curve = BroadLinearApproximateCurve()
                for broad_curve_going in tmp_broad_curve_list:
                    for going_ctrl_p in broad_curve_going.going_ctrl_p_list:
                        combined_broad_curve.append_going(going_ctrl_p)
                    #end
                #end
                for broad_curve_returning in reversed(tmp_broad_curve_list):
                    for returning_ctrl_p in broad_curve_returning.returning_ctrl_p_list:
                        combined_broad_curve.append_returning(returning_ctrl_p)
                    #end
                #end
                #combined_broad_curve.update_start_index(curve.start_index)
                #combined_broad_curve.update_end_index(curve.end_index)
                #combined_broad_curve.set_split_ranges(curve.split_ranges)

                tmp_layer.append(combined_broad_curve)

            #end
            broad_canvas.append(tmp_layer)
        #end

        broad_canvas.set_view_box( linearize_canvas.view_box )

        return broad_canvas
    #end
#end