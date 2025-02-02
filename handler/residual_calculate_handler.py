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

from scipy.special import comb
from scipy.spatial import KDTree

class ResidualCalculateHandler(BasicHandler):
    @staticmethod
    def calculate_residual(linear_approximate_curve_a, linear_approximate_curve_b):
        """
        2つの線形近似曲線の点列間の残渣を計算する。
        
        各点列のすべての点について、もう一方の点列内の最も近い点との距離を求め、
        その総和を残渣とする。
        
        :param linear_approximate_curve_a: np.ndarray, shape (N, 2)
            近似曲線Aの点列（各点は[x, y]）
        :param linear_approximate_curve_b: np.ndarray, shape (M, 2)
            近似曲線Bの点列（各点は[x, y]）
        :return: float
            総残渣
        """
        tree_a = KDTree(linear_approximate_curve_a.get_start_points_as_numpy_array())
        tree_b = KDTree(linear_approximate_curve_b.get_start_points_as_numpy_array())
        
        # Aの各点に対してB内の最近点を求める
        distances_a_to_b, _ = tree_b.query(linear_approximate_curve_a.get_start_points_as_numpy_array())
        
        # Bの各点に対してA内の最近点を求める
        distances_b_to_a, _ = tree_a.query(linear_approximate_curve_b.get_start_points_as_numpy_array())
        
        return np.sum(distances_a_to_b) + np.sum(distances_b_to_a)
#end