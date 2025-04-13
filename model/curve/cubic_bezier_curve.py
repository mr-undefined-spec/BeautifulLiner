#import numpy as np

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../primitive'))
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint

from curve import Curve

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class CubicBezierCurve(Curve):
    def append(self, bezier_ctrl_p):
        if not isinstance(bezier_ctrl_p, CubicBezierCurveControlPoint):
            raise TypeError("The argument of the append method must be a CubicBezierCurveControlPoint")
        #end
        self._going_ctrl_p_list.append(bezier_ctrl_p)
    #end

#end