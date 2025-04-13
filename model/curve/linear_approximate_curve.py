from pyqtree import Index
import numpy as np

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../primitive'))
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from rectangular import Rectangular

from curve import Curve

class LinearApproximateCurve(Curve):
    def __init__(self):
        super().__init__()

        self.min_x = 999999
        self.max_x = -999999
        self.min_y = 999999
        self.max_y = -999999

        self._start_index = 0
        self._end_index   = -1
    #end

    def _get_the_end(self):
        # if self._end_index is initial state, then ...
        if (self._end_index == -1):
            return len(self._going_ctrl_p_list) 
        #end
        # if self._end_index is over the array size
        if ( self._end_index >= len(self._going_ctrl_p_list) ):
            return len(self._going_ctrl_p_list)
        #end
        # others, self._end_index is correct
        return self._end_index
    #end

    def append(self, linear_ctrl_p):
        if not isinstance(linear_ctrl_p, LinearApproximateCurveControlPoint):
            raise TypeError("The argument of the append method must be a LinearApproximateCurveControlPoint")
        #end

        self.min_x = min(self.min_x, linear_ctrl_p.start.x, linear_ctrl_p.end.x)
        self.max_x = max(self.max_x, linear_ctrl_p.start.x, linear_ctrl_p.end.x)
        self.min_y = min(self.min_y, linear_ctrl_p.start.y, linear_ctrl_p.end.y)
        self.max_y = max(self.max_y, linear_ctrl_p.start.y, linear_ctrl_p.end.y)

        self._going_ctrl_p_list.append(linear_ctrl_p)
    #end

    def to_str(self):
        s = ""
        the_end = self._get_the_end()
        for i in range( self._start_index, the_end ):
            ctrl_p = self._going_ctrl_p_list[i]
            s += ctrl_p.to_str(i==self._start_index)
        #end
        return s
    #end

    @property
    def rect(self):
        return Rectangular(self.min_x, self.max_x, self.min_y, self.max_y)
    #end

    def get_points(self):
        points = []
        points.append(self._going_ctrl_p_list[self._start_index].start)

        the_end = self._get_the_end()
        for i in range( self._start_index, the_end ):
            points.append(self._going_ctrl_p_list[i].end)
        #end
        return points
    #end

    def copy(self, other_linear_approximate_curve):
        for ctrl_p in other_linear_approximate_curve:
            self.append(ctrl_p)
        #end
        self._start_index = other_linear_approximate_curve.start_index
        self._end_index = other_linear_approximate_curve.end_index
    #end


    def get_start_points(self):
        start_points = []
        for ctrl_p in self._going_ctrl_p_list:
            start_points.append(ctrl_p.start)
        #end
        return start_points
    #end

    def get_start_points_as_numpy_array(self):
        start_points = []
        for ctrl_p in self._going_ctrl_p_list:
            start_points.append([ctrl_p.start.x, ctrl_p.start.y])
        #end
        return np.array(start_points)
    #end

    def get_bounding_boxes(self):
        """各線分に対し、軸平行境界ボックス(AABB)を取得"""
        return [
            (min(ctrl_p.start.x, ctrl_p.end.x), min(ctrl_p.start.y, ctrl_p.end.y), 
             max(ctrl_p.start.x, ctrl_p.end.x), max(ctrl_p.start.y, ctrl_p.end.y))
            for ctrl_p in self._going_ctrl_p_list
        ]
    #end

    def update_start_index(self, start_index):
        if( self._start_index < start_index ):
            self._start_index = start_index
        #end
    #end

    def update_end_index(self, end_index):
        if( self._end_index == -1):
            self._end_index = end_index
        elif( end_index < self._end_index ):
            self._end_index = end_index
        #end
    #end

    def get_going_ctrl_p_list(self):
        return_going_ctrl_p_list = []
        the_end = self._get_the_end()
        for i in range( self._start_index, the_end ):
            return_going_ctrl_p_list.append( self._going_ctrl_p_list[i] )
        #end
        return return_going_ctrl_p_list
    #end

    def create_qtree_going_ctrl_p_list(self, bbox):
        
        self.qtree_going_ctrl_p_list = Index(bbox=bbox)

        for ctrl_p in self._going_ctrl_p_list:
            rect_tuple = ctrl_p.get_rect_tuple()
            self.qtree_going_ctrl_p_list.insert(ctrl_p, rect_tuple)
        #end
    #end

    def get_intersect_segment_set(self, target_rect_tuple):
        return self.qtree_going_ctrl_p_list.intersect(target_rect_tuple)
    #end

    """



    def get_min_distance_to_point(self, point):
        min_distance = 999999
        for i, ctrl_p in enumerate(self._going_ctrl_p_list):
            if ctrl_p.get_distance_to_point(point) < min_distance:
                min_distance = ctrl_p.get_distance_to_point(point)
            #end
        #end

        return min_distance
    #end

    def get_ctrl_p_index_at_min_distance_to_point(self, point):
        the_index = None
        min_distance = 999999
        for i, ctrl_p in enumerate(self._going_ctrl_p_list):
            if ctrl_p.get_distance_to_point(point) < min_distance:
                the_index = i
                min_distance = ctrl_p.get_distance_to_point(point)
            #end
        #end

        return the_index
    #end

    def approximate_line_through_points(points):
        if len(points) < 2:
            raise ValueError("At least two points are required to define a line.")

        x_coords, y_coords = zip(*[(point.x, point.y) for point in points])
        
        A = np.vstack([x_coords, np.ones(len(x_coords))]).T
        m, c = np.linalg.lstsq(A, y_coords, rcond=None)[0]
        
        return m, c
    #end
    def generate_approximate_lines_through_points(self, points):
        lines = []
        for i in range(len(points)-1):
            x0, y0 = points[i].x, points[i].y
            x1, y1 = points[i+1].x, points[i+1].y
            m = (y1-y0)/(x1-x0)
            c = y0 - m*x0
            lines.append((m,c))
        #end
        return lines
    #end
    def calculate_angle_between_approximate_lines_through_points(self, points_a, points_b):
        line_a = self.generate_approximate_lines_through_points(points_a)
        line_b = self.generate_approximate_lines_through_points(points_b)

        m1, c1 = line_a[-1]
        m2, c2 = line_b[0]

        angle = math.atan2(m2 - m1, 1 + m1 * m2)
        return angle
    #end

    def is_continuaous_at_start_side(self, other_curve, distance_threshold):
        other_end_point = other_curve.sequential_points[-1]

        this_index_nearest_other_end_point = self.get_ctrl_p_index_at_min_distance_to_point(other_end_point)
        this_half_index = int(this_index_nearest_other_end_point/2)
        this_quarter_index = int(this_index_nearest_other_end_point/4)
        this_third_this_quarter_index = int(this_index_nearest_other_end_point/4*3)
        if this_index_nearest_other_end_point < 4:
            return False
        #end
        this_points = []
        for i in [0, this_quarter_index, this_half_index, this_third_this_quarter_index, this_index_nearest_other_end_point]:
            this_points.append(self.sequential_points[i])
            #print(self.sequential_points[i])
        #end
        
        #print( [0, this_quarter_index, this_half_index, this_third_this_quarter_index, this_index_nearest_other_end_point])

        other_index_nearest_this_start_point = other_curve.get_ctrl_p_index_at_min_distance_to_point(self.sequential_points[0])
        delta_index = len(other_curve.sequential_points) - other_index_nearest_this_start_point - 1
        if delta_index < 4:
            return False
        #end
        other_quarter_index = int(other_index_nearest_this_start_point + delta_index/4)
        other_half_index = int(other_index_nearest_this_start_point + delta_index/2)
        other_third_other_quarter_index = int(other_index_nearest_this_start_point + delta_index/4*3)
        #print([other_index_nearest_this_start_point, other_quarter_index, other_half_index, other_third_other_quarter_index, len(other_curve.sequential_points)])

        other_points = []
        for i in [other_index_nearest_this_start_point, other_quarter_index, other_half_index, other_third_other_quarter_index, -1]:
            other_points.append(other_curve.sequential_points[i])
            #print(other_curve.sequential_points[i])
        #end
        #other_points.append(other_curve.sequential_points[-1])

        angle = self.calculate_angle_between_approximate_lines_through_points(this_points, other_points)
        #print(angle*180/math.pi)

        if angle*180/math.pi > 30.0 or angle*180/math.pi < -30.0:
            return False
        #end


        average_distance = 0.0
        for i in [0, this_quarter_index, this_half_index, this_third_this_quarter_index, this_index_nearest_other_end_point]:
            point = self.sequential_points[i]
            average_distance += other_curve.get_min_distance_to_point(point)
        #end

        average_distance /= 5.0
        #print("start", average_distance)
        return average_distance < distance_threshold
    #end

    def is_continuaous_at_end_side(self, other_curve, distance_threshold):
        other_start_point = other_curve.sequential_points[0]

        this_index_nearest_other_start_point = self.get_ctrl_p_index_at_min_distance_to_point(other_start_point)

        delta_index = len(self.sequential_points) - this_index_nearest_other_start_point - 1
        if delta_index < 4:
            return False
        #end
        #print(this_index_nearest_other_start_point, delta_index)

        this_half_index = int(this_index_nearest_other_start_point + delta_index/2)
        this_quarter_index = int(this_index_nearest_other_start_point + delta_index/4)
        this_third_this_quarter_index = int(this_index_nearest_other_start_point + delta_index/4*3)
        this_points = []
        for i in [this_index_nearest_other_start_point, this_quarter_index, this_half_index, this_third_this_quarter_index, len(self.sequential_points)-1]:
            this_points.append(self.sequential_points[i])
            #print(self.sequential_points[i])
        #end

        #print([this_index_nearest_other_start_point, this_quarter_index, this_half_index, this_third_this_quarter_index, len(self.sequential_points)-1])

        other_index_nearest_this_end_point = other_curve.get_ctrl_p_index_at_min_distance_to_point(self.sequential_points[-1])
        if other_index_nearest_this_end_point < 4:
            return False
        #end
        other_quarter_index = int(other_index_nearest_this_end_point/4)
        other_half_index = int(other_index_nearest_this_end_point/2)
        other_third_other_quarter_index = int(other_index_nearest_this_end_point/4*3)
        #print([other_index_nearest_this_start_point, other_quarter_index, other_half_index, other_third_other_quarter_index, len(other_curve.sequential_points)])

        other_points = []
        for i in [0, other_quarter_index, other_half_index, other_third_other_quarter_index, other_index_nearest_this_end_point]:
            other_points.append(other_curve.sequential_points[i])
            #print(other_curve.sequential_points[i])
        #end

        angle = self.calculate_angle_between_approximate_lines_through_points(this_points, other_points)
        #print(angle*180/math.pi)

        if angle*180/math.pi > 30.0 or angle*180/math.pi < -30.0:
            return False
        #end

        average_distance = 0.0
        for i in [this_index_nearest_other_start_point, this_quarter_index, this_half_index, this_third_this_quarter_index, len(self.sequential_points)-1]:
            point = self.sequential_points[i]
            average_distance += other_curve.get_min_distance_to_point(point)
        #end

        average_distance /= 5.0
        #print("end", average_distance)
        return average_distance < distance_threshold
    #end

    def get_perpendicular_intersection_point_from_point(self, point):
        the_index = self.get_ctrl_p_index_at_min_distance_to_point(point)
        return self._going_ctrl_p_list[the_index].get_perpendicular_intersection_point_from_point(point)
    #end

    def create_connection_point_at_start_point(self, other_curve):
        start_point = self.sequential_points[0]
        self.start_connection_point = other_curve.get_perpendicular_intersection_point_from_point(start_point)
        #print(self.start_connection_point)
    #end

    def create_connection_point_at_end_point(self, other_curve):
        end_point = self.sequential_points[-1]
        self.end_connection_point = other_curve.get_perpendicular_intersection_point_from_point(end_point)
        #print(self.end_connection_point)
    #end
    """

    @property
    def start_index(self):
        return self._start_index
    #end
    @property
    def end_index(self):
        return self._end_index
    #end



    def update_start_end_index_with_intersection(self, other_curve, ratio):
        the_end_of_start_side_index = int( len(self._going_ctrl_p_list)*ratio )
        for i in range( self._start_index, the_end_of_start_side_index ):
            the_segment = self._going_ctrl_p_list[i]
            the_rect_tuple = the_segment.get_rect_tuple()
            for other_segment in other_curve.__get_intersect_segment_set(the_rect_tuple):
                if the_segment.is_intersection(other_segment):
                    self._start_index = i
                #end
            #end
        #end

        the_start_of_end_side_index = int( len(self._going_ctrl_p_list)*(1.0-ratio) )
        the_end = self._get_the_end()
        for i in range( the_start_of_end_side_index, the_end ):
            the_segment = self._going_ctrl_p_list[i]
            the_rect_tuple = the_segment.get_rect_tuple()
            for other_segment in other_curve.__get_intersect_segment_set(the_rect_tuple):
                if the_segment.is_intersection(other_segment):
                    self._end_index = i
                #end
            #end
        #end
    #end 

    def __get_nearest_ctrl_p_index_to_point(self, point):
        min_distance = 999999
        the_index = None
        for i, ctrl_p in enumerate(self._going_ctrl_p_list):
            if ctrl_p.get_distance_to_point(point) < min_distance:
                the_index = i
                min_distance = ctrl_p.get_distance_to_point(point)
            #end
        #end
        return the_index
    #end

    def overwrite_start_end_index_finding_nearest(self, midpoint_start, midpoint_end):
        if midpoint_start is not None:
            self._start_index = self.__get_nearest_ctrl_p_index_to_point(midpoint_start)
        #end
        if midpoint_end is not None:
            self._end_index = self.__get_nearest_ctrl_p_index_to_point(midpoint_end)
        #end

        #print(self._start_index, self._end_index, len(self._going_ctrl_p_list))
    #end 


#end