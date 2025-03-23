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
from scipy.optimize import minimize

class CurveOrientationHandler(BasicHandler):

    @classmethod
    def get_curve_orientations(cls, curve):
        """
        Curveの離散的な点列に基づいて相対的な回転関係（時計回りか反時計回りか）を計算する
        """
        points = curve.get_points()
        #print(points)

        curve_orientations = []

        # 点列を3点ずつ取り出す
        for i in range(1, len(points) - 1):
            p1, p2, p3 = points[i - 1], points[i], points[i + 1]
            
            # ベクトルを計算
            #v1 = p2 - p1
            #v2 = p3 - p2
            v1 = [p2.x - p1.x, p2.y - p1.y]
            v2 = [p3.x - p2.x, p3.y - p2.y]
            
            # 外積の大きさ（曲率の分子）を計算
            cross_product = np.cross(v1, v2)
            
            if cross_product > 0:
                curve_orientations.append(1.0)
            else:
                curve_orientations.append(-1.0)
            #end
            #curve_orientations.append(curvature)
        #end

        first_element = curve_orientations[0]
        last_element = curve_orientations[-1]
        curve_orientations.insert(0, first_element)
        curve_orientations.append(last_element)
        
        return np.array(curve_orientations)
    #end
#end
