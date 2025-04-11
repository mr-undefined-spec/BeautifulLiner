
import numpy as np
from scipy.special import comb

import math
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

from rectangular import Rectangular

from pyqtree import Index

from curve import Curve

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class CubicBezierCurve(Curve):
    def append(self, bezier_ctrl_p):
        if not isinstance(bezier_ctrl_p, CubicBezierCurveControlPoint):
            raise TypeError("The argument of the append method must be a CubicBezierCurveControlPoint")
        #end
        self._going_ctlr_p_list.append(bezier_ctrl_p)
    #end

#end