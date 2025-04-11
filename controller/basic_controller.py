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

sys.path.append(os.path.join(os.path.dirname(__file__), '../handler'))
from read_handler import ReadHandler
from linearize_handler import LinearizeHandler
from curve_orientation_handler import CurveOrientationHandler
from split_handler import SplitHandler
from broaden_handler import BroadenHandler

class BasicController():
    def initialize(self):
        self.total_step_num = 0
        self.step_offset = 0
    #end

    def set_total_step_num(self, total_step_num):
        self.total_step_num = total_step_num
    #end

    def set_step_offset(self, step_offset):
        self.step_offset = step_offset
    #end

    def print_step(self, step_name, step_num):
        print("{} {} / {}".format(step_name, step_num + 1 + self.step_offset, self.total_step_num))
    #end
#end
