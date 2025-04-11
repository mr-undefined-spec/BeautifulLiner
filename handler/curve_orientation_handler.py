import os
import sys

import math

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
    def get_perpendicular_intersection_point_from_point(self, start, end, point):
        # Calculate the differences
        dx = end.x - start.x
        dy = end.y - start.y
        
        # If the segment is a point, return the point itself
        if dx == 0 and dy == 0:
            return Point(start.x, start.y)
        
        # Calculate the parameter t for the projection
        t = ((point.x - start.x) * dx + (point.y - start.y) * dy) / (dx * dx + dy * dy)
        
        # Compute the intersection point
        intersection_x = start.x + t * dx
        intersection_y = start.y + t * dy
        
        return Point(intersection_x, intersection_y)
    #end

    @staticmethod
    def get_the_distance_of_perpendicular_intersection_point_from_point(start, point, end):
        # Calculate the differences
        dx = end.x - start.x
        dy = end.y - start.y
        
        # If the segment is a point, return the point itself
        if dx == 0 and dy == 0:
            return Point(start.x, start.y)
        
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
    def process(curve):
        """
        Curveの離散的な点列に基づいて相対的な回転関係（時計回りか反時計回りか）を計算する
        """
        points = curve.get_points()
        #print(points)

        curve_orientations = []

        skip_ratio = 0.1
        skip_size = int( len(points)*skip_ratio ) 

        are_all_cross_products_less_than = True

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


            dist = CurveOrientationHandler.get_the_distance_of_perpendicular_intersection_point_from_point(points[0], points[i], points[-1])
            if dist < 1.0:
                curve_orientations.append(1.0)
            else:
                if cross_product > 0:
                    curve_orientations.append(1.0)
                else:
                    curve_orientations.append(-1.0)
                #end
            #end

            #curve_orientations.append(curvature)
        #end

        first_element = curve_orientations[0]
        last_element = curve_orientations[-1]
        for i in range(skip_size):
            curve_orientations.insert(0, first_element)
            curve_orientations.append(last_element)
        #end

        if are_all_cross_products_less_than:
            size = len(curve_orientations)
            return np.ones(size)
        else:
            return np.array(curve_orientations)
        #end

    #end
#end
