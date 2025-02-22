
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../handler'))
from optimize_handler import OptimizeHandler

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/curve'))
from linear_approximate_curve import LinearApproximateCurve

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model/primitive'))
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

sys.path.append(os.path.join(os.path.dirname(__file__), '../helper'))
import handler_mocks
import model_mocks

import unittest

import numpy as np
import math

class TestOptimizeHandler(unittest.TestCase):
    def setUp(self):
        self.layer_set = handler_mocks.create_mock_layer_set_of_cubic_bezier_curve_arc()

    #end

    def generate_data_including_noise(self, size, invert_index, noise_ratio=0.0, seed=None):
        """
        ノイズを含むデータを生成する
        size: 配列の長さ
        invert_index: 符号が変わるポイントのリスト
        noise_ratio: ノイズの割合
        seed: 乱数シード
        """
        if seed is not None:
            np.random.seed(seed)
        
        base_sign = 1 if np.random.rand() < 0.5 else -1  # 符号のランダム選択
        data = np.full(size, base_sign)
        
        for i, cp in enumerate(invert_index):
            data[cp:] *= -1
        
        # ノイズを追加
        num_noisy = int(size * noise_ratio)
        noisy_indices = np.random.choice(size, num_noisy, replace=False)
        data[noisy_indices] *= -1
        
        return data
    #end

    def test_optimize_without_noise(self):
        size = 100
        noise_ratio = 0.0
        seed = 42

        original_invert_index_2 = [20]
        test_curve_orientations_2 = self.generate_data_including_noise(size, original_invert_index_2, noise_ratio, seed)
        optimize_handler = OptimizeHandler()
        optimized_invert_index_2 = optimize_handler.optimize(test_curve_orientations_2, 2)
        #print(test_curve_orientations_2)
        #print(original_invert_index_2)
        #print(optimized_invert_index_2)
        self.assertEqual(optimized_invert_index_2, [0, 20, 99])

        original_invert_index_3 = [30, 45]
        test_curve_orientations_3 = self.generate_data_including_noise(size, original_invert_index_3, noise_ratio, seed)
        optimize_handler = OptimizeHandler()
        optimized_invert_index_3 = optimize_handler.optimize(test_curve_orientations_3, 3)
        #print(original_invert_index_3)
        #print(optimized_invert_index_3)
        self.assertEqual(optimized_invert_index_3, [0, 30, 45, 99])

        original_invert_index_4 = [10, 20, 75]
        test_curve_orientations_4 = self.generate_data_including_noise(size,original_invert_index_4, noise_ratio, seed)
        optimize_handler = OptimizeHandler()
        optimized_invert_index_4 = optimize_handler.optimize(test_curve_orientations_4, 4)
        #print(original_invert_index_4)
        #print(optimized_invert_index_4)
        self.assertEqual(optimized_invert_index_4, [0, 10, 20, 75, 99])

    #end

    def test_optimize_with_noise(self):
        size = 100
        noise_ratio = 0.1
        seed = 42

        original_invert_index_2 = [20]
        test_curve_orientations_2 = self.generate_data_including_noise(size, original_invert_index_2, noise_ratio, seed)
        optimize_handler = OptimizeHandler()
        optimized_invert_index_2 = optimize_handler.optimize(test_curve_orientations_2, 2)
        #print(test_curve_orientations_2)
        #print(original_invert_index_2)
        #print(optimized_invert_index_2)
        self.assertEqual(optimized_invert_index_2, [0, 20, 99])

        original_invert_index_3 = [30, 45]
        test_curve_orientations_3 = self.generate_data_including_noise(size, original_invert_index_3, noise_ratio, seed)
        optimize_handler = OptimizeHandler()
        optimized_invert_index_3 = optimize_handler.optimize(test_curve_orientations_3, 3)
        #print(original_invert_index_3)
        #print(optimized_invert_index_3)
        self.assertEqual(optimized_invert_index_3, [0, 30, 44, 99]) # <- not 45 because of noise

        original_invert_index_4 = [10, 20, 75]
        test_curve_orientations_4 = self.generate_data_including_noise(size,original_invert_index_4, noise_ratio, seed)
        optimize_handler = OptimizeHandler()
        optimized_invert_index_4 = optimize_handler.optimize(test_curve_orientations_4, 4)
        #print(original_invert_index_4)
        #print(optimized_invert_index_4)
        self.assertEqual(optimized_invert_index_4, [0, 11, 20, 75, 99]) # <- not 10 because of noise

    #end

#end

if __name__ == '__main__':
    unittest.main()
#end

