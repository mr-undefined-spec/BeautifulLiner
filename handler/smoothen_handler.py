import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../model/curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../model/layer'))

from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from linear_approximate_curve import LinearApproximateCurve
from cubic_bezier_curve import CubicBezierCurve

from layer import Layer
from layer_set import LayerSet

from basic_handler import BasicHandler

import numpy as np

from scipy.special import comb

class SmoothenHandler():

    @staticmethod
    def __get_bernstein_polynomial(n, t, k):
        """ Bernstein polynomial when a = 0 and b = 1. """
        return t ** k * (1 - t) ** (n - k) * comb(n, k)
    #end

    @staticmethod
    def __get_bernstein_matrix(degree, T):
        """ Bernstein matrix for Bezier curves. """
        matrix = []
        for t in T:
            row = []
            for k in range(degree + 1):
                row.append( SmoothenHandler.__get_bernstein_polynomial(degree, t, k) )
            #end
            matrix.append(row)
        #end
        return np.array(matrix)
    #end

    @staticmethod
    def __least_square_fit(points, M):
        M_ = np.linalg.pinv(M)
        return np.matmul(M_, points)
    #end

    @staticmethod
    def process(linear_approximate_curve):
        """ Least square qbezier fit using penrose pseudoinverse.

        Based on https://stackoverflow.com/questions/12643079/b%C3%A9zier-curve-fitting-with-scipy
        and probably on the 1998 thesis by Tim Andrew Pastva, "Bezier Curve Fitting".
        """

        degree = 3 # only cubic bezier curve

        x_array = []
        y_array = []
        ctrl_p_set = linear_approximate_curve.get_ctrl_p_set()

        x_array.append( ctrl_p_set[0].start.x )
        y_array.append( ctrl_p_set[0].start.y )
        for ctrl_p in ctrl_p_set:
            x_array.append( ctrl_p.end.x )
            y_array.append( ctrl_p.end.y )
        #end

        x_data = np.array(x_array)
        y_data = np.array(y_array)

        T = np.linspace(0, 1, len(x_data))
        M = SmoothenHandler.__get_bernstein_matrix(degree, T)
        points = np.array(list(zip(x_data, y_data)))

        fit = SmoothenHandler.__least_square_fit(points, M).tolist()

        first_point = Point(x_data[0], y_data[0] )
        last_point  = Point(x_data[-1], y_data[-1] )

        cubic_bezier_curve = CubicBezierCurve()
        cubic_bezier_curve.append( CubicBezierCurveControlPoint(first_point, Point(fit[1][0], fit[1][1]), Point(fit[2][0], fit[2][1]), last_point) )
        return cubic_bezier_curve

        #return CubicBezierCurveControlPoint(first_point, Point(fit[1][0], fit[1][1]), Point(fit[2][0], fit[2][1]), last_point)
    #end

#end