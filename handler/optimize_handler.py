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
from scipy.optimize import minimize

class OptimizeHandler(BasicHandler):

    @staticmethod
    def compute_segment_error(data, start, end):
        """ 区間 [start, end] を +1 または -1 で近似した場合の誤差を計算 """
        segment = data[start:end+1]
        
        # +1 に近似した場合の誤差
        error_plus = np.sum((segment - 1) ** 2)
        
        # -1 に近似した場合の誤差
        error_minus = np.sum((segment + 1) ** 2)
        
        # より誤差が小さい方を採用
        return min(error_plus, error_minus)
    #end

    @staticmethod
    def optimize(curve_orientations, optimize_order):
        """ セグメント平均法を用いた最適な符号反転点の探索 """

        if optimize_order < 2:
            raise ValueError('optimize_order must be greater than or equal to 2.')
        #end

        size = len(curve_orientations)
        
        # コストテーブル（累積誤差）
        cost = np.full((size, size), np.inf)
        
        # 各区間 [i, j] の誤差を事前計算
        for i in range(size):
            for j in range(i, size):
                cost[i][j] = OptimizeHandler.compute_segment_error(curve_orientations, i, j)
        
        # 動的計画法の DP テーブル
        dp = np.full((size+1, optimize_order+1), np.inf)
        dp[0][0] = 0  # 初期状態（データなし）

        # 最適な分割点を保持するテーブル
        prev = np.zeros((size+1, optimize_order+1), dtype=int)

        # DP で最適な誤差を計算
        for m in range(1, optimize_order+1):  # m 回までの符号反転を許容
            for j in range(1, size+1):
                for i in range(j):  # 直前の分割位置
                    new_cost = dp[i][m-1] + cost[i][j-1]
                    if new_cost < dp[j][m]:
                        dp[j][m] = new_cost
                        prev[j][m] = i  # どこで分割したかを記録

        # 最小誤差を持つ最適な分割点を復元
        best_m = np.argmin(dp[size, :])
        best_error = dp[size, best_m]
        
        # 最適な分割点の復元
        optimized_invert_index = []
        idx = size
        for m in range(best_m, 0, -1):
            idx = prev[idx][m]
            optimized_invert_index.append(idx)
        
        optimized_invert_index.reverse()
        
        return optimized_invert_index

        
    #end



#end
