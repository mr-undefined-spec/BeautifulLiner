
import numpy as np
from scipy.special import comb

import math
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

from rectangular import Rectangular

from pyqtree import Index

from curve import Curve

class LinearApproximateCurve(Curve):
    def __init__(self):
        super().__init__()
        self.qtree_ctrl_p_set = None
    #end

    def append(self, linear_ctrl_p):
        if not type(linear_ctrl_p) is LinearApproximateCurveControlPoint:
            raise TypeError("The argument of the append method must be a LinearApproximateCurveControlPoint")
        #end
        self._going_ctrl_p_set.append(linear_ctrl_p)
    #end

    def to_svg(self):
        s = ""
        the_end = self._get_the_end()
        for i in range( self._start_index, the_end ):
            ctrl_p = self._going_ctrl_p_set[i]
            s += ctrl_p.to_svg(i==self._start_index)
        #end
        return s
    #end

    def __get_bernstein_polynomial(self, n, t, k):
        """ Bernstein polynomial when a = 0 and b = 1. """
        return t ** k * (1 - t) ** (n - k) * comb(n, k)
    #end

    def __get_bernstein_matrix(self, degree, T):
        """ Bernstein matrix for Bezier curves. """
        matrix = []
        for t in T:
            row = []
            for k in range(degree + 1):
                row.append( self.__get_bernstein_polynomial(degree, t, k) )
            #end
            matrix.append(row)
        #end
        return np.array(matrix)
    #end

    def __least_square_fit(self, points, M):
        M_ = np.linalg.pinv(M)
        return np.matmul(M_, points)
    #end

    def _smoothen(self, ctrl_p_set, start_index, the_end):
        """ Least square qbezier fit using penrose pseudoinverse.

        Based on https://stackoverflow.com/questions/12643079/b%C3%A9zier-curve-fitting-with-scipy
        and probably on the 1998 thesis by Tim Andrew Pastva, "Bezier Curve Fitting".
        """

        degree = 3 # only cubic bezier curve

        x_array = []
        y_array = []

        x_array.append( ctrl_p_set[start_index].s.x )
        y_array.append( ctrl_p_set[start_index].s.y )
        for i in range( start_index, the_end ):
            x_array.append( ctrl_p_set[i].e.x )
            y_array.append( ctrl_p_set[i].e.y )
        #end

        x_data = np.array(x_array)
        y_data = np.array(y_array)

        T = np.linspace(0, 1, len(x_data))
        M = self.__get_bernstein_matrix(degree, T)
        points = np.array(list(zip(x_data, y_data)))

        fit = self.__least_square_fit(points, M).tolist()

        first_point = Point(x_data[0], y_data[0] )
        last_point  = Point(x_data[-1], y_data[-1] )

        return CubicBezierCurveControlPoint(first_point, Point(fit[1][0], fit[1][1]), Point(fit[2][0], fit[2][1]), last_point)
    #end

    def smoothen(self):
        from cubic_bezier_curve import CubicBezierCurve
        """ In LinearApproximateCurve class, public smoothen method calls only one protected _smoothen method
        On the other hand, in BroadLinearApproximateCurve class, public smoothen method calls two protected _smoothen methods(going & returning)"""
        cubic_bezier_curve = CubicBezierCurve()
        the_end = self._get_the_end()
        cubic_bezier_curve.append( self._smoothen(self._going_ctrl_p_set, self._start_index, the_end) )
        return cubic_bezier_curve
    #end

    def create_qtree_ctrl_p_set(self, bbox):
        self.qtree_ctrl_p_set = Index(bbox=bbox)

        for ctrl_p in self._going_ctrl_p_set:
            rect_tuple = ctrl_p.get_rect_tuple()
            self.qtree_ctrl_p_set.insert(ctrl_p, rect_tuple)
        #end
    #end

    def get_intersect_segment_set(self, target_rect_tuple):
        return self.qtree_ctrl_p_set.intersect(target_rect_tuple)
    #end

    def update_start_end_index_with_intersection(self, other_curve, ratio):
        the_end_of_start_side_index = int( len(self._going_ctrl_p_set)*ratio )
        for i in range( self._start_index, the_end_of_start_side_index ):
            the_segment = self._going_ctrl_p_set[i]
            the_rect_tuple = the_segment.get_rect_tuple()
            for other_segment in other_curve.get_intersect_segment_set(the_rect_tuple):
                if the_segment.is_intersection(other_segment):
                    self._start_index = i
                #end
            #end
        #end

        the_start_of_end_side_index = int( len(self._going_ctrl_p_set)*(1.0-ratio) )
        the_end = self._get_the_end()
        for i in range( the_start_of_end_side_index, the_end ):
            the_segment = self._going_ctrl_p_set[i]
            the_rect_tuple = the_segment.get_rect_tuple()
            for other_segment in other_curve.get_intersect_segment_set(the_rect_tuple):
                if the_segment.is_intersection(other_segment):
                    self._end_index = i
                #end
            #end
        #end

    #end 

    # 
    # The Algorithm
    #                                                                                                                                        
    # 0. Prerequisite
    #
    #  Cubic Bezier curves are approximated by line segments with linearize method in CubicBezierCurve
    #   
    #    P1 ...........Q1........................................   P2
    #     __          x  ooooo                                         `
    #      __        x        ooooooooooR1oooooooooooooooooo           ``
    #       _        x            """""""                  oooooooooo    ``
    #        _       x        """""     *****************           oooooo Q2 
    #         _     x      """""*********               **********           `` 
    #          _    x   """" ****                                 ******       `` 
    #          _    x ""  ***                                           ******   ``
    #           _   R0  ***                                                  ***** ```
    #           __ x   **                                                         *** ``
    #            _ x  **                                                            *** ``
    #             _x **                                                               **  ``
    #             __ *                                                                 **  ``
    #             Q0 *                                                                  ***  ``
    #               _*                                                                    ***  ```
    #               _*                                                                      ***  ``
    #                _*                                                                            P3
    #                                                                           
    #                P0                                                        
    #                     * = Points (= Both ends of a line segment)
    #
    #
    #
    #
    # This method broaden line as below
    #
    #
    #  A ******************************************* B
    #
    #                     |
    #                     V
    #
    #                    ************       
    #            ***************************
    #       *************************************
    #  A ******************************************* B
    #       *************************************
    #            ***************************
    #                    ************       
    #
    #
    # Line AB consists of multiple line segments
    #
    #  A o****o******o****o*******o**o****o***o****o B
    #
    # Now turn attention to the line segments at the first two points
    #
    #    This! 
    #    |
    #    V
    #    +----+
    #    |    |
    #  A o****o******o****o*******o**o****o***o****o B
    #
    # Consider it a vector
    #
    #  A o---->******o****o*******o**o****o***o****o B
    #
    # Rotate 90 degrees from the focused vector and find a point slightly away from it.
    #
    #  A o---->******o****o*******o**o****o***o****o B
    #         |
    #         V
    #         x
    #       
    # Compute sameway in the second, third ... line segment
    #
    #  A o---->------>****o*******o**o****o***o****o B
    #         |      |    |       |  |    |   |    |
    #         V      V    V       V  V    V   V    V
    #         x      x    x       x  x    x   x    x
    #       
    # The distance delta from the original line is a position-dependent function.
    # These are small deltas at both ends and large in the center.      
    #       
    #  A o---->------>****o*******o**o****o***o****o B
    #         |      |    |       |  |    |   |    |
    #         V      |    |       |  |    |   |    V
    #         x      V    V       |  |    V   V    x
    #                x    x       V  V    x   x    
    #                             x  x
    #       
    # By calculating this on both sides, a thin line at both ends and a thick line in the center can be obtained.
    #       
    #       
    #                             x  x
    #                x    x       A  A    x   x
    #         x      A    A       |  |    A   A    x
    #         A      |    |       |  |    |   |    A
    #         |      |    |       |  |    |   |    |
    #  A o****o******o****o*******o**o****o***o****o B
    #         |      |    |       |  |    |   |    |
    #         V      |    |       |  |    |   |    V
    #         x      V    V       |  |    V   V    x
    #                x    x       V  V    x   x    
    #                             x  x
    #       
    
    def __get_delta_point(self, prev_point, current_point, delta):
        vec_x = current_point.x - prev_point.x
        vec_y = current_point.y - prev_point.y
        len_vec = math.sqrt( vec_x*vec_x + vec_y*vec_y )
        if len_vec == 0:
            return None
        #end
    
        final_x = current_point.x - ( vec_y * delta/len_vec)
        final_y = current_point.y + ( vec_x * delta/len_vec)
        return Point(final_x, final_y)
    #end 

    def __get_slightly_away_control_point_set(self, ctrl_p_set, broaden_width, is_going):
        slightly_away_control_point_set = []


        points = []
        if is_going:
            for ctrl_p in ctrl_p_set:
                points.append(ctrl_p.s)
            #end
            points.append(ctrl_p_set[-1].e)
        else: # is returning
            reversed_ctrl_p_set = list( reversed(ctrl_p_set) )
            for ctrl_p in reversed_ctrl_p_set:
                points.append(ctrl_p.e)
            #end
            points.append(reversed_ctrl_p_set[-1].s)
        #end
    
        half_length = len(points)/2.0 - 0.5 
    
        # first point is equal to original first point
        last_slightly_away_point = points[0]
    
        # middle points are slightly away points
        for i in range( len(points) - 2 ):
            delta = broaden_width * ( half_length - abs(half_length - i - 1) ) / half_length
            delta += 0.5
            prev_point = points[i]
            current_point = points[i+1]
            slightly_away_point = self.__get_delta_point(prev_point, current_point, delta)
            if slightly_away_point is not None:
                the_ctrl_p = LinearApproximateCurveControlPoint(last_slightly_away_point, slightly_away_point)
                slightly_away_control_point_set.append(the_ctrl_p)
                last_slightly_away_point = slightly_away_point
            #end
        #end
    
        # last point is equal to original last point
        the_ctrl_p = LinearApproximateCurveControlPoint(last_slightly_away_point, points[-1])
        slightly_away_control_point_set.append( the_ctrl_p )
    
        return slightly_away_control_point_set
    #end 

    def broaden(self, broaden_width):
        from broad_linear_approximate_curve import BroadLinearApproximateCurve
        broad_curve = BroadLinearApproximateCurve()

        tmp_going_ctrl_p_set = self.__get_slightly_away_control_point_set(self._going_ctrl_p_set, broaden_width, True)
        tmp_returning_ctrl_p_set = self.__get_slightly_away_control_point_set(self._going_ctrl_p_set, broaden_width, False)

        broad_curve.set_ctrl_p_set(tmp_going_ctrl_p_set, tmp_returning_ctrl_p_set, self._start_index, self._end_index)

        return broad_curve
    #end

#end