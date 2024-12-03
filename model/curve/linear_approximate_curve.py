
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
        self.qtree_ctrl_p_set = None
        self.start_side_edge_segment = None
        self.end_side_edge_segment   = None
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

    def thin_smoothen(self):
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

    def create_sequential_points(self):
        self.sequential_points = []
        
        for ctrl_p in self._going_ctrl_p_set:
            self.sequential_points.append(ctrl_p.s)
        #end
        self.sequential_points.append(self._going_ctrl_p_set[-1].e)
    #end

    def create_edge_sequential_points(self, ratio):
        self.start_side_sequential_points = []
        self.end_side_sequential_points = []

        num_of_sequential_points = len(self.sequential_points)
        num_of_edge_points = int(ratio*num_of_sequential_points)

        for i in range(num_of_edge_points):
            self.start_side_sequential_points.append(self.sequential_points[i])
            end_side_index = num_of_sequential_points - i - 1
            self.end_side_sequential_points.append(self.sequential_points[end_side_index])
        #end
    #end

    def is_continuaous_at_start_side(self, other_curve, distance_threshold):
        average_distance = 0.0
#        min_distances = []
        for point in self.start_side_sequential_points:
            min_distance = 999999
            for other_point in other_curve.sequential_points:
                min_distance = min(min_distance, other_point.distance(point))
            #end
#            min_distances.append(min_distance)
            average_distance += min_distance
        #end

        average_distance /= len(self.start_side_sequential_points)
        return average_distance < distance_threshold
    #end

    def is_continuaous_at_end_side(self, other_curve, distance_threshold):
        average_distance = 0.0
#        min_distances = []
        for point in self.end_side_sequential_points:
            min_distance = 999999
            for other_point in other_curve.sequential_points:
                min_distance = min(min_distance, other_point.distance(point))
            #end
#            min_distances.append(min_distance)
            average_distance += min_distance
        #end

        average_distance /= len(self.end_side_sequential_points)
        return average_distance < distance_threshold
    #end




    def __min_distance_segment_to_segment(self, seg1_start, seg1_end, seg2_start, seg2_end):
        distance_seg1_s = self.__distance_point_to_line(seg1_start.x, seg1_start.y, seg1_end.x, seg1_end.y, seg2_start.x, seg2_start.y)
        distance_seg1_e = self.__distance_point_to_line(seg1_start.x, seg1_start.y, seg1_end.x, seg1_end.y, seg2_end.x, seg2_end.y)
        distance_seg2_s = self.__distance_point_to_line(seg2_start.x, seg2_start.y, seg2_end.x, seg2_end.y, seg1_start.x, seg1_start.y)
        distance_seg2_e = self.__distance_point_to_line(seg2_start.x, seg2_start.y, seg2_end.x, seg2_end.y, seg1_end.x, seg1_end.y)

        return min(distance_seg1_s, distance_seg1_e, distance_seg2_s, distance_seg2_e)
    #end
    def __distance_point_to_line(self,x1, y1, x2, y2, px, py):
        """
        2点 (x1, y1), (x2, y2) を通る直線と点 (px, py) との距離を求める。

        Args:
            x1, y1: 1つ目の点の座標
            x2, y2: 2つ目の点の座標
            px, py: 線上にない点の座標

        Returns:
            距離 (float) またはエラーメッセージ (str)
        """
        # 2点が同じ場合は直線が定義できない
        if x1 == x2 and y1 == y2:
            return "2点が同じ座標です。直線が定義できません。"

        # 2点を通る直線の方程式: Ax + By + C = 0 の係数を計算
        A = y2 - y1
        B = x1 - x2
        C = x2 * y1 - x1 * y2

        denominator = math.sqrt(A**2 + B**2)

        # 点と直線の距離の公式を適用
        distance = abs(A * px + B * py + C) / denominator
        return distance



    def __calculate_distance(self, point, line_start, line_end):
        """点と直線の距離を計算する"""
        line_vec = ((line_end.x - line_start.x), (line_end.y - line_start.y))#, line_end - line_start
        point_vec = ((point.e.x - line_start.x), (point.e.y - line_start.y))
        line_length = np.linalg.norm(line_vec)
        if line_length == 0:
            return np.linalg.norm(point_vec)
        print(line_vec, point_vec, line_length)
        projection = np.dot(point_vec, line_vec) / line_length
        if projection < 0:
            return np.linalg.norm(point_vec)
        elif projection > line_length:
            return np.linalg.norm(point - line_end)
        else:
            projection_point = line_start + projection * line_vec / line_length
            return np.linalg.norm(point - projection_point)

    def __is_approximated_with_segment(self, start_index, end_index, threshold):
        """
        微小線分の集合に対し、端部から一定区間を直線で近似できる範囲を求める
        
        :param segments: 微小線分集合 [(x1, y1), (x2, y2), ...]
        :param segment_count: 端部からの区間に含める微小線分の個数
        :param threshold: 距離の平均値の閾値
        :return: 直線近似が可能な端部の範囲（始点インデックス, 終点インデックス）
        """
        segments = np.array(self._going_ctrl_p_set[start_index:end_index])
        segment_count = end_index - start_index
        n = len(segments)
        if n < segment_count:
            raise ValueError("微小線分が指定された個数より少ないです。")
        
        # 始点からの計算
        start_point = segments[0].s
        end_point = segments[segment_count - 1].e
        distances = [
#            self.__calculate_distance(segments[i], start_point, end_point)
            self.__distance_point_to_line(start_point.x, start_point.y, end_point.x, end_point.y, segments[i].s.x, segments[i].s.y)
            for i in range(segment_count)
        ]
        avg_distance = np.mean(distances)
        
        if avg_distance <= threshold:
            return True 
        else:
            return False
        #end
    #end

    def prepare_edge_segments(self):
        start_side_start_index = 0
        start_side_end_index = 1 #FIXME
        end_side_start_index = len(self._going_ctrl_p_set) - 2
        end_side_end_index = len(self._going_ctrl_p_set) - 1

        num_of_going_ctrl_p_set = len(self._going_ctrl_p_set)
        the_25_percent_index_of_this_curve = int(num_of_going_ctrl_p_set*0.25)
        the_75_percent_index_of_this_curve = int(num_of_going_ctrl_p_set*0.75)

        for i in range(1, the_25_percent_index_of_this_curve):
            if not self.__is_approximated_with_segment(start_side_start_index, i, 0.1):
                start_side_end_index = i+1
                break
            #end
        #end

        for i in reversed( range(the_75_percent_index_of_this_curve, num_of_going_ctrl_p_set-2) ):
            if not self.__is_approximated_with_segment(i, end_side_end_index, 0.1):
                end_side_start_index = i
                break
            #end
        #end
        
        self.start_side_edge_segment = LinearApproximateCurveControlPoint(self._going_ctrl_p_set[start_side_start_index].s, self._going_ctrl_p_set[start_side_end_index].e)
        self.end_side_edge_segment = LinearApproximateCurveControlPoint(self._going_ctrl_p_set[end_side_start_index].s, self._going_ctrl_p_set[end_side_end_index].e)

    #end



    def __is_continuous_with(self, target_control_point, reference_control_points, distance_threshold):
        s = ""
        target_vec = Vector(target_control_point.s, target_control_point.e)

        for ref_cp in reference_control_points:
            distance_s_s = target_control_point.s.distance(ref_cp.s)
            distance_e_e = target_control_point.e.distance(ref_cp.e)
            distance_s_e = target_control_point.s.distance(ref_cp.e)
            distance_e_s = target_control_point.e.distance(ref_cp.s)

            distance_check = False
            if distance_s_s < distance_threshold and distance_e_e < distance_threshold:
                distance_check = True
            elif distance_s_e < distance_threshold and distance_e_s < distance_threshold:
                distance_check = True
            #end




            s = ""
            s += "target_control_point: {}, {}\n".format(str(target_control_point.s), str(target_control_point.e))
            s += "target_vec: ({}, {})\n".format(target_vec.x, target_vec.y)
            s += "ref_cp: {}, {}\n".format(str(ref_cp.s), str(ref_cp.e))
            ref_vec = Vector(ref_cp.s, ref_cp.e)
            s += "ref_vec: ({}, {})\n".format(ref_vec.x, ref_vec.y)

            angle_check = False
            angle = target_vec.calc_angle(ref_vec)
            if angle < 10.0*math.pi/180.0:
                angle_check = True
            elif angle > 170.0*math.pi/180.0:
                angle_check = True
            #end

            s += "angle: {}\n".format(angle*180.0/math.pi)

            print(s)


            print(angle*180.0/math.pi, angle_check)

            if distance_check and angle_check:
                return True
            #end
        #end
        print(s)
        return False
    #end

    def is_continuaous_with(self, other_curve, distance_threshold):
        this_start_side_edge_segment = self.start_side_edge_segment
        this_end_side_edge_segment = self.end_side_edge_segment
        other_start_side_edge_segment = other_curve.start_side_edge_segment
        other_end_side_edge_segment = other_curve.end_side_edge_segment

        target_edge_segment_of_this = None
        target_edge_segment_of_other = None

        start_point_of_this = this_start_side_edge_segment.s
        end_point_of_this = this_end_side_edge_segment.e
        start_point_of_other = other_start_side_edge_segment.s
        end_point_of_other = other_end_side_edge_segment.e

        distance_s_s = start_point_of_this.distance(start_point_of_other)
        distance_e_e = end_point_of_this.distance(end_point_of_other)
        distance_s_e = start_point_of_this.distance(end_point_of_other)
        distance_e_s = end_point_of_this.distance(start_point_of_other)
        min_distance_of_four = min(distance_s_s, distance_e_e, distance_s_e, distance_e_s)

        if min_distance_of_four == distance_s_s:
            target_edge_segment_of_this = this_start_side_edge_segment
            target_edge_segment_of_other = other_start_side_edge_segment
        elif min_distance_of_four == distance_e_e:
            target_edge_segment_of_this = this_end_side_edge_segment
            target_edge_segment_of_other = other_end_side_edge_segment
        elif min_distance_of_four == distance_s_e:
            target_edge_segment_of_this = this_start_side_edge_segment
            target_edge_segment_of_other = other_end_side_edge_segment
        else:
            target_edge_segment_of_this = this_end_side_edge_segment
            target_edge_segment_of_other = other_start_side_edge_segment
        #end

        min_distance = self.__min_distance_segment_to_segment(target_edge_segment_of_this.s, target_edge_segment_of_this.e, target_edge_segment_of_other.s, target_edge_segment_of_other.e)
        #print(this_start_side_edge_segment.to_svg(True), this_end_side_edge_segment.to_svg(True))
        #print(other_start_side_edge_segment.to_svg(True), other_end_side_edge_segment.to_svg(True))
        #print(target_edge_segment_of_this.to_svg(True), target_edge_segment_of_other.to_svg(True))
        #print(min_distance)

        distance_check = min_distance < distance_threshold

        vec_this = Vector(target_edge_segment_of_this.s, target_edge_segment_of_this.e)
        vec_other = Vector(target_edge_segment_of_other.s, target_edge_segment_of_other.e)

        angle = vec_this.calc_angle(vec_other)
        angle_check = angle < 30.0*math.pi/180.0 or angle > 150.0*math.pi/180.0
        
        #print(angle*180.0/math.pi, angle_check)

        return distance_check and angle_check

    #end


    def tottoku(self, other_curve, distance_threshold):
        num_of_going_ctrl_p_set = len(self._going_ctrl_p_set)
        num_of_other_going_ctrl_p_set = len(other_curve._going_ctrl_p_set)

        the_10_percent_index_of_this_curve = int(num_of_going_ctrl_p_set*0.1)
        the_90_percent_index_of_this_curve = int(num_of_going_ctrl_p_set*0.9)
        the_10_percent_index_of_other_curve = int(num_of_other_going_ctrl_p_set*0.1)
        the_90_percent_index_of_other_curve = int(num_of_other_going_ctrl_p_set*0.9)

        """
        the_first_point_of_this_curve = self._going_ctrl_p_set[0].s
        the_point_at_10_percent_of_this_curve = self._going_ctrl_p_set[the_10_percent_index].e
        the_point_at_90_percent_of_this_curve = self._going_ctrl_p_set[the_90_percent_index].s
        the_last_point_of_this_curve = self._going_ctrl_p_set[-1].e
        vec_first_to_10_percent_of_this_curve = Vector(the_first_point_of_this_curve, the_point_at_10_percent_of_this_curve)
        vec_90_percent_to_last_of_this_curve = Vector(the_point_at_90_percent_of_this_curve, the_last_point_of_this_curve)

        the_first_point_of_other_curve = other_curve._going_ctrl_p_set[0].s
        the_point_at_10_percent_of_other_curve = other_curve._going_ctrl_p_set[the_10_percent_index].e
        the_point_at_90_percent_of_other_curve = other_curve._going_ctrl_p_set[the_90_percent_index].s
        the_last_point_of_other_curve = other_curve._going_ctrl_p_set[-1].e
        vec_first_to_10_percent_of_other_curve = Vector(the_first_point_of_other_curve, the_point_at_10_percent_of_other_curve)
        vec_90_percent_to_last_of_other_curve = Vector(the_point_at_90_percent_of_other_curve, the_last_point_of_other_curve)

        the_first_control_point_of_this_curve = self._going_ctrl_p_set[the_10_percent_index_of_this_curve]
        the_last_control_point_of_this_curve = self._going_ctrl_p_set[the_90_percent_index_of_this_curve]

        the_first_control_point_of_other_curve = other_curve._going_ctrl_p_set[the_10_percent_index_of_other_curve]
        the_last_control_point_of_other_curve = other_curve._going_ctrl_p_set[the_90_percent_index_of_other_curve]
        """

        the_first_control_point_of_this_curve = self._going_ctrl_p_set[10]
        the_last_control_point_of_this_curve = self._going_ctrl_p_set[-10]

        the_first_control_point_of_other_curve = other_curve._going_ctrl_p_set[10]
        the_last_control_point_of_other_curve = other_curve._going_ctrl_p_set[-10]


        if self.__is_continuous_with(the_first_control_point_of_this_curve, other_curve._going_ctrl_p_set, distance_threshold):
            print("the_first_control_point_of_this_curve")
            if self.__is_continuous_with(the_first_control_point_of_other_curve, self._going_ctrl_p_set, distance_threshold):
                print("the_first_control_point_of_other_curve")
                return True
            elif self.__is_continuous_with(the_last_control_point_of_other_curve, self._going_ctrl_p_set, distance_threshold):
                print("the_last_control_point_of_other_curve")
                return True
            #end
        elif self.__is_continuous_with(the_last_control_point_of_this_curve, other_curve._going_ctrl_p_set, distance_threshold):
            print("the_last_control_point_of_this_curve")
            if self.__is_continuous_with(the_first_control_point_of_other_curve, self._going_ctrl_p_set, distance_threshold):
                print("the_first_control_point_of_other_curve")
                return True
            elif self.__is_continuous_with(the_last_control_point_of_other_curve, self._going_ctrl_p_set, distance_threshold):
                print("the_last_control_point_of_other_curve")
                return True
            #end
        #end

        return False
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