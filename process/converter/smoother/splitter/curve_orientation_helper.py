import numpy as np
import math
from model.primitive.point import Point
from util.geometry import Geometry # 既存の共通幾何計算ユーティリティ


class CurveOrientationHelper:

    @staticmethod
    def are_points_almost_linear(points: list[Point], skip_size: int, eps_dist: float = 1.0) -> bool:
        for i in range(skip_size, len(points) - skip_size):
            dist = Geometry.get_distance_point_to_segment(points[0], points[i], points[-1])
            if dist > eps_dist:
                return False
            # end if
        return True
    # end are_points_almost_linear

    @staticmethod
    def create_curve_orientations(points: list[Point], skip_size: int) -> np.ndarray:
        orientations = []
        all_small = True
        for i in range(skip_size, len(points) - skip_size):
            p1, p2, p3 = points[0], points[i], points[-1]
            v1 = [p2.x - p1.x, p2.y - p1.y]
            v2 = [p3.x - p2.x, p3.y - p2.y]
            
            # NumPyの代わりに純粋な数学計算で2次元の外積とノルムを計算
            length_v1 = math.hypot(v1[0], v1[1])
            length_v2 = math.hypot(v2[0], v2[1])
            
            if length_v1 == 0 or length_v2 == 0:
                cross = 0.0
            else:
                # 2次元ベクトルの外積公式: x1*y2 - y1*x2
                cross = (v1[0] * v2[1] - v1[1] * v2[0]) / (length_v1 * length_v2)
            # end if
            
            # arcsinのドメインエラー防止
            theta = math.asin(max(-1.0, min(1.0, cross)))
            theta_deg = math.degrees(theta)

            if cross > 0.1:
                all_small = False
            # end if

            orientations.append(1.0 if cross > 0 else -1.0)
        # end for

        if all_small:
            return np.ones(len(points))
        # end if

        first, last = orientations[0], orientations[-1]
        for _ in range(skip_size):
            orientations.insert(0, first)
            orientations.append(last)
        # end for

        return np.array(orientations)
    # end create_curve_orientations

    @staticmethod
    def smooth_and_remove_noise(arr: np.ndarray) -> np.ndarray:
        arr = np.asarray(arr)
        kernel = np.ones(3) / 3
        smoothed = np.convolve(arr, kernel, mode='same')
        return np.where(smoothed > 0, 1, -1)
    # end smooth_and_remove_noise

# end class