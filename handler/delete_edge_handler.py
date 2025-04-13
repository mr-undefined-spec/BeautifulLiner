#import numpy as np

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/curve'))
from linear_approximate_curve import LinearApproximateCurve

from basic_handler import BasicHandler

class DeleteEdgeHandler(BasicHandler):
    @staticmethod
    def process(target_curve, other_curve, delete_ratio):
        """ターゲットの曲線と一本の曲線を比較し、交差したらstart_index, end_indexを更新する"""
        return_curve = LinearApproximateCurve()
        return_curve.copy(target_curve)

        num_segments = len(target_curve)
        start_ignore = int(num_segments * delete_ratio)
        end_ignore = num_segments - start_ignore

        first_intersection_index = None

        for i, the_segment in enumerate(target_curve.going_ctrl_p_list):
            if start_ignore < i and i <= end_ignore:
                continue  # 端部しか交差判定しない
            #end

            the_rect_tuple = the_segment.get_rect_tuple()
            for other_segment in other_curve.get_intersect_segment_set(the_rect_tuple):
                if the_segment.is_intersection(other_segment):
                    first_intersection_index = i
                #end
            #end
        #end

        if first_intersection_index == None:
            return return_curve # 交差がなければ何もしない
        #end

        num_segments = len(target_curve)
        # 切り取られる箇所に応じて start_index または end_index を更新
        if first_intersection_index < num_segments // 2:
            return_curve.update_start_index(first_intersection_index)
        else:
            return_curve.update_end_index(first_intersection_index)
        #end

        #print(return_curve.start_index)
        #print(return_curve.end_index)

        return return_curve
    #end

#end
