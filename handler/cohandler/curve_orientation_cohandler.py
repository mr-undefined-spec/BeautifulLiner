import numpy as np

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../cohandler'))

from geometry_cohandler import GeometryCohandler

class CurveOrientationCohandler:

    @staticmethod
    def are_points_almost_linear(points, skip_size, eps_dist=1.0):
        for i in range(skip_size, len(points) - skip_size):
            dist = GeometryCohandler.get_distance_point_to_segment(points[0], points[i], points[-1])
            if dist > eps_dist:
                return False
            # end if
        return True
    # end are_points_almost_linear

    @staticmethod
    def create_curve_orientations(points, skip_size):
        orientations = []
        all_small = True
        for i in range(skip_size, len(points) - skip_size):
            p1, p2, p3 = points[0], points[i], points[-1]
            v1 = [p2.x - p1.x, p2.y - p1.y]
            v2 = [p3.x - p2.x, p3.y - p2.y]
            length_v1 = np.linalg.norm(v1)
            length_v2 = np.linalg.norm(v2)
            cross = np.cross(v1, v2) / (length_v1 * length_v2)
            theta = np.arcsin(cross)
            theta_deg = np.degrees(theta)

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
    def smooth_and_remove_noise(arr):
        arr = np.asarray(arr)
        kernel = np.ones(3) / 3
        smoothed = np.convolve(arr, kernel, mode='same')
        return np.where(smoothed > 0, 1, -1)
    # end smooth_and_remove_noise

# end CurveOrientationCohandler