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

class SplitHandler(BasicHandler):

    @classmethod
    def create_positive_start_signed_array(cls, size, invert_index):
        """
        +1 から始めて反転インデックスに従いデータを反転
        """
        return_array = np.ones(size, dtype=int)
        sign = 1  # 初期符号

        for i in range(len(invert_index)):
            return_array[invert_index[i]:] *= -1  # 反転処理
        #end
        return return_array
    #end

    @classmethod
    def create_negative_start_signed_array(cls, size, invert_index):
        """
        -1 から始めて反転インデックスに従いデータを反転
        """
        return_array = np.ones(size, dtype=int)
        sign = -1  # 初期符号

        for i in range(len(invert_index)):
            return_array[invert_index[i]:] *= -1  # 反転処理
        #end
        return return_array
    #end

    @classmethod
    def objective_function(cls, opt_idx, size, original_array):
        """
        目的関数: optimized_array (正負どちらの始まりも考慮) が original_array に近づくように最適化
        """
        opt_idx = np.round(opt_idx).astype(int)  # 整数化
        opt_idx = np.clip(opt_idx, 1, size - 1)  # 範囲制限

        # +1 から始まるパターン
        optimized_array_positive = cls.create_positive_start_signed_array(size, opt_idx)
        loss_positive = np.sum((optimized_array_positive - original_array) ** 2)

        # -1 から始まるパターン
        optimized_array_negative = cls.create_negative_start_signed_array(size, opt_idx)
        loss_negative = np.sum((optimized_array_negative - original_array) ** 2)

        # 最小誤差を採用
        return min(loss_positive, loss_negative)
    #end

    @classmethod
    def optimize_invert_index(cls, original_array, initial_guess_index):
        """
        最適なデータ反転インデックスを求める。
        """
        size = len(original_array)
        initial_guess = np.array(initial_guess_index, dtype=float)

        result = minimize(cls.objective_function, initial_guess, args=(size, original_array),
                        method='Nelder-Mead', tol=1.0e-10, options={'maxiter': 10000, 'disp': False})

        optimized_index = np.round(result.x).astype(int)  # 整数化
        optimized_index = np.clip(optimized_index, 1, size - 1)  # 範囲制限
        return sorted(optimized_index.tolist())
    #end


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
            #end

            if curvature > 0:
                curvatures.append(1.0)
            else:
                curvatures.append(-1.0)
            #end
            #curvatures.append(curvature)
        #end
        
        return np.array(curvatures)
    #end

    @classmethod
    def denoise_sign_transitions(cls, curvatures):
        n = len(curvatures)
        threshold = int(n * 0.1)  # 10% の閾値

        # 符号が変わるインデックスを取得
        sign_changes = np.where(np.diff(np.sign(curvatures)) != 0)[0] + 1

        # 連続する符号の範囲を取得
        segments = []
        start = 0
        for idx in sign_changes:
            segments.append((start, idx))
            start = idx
        segments.append((start, n))  # 最後のセグメントを追加
        print(segments)

        # 短すぎるセグメントを修正
        new_arr = curvatures.copy()
        for i, (start, end) in enumerate(segments):
            if end - start <= threshold:
                # 周囲の符号に統一
                if start == 0:
                    new_sign = np.sign(curvatures[end])
                elif end == n:
                    new_sign = np.sign(curvatures[start - 1])
                else:
                    new_sign = np.sign(curvatures[start - 1])  # 前のセグメントの符号を優先

                new_arr[start:end] = new_sign
            #end
        #end

        return new_arr
    #end

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

                    size = len(curvatures)

                    initial_guess_index = [size/3, size/2]
                    #initial_guess_index = []

                    inflection_points = cls.optimize_invert_index(curvatures, initial_guess_index)  
                    #cls.find_inflection_points(new_curvatures)
                    print(inflection_points)
                #end

                print(len(curve_set[0]))

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
