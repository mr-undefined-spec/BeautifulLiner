import math
import numpy as np

#import os
#import sys
#sys.path.append(os.path.join(os.path.dirname(__file__), '../model/primitive'))

import numpy as np
from handler.basic_handler import BasicHandler
from handler.cohandler.curve_orientation_cohandler import CurveOrientationCohandler
from handler.cohandler.split_range_cohandler import SplitRangeCohandler

class SplitHandler(BasicHandler):

    @staticmethod
    def __create_curve_orientations(curve):
        points = curve.get_points()
        if len(points) < 30:
            return np.ones(len(points))
        # end if

        skip_size = max(1, int(len(points) * 0.1))

        if CurveOrientationCohandler.are_points_almost_linear(points, skip_size):
            return np.ones(len(points))
        # end if

        return CurveOrientationCohandler.create_curve_orientations(points, skip_size)
    # end __create_curve_orientations

    @staticmethod
    def process(curve, index_offset):
        points = curve.get_points()
        curve_orientations = SplitHandler.__create_curve_orientations(curve)
        curve_orientations = CurveOrientationCohandler.smooth_and_remove_noise(curve_orientations)
        once_split_curve_ranges = SplitRangeCohandler.create_split_ranges(curve_orientations, 0)

        split_curve_ranges = []
        for r in once_split_curve_ranges:
            if r[1] - r[0] < 30:
                split_curve_ranges.append((r[0] + index_offset, r[1] + index_offset))
                continue
            # end if

            ratio = 0.1
            min_idx = r[0] + int((r[1] - r[0]) * ratio)
            max_idx = r[1] - int((r[1] - r[0]) * ratio)

            split_idx = SplitRangeCohandler.find_split_point_by_angle(points, r[0], r[1], 90.0)
            if split_idx != -1 and min_idx < split_idx < max_idx:
                split_curve_ranges.append((r[0] + index_offset, split_idx + index_offset))
                split_curve_ranges.append((split_idx + 1 + index_offset, r[1] + index_offset))
            else:
                split_curve_ranges.append((r[0] + index_offset, r[1] + index_offset))
            # end if
        # end for

        return split_curve_ranges
    # end process

# end SplitHandler