
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/layer'))
from layer import Layer
from canvas import Canvas

sys.path.append(os.path.join(os.path.dirname(__file__), '../handler'))
from curve_orientation_handler import CurveOrientationHandler
from split_handler import SplitHandler
from broaden_handler import BroadenHandler

from basic_controller import BasicController


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class BroadenController(BasicController):
    def __init__(self, total_step_num):
        self.total_step_num = total_step_num
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

    def process(self, linearize_canvas, broaden_width):
        broaden_handler = BroadenHandler()

        broad_canvas = Canvas()

        for layer in linearize_canvas:
            tmp_layer = Layer(layer.name)
            for step_num, curve in enumerate(layer):
                self.print_step("broaden", step_num)

                curve_orientations = CurveOrientationHandler.process(curve)
                split_curve_ranges = SplitHandler.process(curve_orientations, curve.start_index)

                for index_curve, split_curve_range in enumerate(split_curve_ranges):
                    position = self.__get_position(index_curve, len(split_curve_ranges))
                    broad_curve = BroadenHandler.process(curve, broaden_width, position)
                #end

                tmp_layer.append(broad_curve)

            #end
            broad_canvas.append(tmp_layer)
        #end

        broad_canvas.set_view_box( linearize_canvas.view_box )

        return broad_canvas
    #end
#end