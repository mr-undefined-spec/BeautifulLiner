


from xml.dom import minidom

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../model/curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../model/layer'))

from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from linear_approximate_curve import LinearApproximateCurve
from multi_curve_set import MultiCurveSet

from layer import Layer
from layer_set import LayerSet

from basic_handler import BasicHandler

import numpy as np

import re

class SplitHandler(BasicHandler):

    @classmethod
    def calculate_curvature(cls, points):
        """
        離散的な点列に基づいて局所曲率を計算する
        """
        # 点列を3点ずつ取り出す
        curvatures = []
        for i in range(1, len(points) - 1):
            p1, p2, p3 = points[i - 1], points[i], points[i + 1]
            
            # ベクトルを計算
            #v1 = p2 - p1
            #v2 = p3 - p2
            v1 = [p2.x - p1.x, p2.y - p1.y]
            v2 = [p3.x - p2.x, p3.y - p2.y]
            
            # 外積の大きさ（曲率の分子）を計算
            cross_product = np.cross(v1, v2)
            
            # 各ベクトルの長さ（曲率の分母）を計算
            norm_v1 = np.linalg.norm(v1)
            norm_v2 = np.linalg.norm(v2)
            
            # 曲率を計算
            if norm_v1 * norm_v2 != 0:  # 0割防止
                curvature = cross_product / (norm_v1 * norm_v2)
            else:
                curvature = 0
            curvatures.append(curvature)
        
        return np.array(curvatures)

    @classmethod
    def find_inflection_points(cls, curvatures):
        """
        曲率の符号反転点（変曲点）を検出する
        """
        inflection_points = []
        for i in range(1, len(curvatures)):
            if curvatures[i - 1] * curvatures[i] < 0:  # 符号反転
                inflection_points.append(i)
        return inflection_points

    @classmethod
    def process(cls, layer_set):
        return_layer_set = LayerSet()

        for layer in layer_set:
            tmp_layer = Layer(layer.name)
            for curve_set in layer:
                for curve in curve_set:
                    points = curve.get_start_points()
                    #print(points)

                    curvatures = cls.calculate_curvature(points)
                    #print(curvatures)

                    inflection_points = cls.find_inflection_points(curvatures)
                    #print(inflection_points)
                #end

                if inflection_points == []:
                    tmp_layer.append(curve_set)
                    continue
                #end

                inflection_range_set = []
                inflection_range_set.append( [0, inflection_points[0]] )
                for index_inflection_point in range(  0, ( len(inflection_points)-1 )  ):
                    inflection_range_set.append( [inflection_points[index_inflection_point], inflection_points[index_inflection_point+1]] )
                #end
                inflection_range_set.append( [inflection_points[-1], len(curve_set[0])-1 ] )

                tmp_curve_set = MultiCurveSet()
                for inflection_range in inflection_range_set:
                    tmp_curve = LinearApproximateCurve()
                    for index_curve in range(inflection_range[0], inflection_range[1]):
                        tmp_curve.append( LinearApproximateCurveControlPoint(curve_set[0][index_curve].start, curve_set[0][index_curve].end) )
                    #end
                    tmp_curve_set.append(tmp_curve)
                #end

                tmp_layer.append(tmp_curve_set)
            #end
            return_layer_set.append(tmp_layer)
        #end

        return return_layer_set
    #end



#end
