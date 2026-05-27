import numpy as np
import math
from model.primitive.point import Point
from util.geometry import Geometry


class SplitRangeHelper:

    @staticmethod
    def create_split_ranges(curve_orientations: np.ndarray, index_offset: int) -> list[tuple[int, int]]:
        ranges = []
        current = curve_orientations[0]
        pre_index = 0
        for i, value in enumerate(curve_orientations):
            if value != current:
                ranges.append((pre_index + index_offset, i + index_offset))
                pre_index = i
                current = value
            # end if
        # end for
        ranges.append((pre_index + index_offset, len(curve_orientations) + index_offset - 1))
        return ranges
    # end create_split_ranges

    @staticmethod
    def find_split_point_by_angle(
        points: list[Point], 
        start_index: int, 
        end_index: int, 
        angle_threshold_deg: float
    ) -> int:
        if len(points) < 3:
            return -1
        # end if
        start = points[start_index]
        end = points[end_index] # 元コードの「end_index - 1」は新生Curveのスライス仕様（閉区間）に合わせて調整
        max_dist = -1
        max_index = -1

        for i in range(start_index + 1, end_index - 1):
            p = points[i]
            dist = Geometry.get_distance_point_to_segment(start, p, end)
            if dist > max_dist:
                max_dist = dist
                max_index = i
            # end if
        # end for

        if max_index == -1:
            return -1
        # end if

        vec1 = (start.x - points[max_index].x, start.y - points[max_index].y)
        vec2 = (end.x - points[max_index].x, end.y - points[max_index].y)
        angle_rad = Geometry.calculate_angle_between_vectors(vec1, vec2)
        angle_deg = math.degrees(angle_rad)

        if angle_deg < angle_threshold_deg:
            return max_index
        else:
            return -1
        # end if
    # end find_split_point_by_angle

# end class