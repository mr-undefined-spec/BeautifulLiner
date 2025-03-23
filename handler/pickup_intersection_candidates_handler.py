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

import numpy as np

class PickupIntersectionCandidatesHandler(BasicHandler):
    @classmethod
    def process(cls, target_curve, other_curves):
        candidates = []
        for other_curve in other_curves:
            if other_curve == target_curve:
                # do nothing
                pass
            elif target_curve.rect.test_collision(other_curve.rect):
                candidates.append(other_curve)
            #end
        #end
        return candidates
    #end
#end
