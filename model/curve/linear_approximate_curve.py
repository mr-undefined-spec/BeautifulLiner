
import numpy as np
from scipy.special import comb

import math
from point import Point
from vector import Vector
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

from rectangular import Rectangular

from pyqtree import Index

from curve import Curve

class LinearApproximateCurve(Curve):
    def __init__(self):
        super().__init__()

        self.min_x = 999999
        self.max_x = -999999
        self.min_y = 999999
        self.max_y = -999999

        self._start_index = 0
        self._end_index   = -1
    #end

    def _get_the_end(self):
        # if self._end_index is initial state, then ...
        if (self._end_index == -1):
            return len(self._ctrl_p_set) 
        #end
        # if self._end_index is over the array size
        if ( self._end_index >= len(self._ctrl_p_set) ):
            return len(self._ctrl_p_set)
        #end
        # others, self._end_index is correct
        return self._end_index
    #end

    def append(self, linear_ctrl_p):
        if not isinstance(linear_ctrl_p, LinearApproximateCurveControlPoint):
            raise TypeError("The argument of the append method must be a LinearApproximateCurveControlPoint")
        #end

        self.min_x = min(self.min_x, linear_ctrl_p.start.x, linear_ctrl_p.end.x)
        self.max_x = max(self.max_x, linear_ctrl_p.start.x, linear_ctrl_p.end.x)
        self.min_y = min(self.min_y, linear_ctrl_p.start.y, linear_ctrl_p.end.y)
        self.max_y = max(self.max_y, linear_ctrl_p.start.y, linear_ctrl_p.end.y)

        self._ctrl_p_set.append(linear_ctrl_p)
    #end

    def to_str(self):
        s = ""
        the_end = self._get_the_end()
        for i in range( self._start_index, the_end ):
            ctrl_p = self._ctrl_p_set[i]
            s += ctrl_p.to_str(i==self._start_index)
        #end
        return s
    #end

    @property
    def rect(self):
        return Rectangular(self.min_x, self.max_x, self.min_y, self.max_y)
    #end

    def get_points(self):
        points = []
        points.append(self._ctrl_p_set[self._start_index].start)

        the_end = self._get_the_end()
        for i in range( self._start_index, the_end ):
            points.append(self._ctrl_p_set[i].end)
        #end
        return points
    #end

    def copy(self, other_linear_approximate_curve):
        for ctrl_p in other_linear_approximate_curve:
            self.append(ctrl_p)
        #end
        self._start_index = other_linear_approximate_curve.start_index
        self._end_index = other_linear_approximate_curve.end_index
    #end


    def get_start_points(self):
        start_points = []
        for ctrl_p in self._ctrl_p_set:
            start_points.append(ctrl_p.start)
        #end
        return start_points
    #end

    def get_start_points_as_numpy_array(self):
        start_points = []
        for ctrl_p in self._ctrl_p_set:
            start_points.append([ctrl_p.start.x, ctrl_p.start.y])
        #end
        return np.array(start_points)
    #end

    def get_bounding_boxes(self):
        """各線分に対し、軸平行境界ボックス(AABB)を取得"""
        return [
            (min(ctrl_p.start.x, ctrl_p.end.x), min(ctrl_p.start.y, ctrl_p.end.y), 
             max(ctrl_p.start.x, ctrl_p.end.x), max(ctrl_p.start.y, ctrl_p.end.y))
            for ctrl_p in self._ctrl_p_set
        ]
    #end

    def update_start_index(self, start_index):
        if( self._start_index < start_index ):
            self._start_index = start_index
        #end
    #end

    def update_end_index(self, end_index):
        if( self._end_index == -1):
            self._end_index = end_index
        elif( end_index < self._end_index ):
            self._end_index = end_index
        #end
    #end

    def get_ctrl_p_set(self):
        return_ctrl_p_set = []
        the_end = self._get_the_end()
        for i in range( self._start_index, the_end ):
            return_ctrl_p_set.append( self._ctrl_p_set[i] )
        #end
        return return_ctrl_p_set
    #end



    """

    def create_qtree_ctrl_p_set(self, bbox):
        
        self.qtree_ctrl_p_set = Index(bbox=bbox)

        for ctrl_p in self._ctrl_p_set:
            rect_tuple = ctrl_p.get_rect_tuple()
            self.qtree_ctrl_p_set.insert(ctrl_p, rect_tuple)
        #end
    #end


    def get_min_distance_to_point(self, point):
        min_distance = 999999
        for i, ctrl_p in enumerate(self._ctrl_p_set):
            if ctrl_p.get_distance_to_point(point) < min_distance:
                min_distance = ctrl_p.get_distance_to_point(point)
            #end
        #end

        return min_distance
    #end

    def get_ctrl_p_index_at_min_distance_to_point(self, point):
        the_index = None
        min_distance = 999999
        for i, ctrl_p in enumerate(self._ctrl_p_set):
            if ctrl_p.get_distance_to_point(point) < min_distance:
                the_index = i
                min_distance = ctrl_p.get_distance_to_point(point)
            #end
        #end

        return the_index
    #end

    def approximate_line_through_points(points):
        if len(points) < 2:
            raise ValueError("At least two points are required to define a line.")

        x_coords, y_coords = zip(*[(point.x, point.y) for point in points])
        
        A = np.vstack([x_coords, np.ones(len(x_coords))]).T
        m, c = np.linalg.lstsq(A, y_coords, rcond=None)[0]
        
        return m, c
    #end
    def generate_approximate_lines_through_points(self, points):
        lines = []
        for i in range(len(points)-1):
            x0, y0 = points[i].x, points[i].y
            x1, y1 = points[i+1].x, points[i+1].y
            m = (y1-y0)/(x1-x0)
            c = y0 - m*x0
            lines.append((m,c))
        #end
        return lines
    #end
    def calculate_angle_between_approximate_lines_through_points(self, points_a, points_b):
        line_a = self.generate_approximate_lines_through_points(points_a)
        line_b = self.generate_approximate_lines_through_points(points_b)

        m1, c1 = line_a[-1]
        m2, c2 = line_b[0]

        angle = math.atan2(m2 - m1, 1 + m1 * m2)
        return angle
    #end

    def is_continuaous_at_start_side(self, other_curve, distance_threshold):
        other_end_point = other_curve.sequential_points[-1]

        this_index_nearest_other_end_point = self.get_ctrl_p_index_at_min_distance_to_point(other_end_point)
        this_half_index = int(this_index_nearest_other_end_point/2)
        this_quarter_index = int(this_index_nearest_other_end_point/4)
        this_third_this_quarter_index = int(this_index_nearest_other_end_point/4*3)
        if this_index_nearest_other_end_point < 4:
            return False
        #end
        this_points = []
        for i in [0, this_quarter_index, this_half_index, this_third_this_quarter_index, this_index_nearest_other_end_point]:
            this_points.append(self.sequential_points[i])
            #print(self.sequential_points[i])
        #end
        
        #print( [0, this_quarter_index, this_half_index, this_third_this_quarter_index, this_index_nearest_other_end_point])

        other_index_nearest_this_start_point = other_curve.get_ctrl_p_index_at_min_distance_to_point(self.sequential_points[0])
        delta_index = len(other_curve.sequential_points) - other_index_nearest_this_start_point - 1
        if delta_index < 4:
            return False
        #end
        other_quarter_index = int(other_index_nearest_this_start_point + delta_index/4)
        other_half_index = int(other_index_nearest_this_start_point + delta_index/2)
        other_third_other_quarter_index = int(other_index_nearest_this_start_point + delta_index/4*3)
        #print([other_index_nearest_this_start_point, other_quarter_index, other_half_index, other_third_other_quarter_index, len(other_curve.sequential_points)])

        other_points = []
        for i in [other_index_nearest_this_start_point, other_quarter_index, other_half_index, other_third_other_quarter_index, -1]:
            other_points.append(other_curve.sequential_points[i])
            #print(other_curve.sequential_points[i])
        #end
        #other_points.append(other_curve.sequential_points[-1])

        angle = self.calculate_angle_between_approximate_lines_through_points(this_points, other_points)
        #print(angle*180/math.pi)

        if angle*180/math.pi > 30.0 or angle*180/math.pi < -30.0:
            return False
        #end


        average_distance = 0.0
        for i in [0, this_quarter_index, this_half_index, this_third_this_quarter_index, this_index_nearest_other_end_point]:
            point = self.sequential_points[i]
            average_distance += other_curve.get_min_distance_to_point(point)
        #end

        average_distance /= 5.0
        #print("start", average_distance)
        return average_distance < distance_threshold
    #end

    def is_continuaous_at_end_side(self, other_curve, distance_threshold):
        other_start_point = other_curve.sequential_points[0]

        this_index_nearest_other_start_point = self.get_ctrl_p_index_at_min_distance_to_point(other_start_point)

        delta_index = len(self.sequential_points) - this_index_nearest_other_start_point - 1
        if delta_index < 4:
            return False
        #end
        #print(this_index_nearest_other_start_point, delta_index)

        this_half_index = int(this_index_nearest_other_start_point + delta_index/2)
        this_quarter_index = int(this_index_nearest_other_start_point + delta_index/4)
        this_third_this_quarter_index = int(this_index_nearest_other_start_point + delta_index/4*3)
        this_points = []
        for i in [this_index_nearest_other_start_point, this_quarter_index, this_half_index, this_third_this_quarter_index, len(self.sequential_points)-1]:
            this_points.append(self.sequential_points[i])
            #print(self.sequential_points[i])
        #end

        #print([this_index_nearest_other_start_point, this_quarter_index, this_half_index, this_third_this_quarter_index, len(self.sequential_points)-1])

        other_index_nearest_this_end_point = other_curve.get_ctrl_p_index_at_min_distance_to_point(self.sequential_points[-1])
        if other_index_nearest_this_end_point < 4:
            return False
        #end
        other_quarter_index = int(other_index_nearest_this_end_point/4)
        other_half_index = int(other_index_nearest_this_end_point/2)
        other_third_other_quarter_index = int(other_index_nearest_this_end_point/4*3)
        #print([other_index_nearest_this_start_point, other_quarter_index, other_half_index, other_third_other_quarter_index, len(other_curve.sequential_points)])

        other_points = []
        for i in [0, other_quarter_index, other_half_index, other_third_other_quarter_index, other_index_nearest_this_end_point]:
            other_points.append(other_curve.sequential_points[i])
            #print(other_curve.sequential_points[i])
        #end

        angle = self.calculate_angle_between_approximate_lines_through_points(this_points, other_points)
        #print(angle*180/math.pi)

        if angle*180/math.pi > 30.0 or angle*180/math.pi < -30.0:
            return False
        #end

        average_distance = 0.0
        for i in [this_index_nearest_other_start_point, this_quarter_index, this_half_index, this_third_this_quarter_index, len(self.sequential_points)-1]:
            point = self.sequential_points[i]
            average_distance += other_curve.get_min_distance_to_point(point)
        #end

        average_distance /= 5.0
        #print("end", average_distance)
        return average_distance < distance_threshold
    #end

    def get_perpendicular_intersection_point_from_point(self, point):
        the_index = self.get_ctrl_p_index_at_min_distance_to_point(point)
        return self._ctrl_p_set[the_index].get_perpendicular_intersection_point_from_point(point)
    #end

    def create_connection_point_at_start_point(self, other_curve):
        start_point = self.sequential_points[0]
        self.start_connection_point = other_curve.get_perpendicular_intersection_point_from_point(start_point)
        #print(self.start_connection_point)
    #end

    def create_connection_point_at_end_point(self, other_curve):
        end_point = self.sequential_points[-1]
        self.end_connection_point = other_curve.get_perpendicular_intersection_point_from_point(end_point)
        #print(self.end_connection_point)
    #end
    """

    @property
    def start_index(self):
        return self._start_index
    #end
    @property
    def end_index(self):
        return self._end_index
    #end


    def __get_intersect_segment_set(self, target_rect_tuple):
        return self.qtree_ctrl_p_set.intersect(target_rect_tuple)
    #end

    def update_start_end_index_with_intersection(self, other_curve, ratio):
        the_end_of_start_side_index = int( len(self._ctrl_p_set)*ratio )
        for i in range( self._start_index, the_end_of_start_side_index ):
            the_segment = self._ctrl_p_set[i]
            the_rect_tuple = the_segment.get_rect_tuple()
            for other_segment in other_curve.__get_intersect_segment_set(the_rect_tuple):
                if the_segment.is_intersection(other_segment):
                    self._start_index = i
                #end
            #end
        #end

        the_start_of_end_side_index = int( len(self._ctrl_p_set)*(1.0-ratio) )
        the_end = self._get_the_end()
        for i in range( the_start_of_end_side_index, the_end ):
            the_segment = self._ctrl_p_set[i]
            the_rect_tuple = the_segment.get_rect_tuple()
            for other_segment in other_curve.__get_intersect_segment_set(the_rect_tuple):
                if the_segment.is_intersection(other_segment):
                    self._end_index = i
                #end
            #end
        #end
    #end 

    def __get_nearest_ctrl_p_index_to_point(self, point):
        min_distance = 999999
        the_index = None
        for i, ctrl_p in enumerate(self._ctrl_p_set):
            if ctrl_p.get_distance_to_point(point) < min_distance:
                the_index = i
                min_distance = ctrl_p.get_distance_to_point(point)
            #end
        #end
        return the_index
    #end

    def overwrite_start_end_index_finding_nearest(self, midpoint_start, midpoint_end):
        if midpoint_start is not None:
            self._start_index = self.__get_nearest_ctrl_p_index_to_point(midpoint_start)
        #end
        if midpoint_end is not None:
            self._end_index = self.__get_nearest_ctrl_p_index_to_point(midpoint_end)
        #end

        #print(self._start_index, self._end_index, len(self._ctrl_p_set))
    #end 

    # 
    # The broaden algorithm
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

    #
    # In continuaous curve, the method broaden line as below
    #
    #
    #  A ******************************************* B ****************** C
    #
    #                     |
    #                     V
    #
    #                    ************************************       
    #            ************************************************
    #       *********************************************************
    #  A ******************************************* B ****************** C
    #       *********************************************************
    #            ************************************************
    #                    ************************************
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

    def __get_slightly_away_control_point_set(self, ctrl_p_set, broaden_width, is_going, position):
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
            delta = 0
            if position == "first":
                if is_going:
                    if i < half_length:
                        delta = broaden_width * ( half_length - abs(half_length - i - 1) ) / half_length
                    else:
                        delta = broaden_width
                    #end
                else:
                    if i < half_length:
                        delta = broaden_width
                    else:
                        delta = broaden_width * ( half_length - abs(half_length - i - 1) ) / half_length
                    #end
                #end
            elif position == "last":
                if is_going:
                    if i < half_length:
                        delta = broaden_width
                    else:
                        delta = broaden_width * ( half_length - abs(half_length - i - 1) ) / half_length
                    #end
                else:
                    if i < half_length:
                        delta = broaden_width * ( half_length - abs(half_length - i - 1) ) / half_length
                    else:
                        delta = broaden_width
                    #end
                #end
            elif position == "middle":
                delta = broaden_width
            elif position == "first_last":
                delta = broaden_width * ( half_length - abs(half_length - i - 1) ) / half_length
            #end
            #delta += 0.5
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

    def broaden(self, broaden_width, position):
        from broad_linear_approximate_curve import BroadLinearApproximateCurve
        broad_curve = BroadLinearApproximateCurve()

        tmp_ctrl_p_set = self.__get_slightly_away_control_point_set(self._ctrl_p_set, broaden_width, True, position)
        tmp_returning_ctrl_p_set = self.__get_slightly_away_control_point_set(self._ctrl_p_set, broaden_width, False, position)

        broad_curve.set_ctrl_p_set(tmp_ctrl_p_set, tmp_returning_ctrl_p_set, self._start_index, self._end_index)

        return broad_curve
    #end

#end