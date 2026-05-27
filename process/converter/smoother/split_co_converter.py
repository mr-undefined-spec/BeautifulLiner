import numpy as np

from model.primitive.curve import Curve, CurveType
from process.converter.smoother.splitter.curve_orientation_helper import CurveOrientationHelper
from process.converter.smoother.splitter.split_range_helper import SplitRangeHelper


class SplitCoConverter:

    @staticmethod
    def __create_curve_orientations(curve: Curve) -> np.ndarray:
        points = curve.points
        if len(points) < 30:
            return np.ones(len(points))
        # end if

        skip_size = max(1, int(len(points) * 0.1))

        if CurveOrientationHelper.are_points_almost_linear(points, skip_size):
            return np.ones(len(points))
        # end if

        return CurveOrientationHelper.create_curve_orientations(points, skip_size)
    # end __create_curve_orientations

    @staticmethod
    def convert_to_multiple(curve: Curve) -> list[Curve]:
        """長い1本のLINEAR_APPROXIMATE曲線を変曲点・急角で切り分け、複数のCurveオブジェクトとして返す"""
        if curve.curve_type != CurveType.LINEAR_APPROXIMATE:
            return [curve]
        # end if

        points = curve.points
        curve_orientations = SplitCoConverter.__create_curve_orientations(curve)
        curve_orientations = CurveOrientationHelper.smooth_and_remove_noise(curve_orientations)
        
        # 内部でのみインデックスの区間（index_offset=0）を扱う
        once_split_curve_ranges = SplitRangeHelper.create_split_ranges(curve_orientations, 0)

        split_curve_ranges = []
        for r in once_split_curve_ranges:
            start_idx, end_idx = r[0], r[1]
            if end_idx - start_idx < 30:
                split_curve_ranges.append((start_idx, end_idx))
                continue
            # end if

            ratio = 0.1
            min_idx = start_idx + int((end_idx - start_idx) * ratio)
            max_idx = end_idx - int((end_idx - start_idx) * ratio)

            split_idx = SplitRangeHelper.find_split_point_by_angle(points, start_idx, end_idx, 90.0)
            if split_idx != -1 and min_idx < split_idx < max_idx:
                split_curve_ranges.append((start_idx, split_idx))
                split_curve_ranges.append((split_idx + 1, end_idx))
            else:
                split_curve_ranges.append((start_idx, end_idx))
            # end if
        # end for

        # インデックス範囲から、実際に新生Curveインスタンスのリストを組み立てる
        split_curves = []
        for start, end in split_curve_ranges:
            # 元の点列から指定範囲をスライス (endは未満ではなく「まで」として含むため +1)
            sub_points = points[start:end + 1]
            
            if len(sub_points) >= 2:
                split_curves.append(
                    Curve(
                        points=sub_points,
                        curve_type=CurveType.LINEAR_APPROXIMATE,
                        is_broad=curve.is_broad
                    )
                )
            # end if
        # end for

        return split_curves
    # end convert_to_multiple

# end class