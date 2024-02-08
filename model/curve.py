
import numpy as np
from scipy.special import comb

import math
from point import Point
from control_point import CubicBezierCurveControlPoint
from control_point import LinearApproximateCurveControlPoint

from rectangular import Rectangular

class Curve:
    def __init__(self):
        self._going_ctrl_p_set = []
        self.__intersect_judge_rectangular = None
        self._start_index = 0
        self._end_index   = -1
    #end

    def get_the_end(self):
        # if self._end_index is initial state, then ...
        if (self._end_index == -1):
            return len(self._going_ctrl_p_set) 
        #end
        # if self._end_index is over the array size
        if ( self._end_index >= len(self._going_ctrl_p_set) ):
            return len(self._going_ctrl_p_set)
        #end
        # others, self._end_index is correct
        return self._end_index
    #end

    def __getitem__(self, i):
        return self._going_ctrl_p_set[i]
    #end

    def __iter__(self):
        self._index = 0
        return self
    #end
    def __next__(self):
        if self._index >= len(self._going_ctrl_p_set): raise StopIteration
        self._index += 1
        return self._going_ctrl_p_set[self._index-1]
    #end

    def __len__(self):
        return len(self._going_ctrl_p_set)
    #end

    def create_intersect_judge_rectangle(self):
        min_x = self._going_ctrl_p_set[0].get_min_x()
        max_x = self._going_ctrl_p_set[0].get_max_x()
        min_y = self._going_ctrl_p_set[0].get_min_y()
        max_y = self._going_ctrl_p_set[0].get_max_y()
        for ctrl_p in self._going_ctrl_p_set:
            min_x = min( min_x, ctrl_p.get_min_x() )
            max_x = max( max_x, ctrl_p.get_max_x() )
            min_y = min( min_y, ctrl_p.get_min_y() )
            max_y = max( max_y, ctrl_p.get_max_y() )
        #end
        self.__intersect_judge_rectangular = Rectangular(min_x, max_x, min_y, max_y)
    #end

    @property
    def rect(self):
        return self.__intersect_judge_rectangular
    #end

    def to_svg(self):
        s = ""
        for i, ctrl_p in enumerate(self._going_ctrl_p_set):
            s += ctrl_p.to_svg(i==0)
        #end
        return s
    #end
#end

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class CubicBezierCurve(Curve):
    def append(self, bezier_ctrl_p):
        if not type(bezier_ctrl_p) is CubicBezierCurveControlPoint:
            raise TypeError("The argument of the append method must be a CubicBezierCurveControlPoint")
        #end
        self._going_ctrl_p_set.append(bezier_ctrl_p)
    #end

    # 
    # The Algorithm
    #                                                                                                                                        
    # 0. Background.
    #    Cubic Bezier curve is the point sequence which is calculated by three-step linear interpolation of 4 control points.
    #
    #    Step 1. Get Q0 ~ Q2 by linear interpolation of 4 control points(P0 ~ P3)
    #    Step 2. Get R0 and R1 by linear interpolation of Step1 points(Q0 ~ Q2)
    #    Step 3. Get @ by linear interpolation of Step2 points(R0 and R1)
    #
    #    (More detail, see wikicommons https://commons.wikimedia.org/wiki/File:Bezier_cubic_anim.gif
    #     and wikipedia https://en.wikipedia.org/wiki/B%C3%A9zier_curve)
    #                                                                                                                                        
    #    P1 ...........Q1........................................   P2
    #     __          x  ooooo                                         `
    #      __        x        ooooooooooR1oooooooooooooooooo           ``
    #       _        x            """""""                  oooooooooo    ``
    #        _       x        """""     *****************           oooooo Q2 
    #         _     x      """""*********               **********           `` 
    #          _    x   """" ****                                 ******       `` 
    #          _    x ""  @**                                           ******   ``
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
    #                                                                                                                                        
    #    where P0 ~ P3 are 4 control points of cubic Bezier curve
    #          Q0 ~ Q2 are interpolation points of P0 ~ P3
    #          R0 ~ R1 are interpolation points of Q0 ~ Q2
    #
    #          _ : The line between P0 and P1
    #          . : The line between P1 and P2
    #          ` : The line between P2 and P3
    #          x : The line between Q0 and Q1
    #          o : The line between Q1 and Q2
    #          " : The line between R0 and R1
    #
    #          @ : The point on cubic Bezier curve at current timing
    #
    #          * : The final resulting cubic Bezier curve
    #                                                                                                                                        
    # 1. First, this algorithm computes the Q0 , Q1 and Q2 Points(lists), which are equally divided from P0 to P1 , P1 to P2 and P2 to P3, respectively.         
    #                                                                                                                                        
    #                                                                                                                                        
    #                    Q1 Points
    #                  +-----------------------------------------------------------+                                                         
    #                  |                                                           |                                                         
    #                                                                                                                                        
    #                  P1 .....................................................   P2
    #             +--   __                                                           `  -------------------------------+
    #             |      __                                                          ``                                |
    #             |       _                                                            ``                              | Q2 Points
    #             |        _                          *****************                  ``                            | 
    #  Equally    |         _                 *********               **********           ``                          |
    #  divided    |          _             ****                                 ******       ``                        |
    #  Q0 Points  |          _          ***                                           ******   ``                      |
    #  (list)     |           _       ***                                                  ***** ```                   |
    #  on the     |           __     **                                                         *** ``                 |
    #  line of    |            _    **                                                            *** ``               |
    #  P0 to P1   |             _  **                                                               **  ``             |
    #             |             __ *                                                                 **  ``            |
    #             |             __ *                                                                  ***  ``          |
    #             |               _*                                                                    ***  ```       |
    #             |         `     _*                                                                      ***  ``      |
    #             |                _*                                                                            P3  --+
    #             +--                                                                         
    #                              P0                                                        
    #                                                                                                                                        
    #                                                                                                                                        
    #                                                                                                                                        
    # 2. Then, it computes the r0 and r1 points from  q0, q1 and q2 , which are the N-th list element of the Q0, Q1 and Q2 Points.
    #    r0 and r1 points are also the N-th list element of R0 and R1 Points, which are equally divided from Q0 to Q1 and Q1 to Q2, respectively.     
    #
    #    It is important to note that r0 and r1 are the N-th elements of the list, as are q0, q1 and q2.
    #
    #    Since both the "Q0, Q1 and Q2 Points" and "R0 and R1 Points" are point sequences that divide the line segment into equal parts, 
    #    the point r0 is the point that divides line q0q1 into |P0q0|:|q0P1|, where |P0q0| is the distance between P0 and q0.
    #    The point r1 can be calculated in the same way.
    #
    #    In other words, it is not necessary to calculate the R0 and R1 lists, and it is sufficient to calculate the internal division point.
    #    
    #                                                                                                                                        
    #    P1 ...........q1........................................   P2
    #     __          x  ooooo                                         `
    #      __        x        ooooooooor1ooooooooooooooooooo           ``
    #       _        x                                     ooooooooo    ``
    #        _       x                  *****************           oooooo q2 
    #         _     x           *********               **********           `` 
    #          _    x        ****                                 ******       `` 
    #          _    x     ***                                           ******   ``
    #           _   r0  ***                                                  ***** ```
    #           __ x   **                                                         *** ``
    #            _ x  **                                                            *** ``
    #             _x **                                                               **  ``
    #             __ *                                                                 **  ``
    #             q0 *                                                                  ***  ``
    #               _*                                                                    ***  ```
    #               _*                                                                      ***  ``
    #                _*                                                                            P3
    #                                                                           
    #                P0                                                        
    #                                                                                                                                        
    # 3. Finaly, it computes the @ point which is the point that diveded line r0r1 into |P0q0|:|q0P1|
    #
    #    P1 ...........q1........................................   P2
    #     __          x  ooooo                                         `
    #      __        x        oooooooooor1oooooooooooooooooo           ``
    #       _        x            """""""                  oooooooooo    ``
    #        _       x        """""     *****************           oooooo q2 
    #         _     x      """""*********               **********           `` 
    #          _    x   """" ****                                 ******       `` 
    #          _    x ""  @**                                           ******   ``
    #           _   r0  ***                                                  ***** ```
    #           __ x   **                                                         *** ``
    #            _ x  **                                                            *** ``
    #             _x **                                                               **  ``
    #             __ *                                                                 **  ``
    #             q0 *                                                                  ***  ``
    #               _*                                                                    ***  ```
    #               _*                                                                      ***  ``
    #                _*                                                                            P3
    #                                                                           
    #                P0                                                        
    #
    # 4. If the division num of Q0, Q1 and Q2 Points is large enough, the resulting point sequence can approximate a cubic Bezier curve with sufficient accuracy.
    #
    
    def __get_division_num(self, ctrl_p, micro_segment_length):
        length_p0_p1 = ctrl_p.p0.distance(ctrl_p.p1)
        length_p1_p2 = ctrl_p.p1.distance(ctrl_p.p2)
        length_p2_p3 = ctrl_p.p2.distance(ctrl_p.p3)
    
        division_num_p0_p1 = math.ceil(length_p0_p1 / micro_segment_length)
        division_num_p1_p2 = math.ceil(length_p1_p2 / micro_segment_length)
        division_num_p2_p3 = math.ceil(length_p2_p3 / micro_segment_length)
    
        return max(division_num_p0_p1, division_num_p1_p2, division_num_p2_p3)
    #end
    
    #
    #  point_a                         point_b
    #  |                               |
    #  V                               V
    #
    #  A---x---x---x---x---x---x---x---B
    #  
    #  |                               |
    #  +-------------------------------+
    #     return_points
    #
    #   Note!
    #     The length of return_points is "division_num + 1"
    #
    def __get_equally_divided_points_between_2_points(self, point_a, point_b, division_num):
        delta_x = (point_b.x - point_a.x) / float(division_num)
        delta_y = (point_b.y - point_a.y) / float(division_num)
    
        return_points = []
        for i in range(division_num):
            return_points.append(  Point( point_a.x + delta_x*float(i), point_a.y + delta_y*float(i) )  )
        #end
        return_points.append(point_b)
    
        return return_points
    #end
    
    #
    #  point_a                         point_b
    #  |                               |
    #  V                               V
    #
    #  A-------@-----------------------B
    #     return_point
    #  
    #  |<----->|<--------------------->|
    #      m   :           n
    #
    #
    def __get_internal_divided_point(self, point_a, point_b, ratio_m, ratio_n):
        x = ( point_a.x*ratio_n + point_b.x*ratio_m ) / (ratio_m + ratio_n)
        y = ( point_a.y*ratio_n + point_b.y*ratio_m ) / (ratio_m + ratio_n)
        return Point(x, y)
    #end
    
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
    #                     * = return_points
    #
    def __approximate_linear_curve(self, ctrl_p, is_first, micro_segment_length):
        division_num = self.__get_division_num(ctrl_p, micro_segment_length)
    
        q0_list = self.__get_equally_divided_points_between_2_points(ctrl_p.p0, ctrl_p.p1, division_num)
        q1_list = self.__get_equally_divided_points_between_2_points(ctrl_p.p1, ctrl_p.p2, division_num)
        q2_list = self.__get_equally_divided_points_between_2_points(ctrl_p.p2, ctrl_p.p3, division_num)
    
        return_points = []
        if division_num == 1:
            if is_first:
                return_points.append( Point(ctrl_p.p0.x, ctrl_p.p0.y) )
            #end
            return_points.append( Point(ctrl_p.p3.x, ctrl_p.p3.y) )
        else:
            start = 0 if is_first else 1
            for i in range(start, division_num+1):
                q0 = q0_list[i]
                q1 = q1_list[i]
                q2 = q2_list[i]
    
                ratio_n = float(i)
                ratio_m = float(division_num - i)
    
                r0 = self.__get_internal_divided_point(q0, q1, ratio_n, ratio_m)
                r1 = self.__get_internal_divided_point(q1, q2, ratio_n, ratio_m)
    
                return_points.append( self.__get_internal_divided_point(r0, r1, ratio_n, ratio_m) )
            #end
        #end
    
        return return_points
    #end
    
    def linearize(self, micro_segment_length):
        linear_approximate_curve = LinearApproximateCurve()
        for i, ctrl_p in enumerate(self._going_ctrl_p_set):
            points = []
            for point in self.__approximate_linear_curve(ctrl_p, i==0, micro_segment_length):
                points.append( point )
            #end
            for j in range( len(points)-1 ):
                linear_approximate_curve.append( LinearApproximateCurveControlPoint(points[j], points[j+1]) )
            #end
        #end
        return linear_approximate_curve
    #end
#end

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class LinearApproximateCurve(Curve):
    def __init__(self):
        super().__init__()
    #end

    def append(self, linear_ctrl_p):
        if not type(linear_ctrl_p) is LinearApproximateCurveControlPoint:
            raise TypeError("The argument of the append method must be a LinearApproximateCurveControlPoint")
        #end
        self._going_ctrl_p_set.append(linear_ctrl_p)
    #end

    def to_svg(self):
        s = ""
        the_end = self.get_the_end()
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

        ## not support now
        ##if len(x_array)==0:
        ##    return None
        ###end
        ##if len(x_array)==1:
        ##    point = curve[ curve.end_index - 1 ]
        ##    x_array.append( float( point.x_array ) )
        ##    y_array.append( float( point.y_array ) )
        ###end
        ##if len(x_array) < degree + 1:
        ##    x_array.insert(1, (x_array[0] + x_array[1])/2.0 )
        ##    y_array.insert(1, (y_array[0] + y_array[1])/2.0 )
        ##    x_array.insert(1, (x_array[0] + x_array[1])/2.0 )
        ##    y_array.insert(1, (y_array[0] + y_array[1])/2.0 )
        ##    x_array.insert(1, (x_array[0] + x_array[1])/2.0 )
        ##    y_array.insert(1, (y_array[0] + y_array[1])/2.0 )
        ###end
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
        """ In LinearApproximateCurve class, public smoothen method calls only one protected _smoothen method
        On the other hand, in BroadLinearApproximateCurve class, public smoothen method calls two protected _smoothen methods(going & returning)"""
        cubic_bezier_curve = CubicBezierCurve()
        the_end = self.get_the_end()
        cubic_bezier_curve.append( self._smoothen(self._going_ctrl_p_set, self._start_index, the_end) )
        return cubic_bezier_curve
    #end

    def update_start_end_index_with_intersection(self, other_curve, ratio):
        the_end_of_start_side_index = int( len(self._going_ctrl_p_set)*ratio )
        for i in range( self._start_index, the_end_of_start_side_index ):
            the_segment = self._going_ctrl_p_set[i]
            for other_segment in other_curve:
                if the_segment.is_intersection(other_segment):
                    self._start_index = i
                #end
            #end
        #end

        the_start_of_end_side_index = int( len(self._going_ctrl_p_set)*(1.0-ratio) )
        the_end = self.get_the_end()
        for i in range( the_start_of_end_side_index, the_end ):
            the_segment = self._going_ctrl_p_set[i]
            for other_segment in other_curve:
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
        broad_curve = BroadLinearApproximateCurve()

        tmp_going_ctrl_p_set = self.__get_slightly_away_control_point_set(self._going_ctrl_p_set, broaden_width, True)
        tmp_returning_ctrl_p_set = self.__get_slightly_away_control_point_set(self._going_ctrl_p_set, broaden_width, False)

        broad_curve.set_ctrl_p_set(tmp_going_ctrl_p_set, tmp_returning_ctrl_p_set, self._start_index, self._end_index)

        return broad_curve
    #end

#end

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class BroadLinearApproximateCurve(LinearApproximateCurve):
    def __init__(self):
        Curve.__init__(self)
        self._returning_ctrl_p_set = []
    #end

    def set_ctrl_p_set(self, going_ctrl_p_set, returning_ctrl_p_set, start_index, end_index):
        self._going_ctrl_p_set     = going_ctrl_p_set
        self._returning_ctrl_p_set = returning_ctrl_p_set
        self._start_index          = start_index
        self._end_index            = end_index
    #end

    def smoothen(self):
        """ In LinearApproximateCurve, public smoothen method calls only one protected _smoothen method
        On the other hand, in BroadLinearApproximateCurve, public smoothen method calls two protected _smoothen methods(going & returning)"""
        the_end = self.get_the_end()
        going_smooth_ctrl_p = self._smoothen(self._going_ctrl_p_set, self._start_index, the_end)

        returning_start = len(self._returning_ctrl_p_set) - the_end 
        returning_end   = len(self._returning_ctrl_p_set) - self._start_index 
        returning_smooth_ctrl_p = self._smoothen(self._returning_ctrl_p_set, returning_start, returning_end)

        broad_cubic_bezier_curve = BroadCubicBezierCurve()
        broad_cubic_bezier_curve.set_ctrl_p(going_smooth_ctrl_p, returning_smooth_ctrl_p)
        return broad_cubic_bezier_curve
    #end

    def to_svg(self):
        s = ""
        the_end = self.get_the_end()
        for i in range( self._start_index, the_end ):
            ctrl_p = self._going_ctrl_p_set[i]
            s += ctrl_p.to_svg(i==self._start_index)
        #end

        returning_start = len(self._returning_ctrl_p_set) - the_end 
        returning_end   = len(self._returning_ctrl_p_set) - self._start_index 

        #print( self._start_index, self._end_index, returning_start, returning_end )
        for i in range( returning_start, returning_end):
            if i == len(self._returning_ctrl_p_set)-1:
                break
            ctrl_p = self._returning_ctrl_p_set[i]
            s += ctrl_p.to_svg(False)
        #end
        s += "Z"
        return s
    #end
#end

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class BroadCubicBezierCurve(CubicBezierCurve):
    def __init__(self):
        Curve.__init__(self)
        self._returning_ctrl_p_set = []
    #end

    def set_ctrl_p(self, going_ctrl_p, returning_ctrl_p):
        """ Curve has many control points, but BroadCubicBezierCurve has ONLY ONE control point in each going & returning."""
        self._going_ctrl_p_set     = [going_ctrl_p]
        self._returning_ctrl_p_set = [returning_ctrl_p]
    #end

    def to_svg(self):
        s = ""
        s += self._going_ctrl_p_set[0].to_svg(True)
        s += self._returning_ctrl_p_set[0].to_svg(False, True)
        s += "Z"
        return s
    #end
#end
