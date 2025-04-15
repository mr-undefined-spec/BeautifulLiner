import math
import numpy as np

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/primitive'))
from point import Point
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/curve'))
from linear_approximate_curve import LinearApproximateCurve

from basic_handler import BasicHandler


class CurveOrientationHandler(BasicHandler):
    @staticmethod
    def get_the_distance_of_perpendicular_intersection_point_from_point(start, point, end):
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
            dist = CurveOrientationHandler.get_the_distance_of_perpendicular_intersection_point_from_point(points[0], points[i], points[-1])
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
    def process(curve):
        points = curve.get_points()
        #print(points)

        skip_ratio = 0.1
        skip_size = int( len(points)*skip_ratio ) 

        if CurveOrientationHandler.__are_all_points_close_to_line(points, skip_size, 1.0):
            return np.ones(size)
        #end

        curve_orientations = CurveOrientationHandler.__create_curve_orientations_with_3points_relative_position(points, skip_size)


        return curve_orientations

    #end
#end
