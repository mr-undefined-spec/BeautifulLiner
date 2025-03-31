import os
import sys

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

from rtree import index

class DeleteEdgeHandler(BasicHandler):
    @staticmethod
    def __intersect_segments(seg1, seg2):
        """２つの線分が交差しているか判定し、交点を求める"""
        def ccw(A, B, C):
            return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)
        #end

        A, B = seg1.start, seg1.end
        C, D = seg2.start, seg2.end
        if ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D):
            denom = (D.y - C.y) * (B.x - A.x) - (D.x - C.x) * (B.y - A.y)
            if denom == 0:
                return None  # 平行な線分
            #end
            ua = ((D.x - C.x) * (A.y - C.y) - (D.y - C.y) * (A.x - C.x)) / denom
            intersection = (A.x + ua * (B.x - A.x), A.y + ua * (B.y - A.y))
            return intersection
        #end

        return None
    #end

    @staticmethod
    def process(target_curve, other_curve, delete_edge_ratio):
        """ターゲットの曲線と一本の曲線を比較し、交差したらstart_index, end_indexを更新する"""
        return_curve = LinearApproximateCurve()
        return_curve.copy(target_curve)

        idx = index.Index()

        # 他の曲線の線分をR-treeに登録
        for i, bbox in enumerate(other_curve.get_bounding_boxes()):
            idx.insert(i, bbox, obj=i)
        #end

        num_segments = len(target_curve)
        start_ignore = int(num_segments * delete_edge_ratio)
        end_ignore = num_segments - start_ignore

        intersections = []

        for i, (seg, bbox) in enumerate(zip(target_curve.ctrl_p_set, target_curve.get_bounding_boxes())):
            if start_ignore < i and i <= end_ignore:
                continue  # 端部しか交差判定しない
            #end

            possible_intersections = list(idx.intersection(bbox, objects=True))
            for j in possible_intersections:
                other_seg = other_curve[j.object]
                intersection = DeleteEdgeHandler.__intersect_segments(seg, other_seg)
                if intersection:
                    intersections.append((i, intersection))
                #end
            #end for j
        #end for i

        if not intersections:
            return  # 交差がなければ何もしない
        #end

        # 最初の交点で切り取る
        first_intersection_index, first_intersection = min(intersections, key=lambda x: x[0])

        # 切り取られる箇所に応じて start_index または end_index を更新
        if first_intersection_index < num_segments // 2:
            return_curve.update_start_index(first_intersection_index)
        else:
            return_curve.update_end_index(first_intersection_index)
        #end

        return return_curve
    #end

#end
