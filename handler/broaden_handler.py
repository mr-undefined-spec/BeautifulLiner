import math

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/primitive'))
from point import Point
from vector import Vector
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/curve'))
from broad_linear_approximate_curve import BroadLinearApproximateCurve

from basic_handler import BasicHandler

class BroadenHandler(BasicHandler):
    # 
    # The broaden algorithm
    #                                                                                                                                        
    # 0. Prerequisite
    #
    #  Cubic Bezier curves are approximated by line segments with linearize method in CubicBezierCurve
    #   
    #    P1 ...........Q1........................................   P2
    #     __          x  ooooo                                         `
    #      __        x        ooooooooooR1oooooooooooooooooo           ``
    #       _        x            """""""                  oooooooooo    ``
    #        _       x        """""     *****************           oooooo Q2 
    #         _     x      """""*********               **********           `` 
    #          _    x   """" ****                                 ******       `` 
    #          _    x ""  ***                                           ******   ``
    #           _   R0  ***                                                  ***** ```
    #           __ x   **                                                         *** ``
    #            _ x  **                                                            *** ``
    #             _x **                                                               **  ``
    #             __ *                                                                 **  ``
    #             Q0 *                                                                  ***  ``
    #               _*                                                                    ***  ```
    #               _*                                                                      ***  ``
    #                _*                                                                            P3
    #                                                                           
    #                P0                                                        
    #                     * = Points (= Both ends of a line segment)
    #
    #
    #
    #
    # This method broaden line as below
    #
    #
    #  A ******************************************* B
    #
    #                     |
    #                     V
    #
    #                    ************       
    #            ***************************
    #       *************************************
    #  A ******************************************* B
    #       *************************************
    #            ***************************
    #                    ************       
    #
    #
    # Line AB consists of multiple line segments
    #
    #  A o****o******o****o*******o**o****o***o****o B
    #
    # Now turn attention to the line segments at the first two points
    #
    #    This! 
    #    |
    #    V
    #    +----+
    #    |    |
    #  A o****o******o****o*******o**o****o***o****o B
    #
    # Consider it a vector
    #
    #  A o---->******o****o*******o**o****o***o****o B
    #
    # Rotate 90 degrees from the focused vector and find a point slightly away from it.
    #
    #  A o---->******o****o*******o**o****o***o****o B
    #         |
    #         V
    #         x
    #       
    # Compute sameway in the second, third ... line segment
    #
    #  A o---->------>****o*******o**o****o***o****o B
    #         |      |    |       |  |    |   |    |
    #         V      V    V       V  V    V   V    V
    #         x      x    x       x  x    x   x    x
    #       
    # The distance delta from the original line is a position-dependent function.
    # These are small deltas at both ends and large in the center.      
    #       
    #  A o---->------>****o*******o**o****o***o****o B
    #         |      |    |       |  |    |   |    |
    #         V      |    |       |  |    |   |    V
    #         x      V    V       |  |    V   V    x
    #                x    x       V  V    x   x    
    #                             x  x
    #       
    # By calculating this on both sides, a thin line at both ends and a thick line in the center can be obtained.
    #       
    #       
    #                             x  x
    #                x    x       A  A    x   x
    #         x      A    A       |  |    A   A    x
    #         A      |    |       |  |    |   |    A
    #         |      |    |       |  |    |   |    |
    #  A o****o******o****o*******o**o****o***o****o B
    #         |      |    |       |  |    |   |    |
    #         V      |    |       |  |    |   |    V
    #         x      V    V       |  |    V   V    x
    #                x    x       V  V    x   x    
    #                             x  x
    #       

    #
    # In continuaous curve, the method broaden line as below
    #
    #
    #  A ******************************************* B ****************** C
    #
    #                     |
    #                     V
    #
    #                    ************************************       
    #            ************************************************
    #       *********************************************************
    #  A ******************************************* B ****************** C
    #       *********************************************************
    #            ************************************************
    #                    ************************************
    #

    
    @staticmethod
    def __get_delta_point(prev_point, current_point, delta):
        vec_x = current_point.x - prev_point.x
        vec_y = current_point.y - prev_point.y
        len_vec = math.sqrt( vec_x*vec_x + vec_y*vec_y )
        if len_vec == 0:
            return None
        #end
    
        final_x = current_point.x - ( vec_y * delta/len_vec)
        final_y = current_point.y + ( vec_x * delta/len_vec)
        return Point(final_x, final_y)
    #end 

    @staticmethod
    def __get_extrapolation_point(outer_most_point, second_outer_most_point):
        vec = Vector(second_outer_most_point, outer_most_point)
        return Point(outer_most_point.x + vec.x, outer_most_point.y + vec.y)
    #end

    @staticmethod
    def __get_end_point(position, direction_type, end_side_type, prev_point, current_point, broaden_width):
        delta = 0
        if position == "first":
            if direction_type == "going" and end_side_type == "start_side":
                return current_point
            elif direction_type == "going" and end_side_type == "end_side":
                delta = broaden_width
            elif direction_type == "returning" and end_side_type == "start_side":
                delta = broaden_width
            elif direction_type == "returning" and end_side_type == "end_side":
                return current_point
            else:
                raise TypeError("Wrong conditions are set. direction=" + direction_type + ", end_side=" + end_side_type )
            #end
        elif position == "last":
            if direction_type == "going" and end_side_type == "start_side":
                delta = broaden_width
            elif direction_type == "going" and end_side_type == "end_side":
                return current_point
            elif direction_type == "returning" and end_side_type == "start_side":
                return current_point
            elif direction_type == "returning" and end_side_type == "end_side":
                delta = broaden_width
            else:
                raise TypeError("Wrong conditions are set. direction=" + direction_type + ", end_side=" + end_side_type )
            #end
        elif position == "middle":
            delta = broaden_width
        elif position == "first_last":
            return current_point
        #end

        return BroadenHandler.__get_delta_point(prev_point, current_point, delta)
    #end

    @staticmethod
    def __get_slightly_away_control_point_list(ctrl_p_set, broaden_width, is_going, position):
        slightly_away_control_point_list = []


        points = []
        if is_going:
            for ctrl_p in ctrl_p_set:
                points.append(ctrl_p.start)
            #end
            points.append(ctrl_p_set[-1].end)
        else: # is returning
            reversed_going_ctrl_p_list = list( reversed(ctrl_p_set) )
            for ctrl_p in reversed_going_ctrl_p_list:
                points.append(ctrl_p.end)
            #end
            points.append(reversed_going_ctrl_p_list[-1].start)
        #end
    
        half_length = len(points)/2.0 - 0.5 
    
        # first point is equal to original first point
        last_slightly_away_point = points[0]

        # middle points are slightly away points
        for i in range( len(points) - 1 ):
            delta = 0
            if position == "first":
                if is_going:
                    if i < half_length:
                        delta = broaden_width * ( half_length - abs(half_length - i - 1) ) / half_length
                    else:
                        delta = broaden_width
                    #end
                else:
                    if i < half_length:
                        delta = broaden_width
                    else:
                        delta = broaden_width * ( half_length - abs(half_length - i - 1) ) / half_length
                    #end
                #end
            elif position == "last":
                if is_going:
                    if i < half_length:
                        delta = broaden_width
                    else:
                        delta = broaden_width * ( half_length - abs(half_length - i - 1) ) / half_length
                    #end
                else:
                    if i < half_length:
                        delta = broaden_width * ( half_length - abs(half_length - i - 1) ) / half_length
                    else:
                        delta = broaden_width
                    #end
                #end
            elif position == "middle":
                delta = broaden_width
            elif position == "first_last":
                delta = broaden_width * ( half_length - abs(half_length - i - 1) ) / half_length
            #end
            #delta += 0.5
            prev_point = points[i]
            current_point = points[i+1]
            slightly_away_point = BroadenHandler.__get_delta_point(prev_point, current_point, delta)
            if slightly_away_point is not None:
                the_ctrl_p = LinearApproximateCurveControlPoint(last_slightly_away_point, slightly_away_point)
                slightly_away_control_point_list.append(the_ctrl_p)
                last_slightly_away_point = slightly_away_point
            #end
        #end
    
        return slightly_away_control_point_list
    #end 

    @staticmethod
    def process(original_curve, broaden_width, position):
        broad_curve = BroadLinearApproximateCurve()

        tmp_going_ctrl_p_list = BroadenHandler.__get_slightly_away_control_point_list(original_curve._going_ctrl_p_list, broaden_width, True, position)
        for going_ctlr_p in tmp_going_ctrl_p_list:
            broad_curve.append_going(going_ctlr_p)
        #end

        tmp_returning_going_ctrl_p_list = BroadenHandler.__get_slightly_away_control_point_list(original_curve._going_ctrl_p_list, broaden_width, False, position)
        for returning_going_ctlr_p in tmp_returning_going_ctrl_p_list:
            broad_curve.append_returning(returning_going_ctlr_p)
        #end

        return broad_curve
    #end

#end
