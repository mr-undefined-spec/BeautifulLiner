import math
import numpy as np

#import os
#import sys
#sys.path.append(os.path.join(os.path.dirname(__file__), '../model/primitive'))

from basic_handler import BasicHandler

class SplitHandler(BasicHandler):

    @staticmethod
    def __get_the_distance_of_perpendicular_intersection_point_from_point(start, point, end):
        # Calculate the differences
        dx = end.x - start.x
        dy = end.y - start.y
        
        # If the segment is a point, return the point itself
        if dx == 0 and dy == 0:
            return Point(start.x, start.y)
        #end
        
        # Calculate the parameter t for the projection
        t = ((point.x - start.x) * dx + (point.y - start.y) * dy) / (dx * dx + dy * dy)
        
        # Compute the intersection point
        intersection_x = start.x + t * dx
        intersection_y = start.y + t * dy

        dist = ( point.x - intersection_x )*( point.x - intersection_x ) + ( point.y - intersection_y )*( point.y - intersection_y )
        dist = math.sqrt(dist)
        
        return dist
    #end

    @staticmethod
    def __are_all_points_close_to_line(points, skip_size, eps_dist):
        are_all_points_close_to_line = True

        for i in range(skip_size, len(points)-skip_size):
            dist = SplitHandler.__get_the_distance_of_perpendicular_intersection_point_from_point(points[0], points[i], points[-1])
            if dist > eps_dist:
                are_all_points_close_to_line = False
            #end
        #end

        return are_all_points_close_to_line
    #end

    @staticmethod
    def __create_curve_orientations_with_3points_relative_position(points, skip_size):
        curve_orientations = []

        # 点列を3点ずつ取り出す
        for i in range(skip_size, len(points)-skip_size):
            p1, p2, p3 = points[0], points[i], points[-1]
            
            # ベクトルを計算
            v1 = [p2.x - p1.x, p2.y - p1.y]
            #v1 = [p1.x - p2.x, p1.y - p2.y]
            v2 = [p3.x - p2.x, p3.y - p2.y]
            length_v1 = np.linalg.norm(v1)
            length_v2 = np.linalg.norm(v2)
            
            # 外積の大きさ（曲率の分子）を計算
            cross_product = np.cross(v1, v2) / length_v1 / length_v2
            #cross_product = (v1[0]*v2[1] - v1[1]*v2[0]) / length_v1 / length_v2

            theta = np.arcsin(cross_product)
            theta_degree = np.degrees(theta)


            """
            if theta_degree > 15:
                print(dist)
                print(theta_degree)
                print(p1)
                print(p2)
                print(p3)
                print(v1)
                print(v2)
                print(length_v1)
                print(length_v2)
                print(cross_product)
                print("")
            """
            if( cross_product > 0.1 ):
                are_all_cross_products_less_than = False
            #end


            if cross_product > 0:
                curve_orientations.append(1.0)
            else:
                curve_orientations.append(-1.0)
            #end

            #curve_orientations.append(curvature)
        #end

        first_element = curve_orientations[0]
        last_element = curve_orientations[-1]
        for i in range(skip_size):
            curve_orientations.insert(0, first_element)
            curve_orientations.append(last_element)
        #end
        return np.array(curve_orientations)

        # old functions not used now
        """
        are_all_cross_products_less_than = True
        if are_all_cross_products_less_than:
            size = len(curve_orientations)
            return np.ones(size)
        else:
        """

    #end

    @staticmethod
    def __create_split_curve_ranges(curve_orientations, index_offset):
        split_curve_ranges = []
        current_value = curve_orientations[0]

        pre_index= 0

        for i, value in enumerate(curve_orientations):
            if value != current_value:
                split_curve_ranges.append((pre_index + index_offset, i + index_offset))
                pre_index = i
                current_value = value
            #end
        #end

        split_curve_ranges.append((pre_index + index_offset, len(curve_orientations) + index_offset))  # 最後の区間を追加
        return split_curve_ranges
    #end

    @staticmethod
    def __calculate_angle_between_vectors(v1, v2):
        """2つのベクトル間の角度をラジアンで計算"""
        dot_product = v1[0]*v2[0] + v1[1]*v2[1]
        mag_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
        mag_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
        cos_theta = dot_product / (mag_v1 * mag_v2)
        # 安全のために値を[-1, 1]にクリップ
        cos_theta = max(-1, min(1, cos_theta))
        return math.acos(cos_theta)  # ラジアンで返す
    #end

    @staticmethod
    def __get_index_of_max_dist_less_than_angle_threshold(points, start_index, end_index, angle_threshold_deg):
        """
        点列から曲線の特徴点を分析し、最大角度が閾値を超えるか判定
        points: [(x1, y1), (x2, y2), ..., (xn, yn)]
        angle_threshold_deg: 判定に使う角度の閾値（度数法）
        """
        if len(points) < 3:
            raise ValueError("点列は最低3点必要です")
        #end

        start = points[start_index]
        end = points[end_index-1]

        # 最も離れている点を見つける
        max_dist = -1
        max_point = None
        max_index = -1

        for i in range(start_index + 1, end_index - 2):  # 最初と最後の点は除く
            p = points[i]
            dist = SplitHandler.__get_the_distance_of_perpendicular_intersection_point_from_point(start, p, end)
            if dist > max_dist:
                max_dist = dist
                max_point = p
                max_index = i
            #end
        #end

        if max_point is None:
            return -1
        #end

        # 三角形の3点: start, max_point, end から角度を求める
        vec1 = (start.x - max_point.x, start.y - max_point.y)
        vec2 = (end.x - max_point.x, end.y - max_point.y)

        angle_rad = SplitHandler.__calculate_angle_between_vectors(vec1, vec2)
        angle_deg = math.degrees(angle_rad)

        if angle_deg < angle_threshold_deg:
            return max_index
        else:
            return -1
        #end
    #end

    @staticmethod
    def __create_curve_orientations(curve):
        points = curve.get_points()
        #print(points)
        #print( len(points) )
        #print( len(curve) )

        skip_ratio = 0.1
        skip_size = int( len(points)*skip_ratio ) 
        if skip_size == 0:
            skip_size = 1 
        #end

        if SplitHandler.__are_all_points_close_to_line(points, skip_size, 1.0):
            return np.ones( len(points) )
        #end

        curve_orientations = SplitHandler.__create_curve_orientations_with_3points_relative_position(points, skip_size)



        return curve_orientations
    #end

    @staticmethod
    def process(curve, index_offset):
        curve_orientations = SplitHandler.__create_curve_orientations(curve)

        once_split_curve_ranges = SplitHandler.__create_split_curve_ranges(curve_orientations, 0)

        split_curve_ranges = []
        for ranges in once_split_curve_ranges:
            the_index = SplitHandler.__get_index_of_max_dist_less_than_angle_threshold(curve.get_points(), 
            ranges[0], ranges[1], 90.0)
            if the_index != -1:
                split_curve_ranges.append((ranges[0] + index_offset, the_index + index_offset))
                split_curve_ranges.append((the_index + 1 + index_offset, ranges[1] + index_offset))
            else:
                split_curve_ranges.append((ranges[0] + index_offset, ranges[1] + index_offset))
            #end
        #end
        
        #SplitHandler.__create_split_curve_ranges(curve_orientations, index_offset)

        return split_curve_ranges
    #end


#end
