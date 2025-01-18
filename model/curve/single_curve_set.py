import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/curve'))
from curve import Curve

from curve_set import CurveSet

class SingleCurveSet(CurveSet):
    def __init__(self, curve):
        super().__init__()
        
        if not isinstance(curve, Curve):
            raise TypeError("The argument of the append method must be a Curve(CubicBezierCurve or LinearApproximateCurve)")
        #end if
        self._data.append(curve)
    #end

#end
