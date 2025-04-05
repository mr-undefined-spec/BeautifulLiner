import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../model/curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../model/layer'))

from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from linear_approximate_curve import LinearApproximateCurve

from layer import Layer
from layer_set import LayerSet

from basic_handler import BasicHandler

class SplitHandler(BasicHandler):

    @staticmethod
    def process(curve_orientations, index_offset):
        split_curve_ranges = []
        current_value = curve_orientations[0]

        pre_index= 0

        for i, value in enumerate(curve_orientations):
            if value != current_value:
                split_curve_ranges.append((pre_index + index_offset, i + index_offset))
                pre_index = i
                current_value = value
            #end
        #end

        split_curve_ranges.append((pre_index + index_offset, len(curve_orientations) + index_offset))  # 最後の区間を追加
        return split_curve_ranges
    #end
#end
