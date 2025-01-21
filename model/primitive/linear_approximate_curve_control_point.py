
import numpy as np

from point import Point

class LinearApproximateCurveControlPoint():
    def __init__(self, start, end):
        if not isinstance(start, Point):
            raise TypeError("p0 must be Point")
        #end if
        if not isinstance(end, Point):
            raise TypeError("p1 must be Point")
        #end if
        self.__start = start
        self.__end   = end
    #end

    @property
    def s(self):
        return self.__start
    #end

    @property
    def e(self):
        return self.__end
    #end

    def get_max_x(self):
        return max(self.__start.x, self.__end.x)
    #end
    def get_min_x(self):
        return min(self.__start.x, self.__end.x)
    #end
    def get_max_y(self):
        return max(self.__start.y, self.__end.y)
    #end
    def get_min_y(self):
        return min(self.__start.y, self.__end.y)
    #end

    def __dot(self, o, a, b):
        return (a.x - o.x) * (b.x - o.x) + (a.y - o.y) * (b.y - o.y)
    #end
    def __cross(self, o, a, b):
        return (a.x - o.x) * (b.y - o.y) - (b.x - o.x) * (a.y - o.y)
    #end

    def is_intersection(self, other_segment):
        c0 = self.__cross(self.__start, self.__end, other_segment.s)
        c1 = self.__cross(self.__start, self.__end, other_segment.e)
        d0 = self.__cross(other_segment.s, other_segment.e, self.__start)
        d1 = self.__cross(other_segment.s, other_segment.e, self.__end)
        if c0 == d1 == 0:
            e0 = self.__dot(self.__start, self.__end, other_segment.s)
            e1 = self.__dot(self.__start, self.__end, other_segment.e)
            if not e0 < e1:
                e0, e1 = e1, e0
            #end
            dist = self.__start.distance(self.__end)
            return e0 <= dist*dist and 0 <= e1
        #end
        return c0 * c1 <= 0 and d0 * d1 <= 0
    #end

    def intersection(self, other_segment):
        if self.is_intersection(other_segment):
            a_self  = self.__end.x - self.__start.x
            b_self  = self.__end.y - self.__start.y
            a_other = other_segment.e.x - other_segment.s.x
            b_other = other_segment.e.y - other_segment.s.y

            d = a_self*b_other - a_other*b_self
            t = b_other * (other_segment.s.x - self.__start.x) - a_other * (other_segment.s.y - self.__start.y)
            return Point(self.__start.x + a_self*t/d, self.__start.y + b_self*t/d)
        else:
            raise ValueError("ERROR. Not intersect. Please use \"is_intersection\" method before calling \"intersection\" method.")
        #end if
    #end

    def get_rect_tuple(self):
        min_x = min(self.__start.x, self.__end.x)
        max_x = max(self.__start.x, self.__end.x)
        min_y = min(self.__start.y, self.__end.y)
        max_y = max(self.__start.y, self.__end.y)

        return (min_x, min_y, max_x, max_y)
    #end

    def get_distance_to_point(self, point):
        this_vec = ((self.__end.x - self.__start.x), (self.__end.y - self.__start.y))#, line_end - self.__start
        point_vec = ((point.x - self.__start.x), (point.y - self.__start.y))
        line_length = np.linalg.norm(this_vec)
        if line_length == 0:
            return np.linalg.norm(point_vec)
        #end
        projection = np.dot(point_vec, this_vec) / line_length
        if projection < 0:
            return np.linalg.norm(point_vec)
        elif projection > line_length:
            point_vec_from_end = ((point.x - self.__end.x), (point.y - self.__end.y))
            return np.linalg.norm(point_vec_from_end)
        else:
            projection_point_x = self.__start.x + projection * this_vec[0] / line_length
            projection_point_y = self.__start.y + projection * this_vec[1] / line_length
            projection_point_vec_from_point = ((projection_point_x - point.x), (projection_point_y - point.y))
            return np.linalg.norm(projection_point_vec_from_point)
        #end
    #end

    def get_min_distance_to_segment(self, other_segment):
        distanse_this_seg_to_other_start = self.get_distance_to_point(other_segment.s)
        distanse_this_seg_to_other_end   = self.get_distance_to_point(other_segment.e)
        distance_other_seg_to_this_start = other_segment.get_distance_to_point(self.__start)
        distance_other_seg_to_this_end   = other_segment.get_distance_to_point(self.__end)

        return min(distanse_this_seg_to_other_start, distanse_this_seg_to_other_end, distance_other_seg_to_this_start, distance_other_seg_to_this_end)
    #end

    def get_average_distance_to_segment(self, other_segment):
        distanse_this_seg_to_other_start = self.get_distance_to_point(other_segment.s)
        distanse_this_seg_to_other_end   = self.get_distance_to_point(other_segment.e)
        distance_other_seg_to_this_start = other_segment.get_distance_to_point(self.__start)
        distance_other_seg_to_this_end   = other_segment.get_distance_to_point(self.__end)

        return (distanse_this_seg_to_other_start + distanse_this_seg_to_other_end + distance_other_seg_to_this_start + distance_other_seg_to_this_end) / 4.0
    #end

    def get_perpendicular_intersection_point_from_point(self, point):
        # Calculate the differences
        dx = self.__end.x - self.__start.x
        dy = self.__end.y - self.__start.y
        
        # If the segment is a point, return the point itself
        if dx == 0 and dy == 0:
            return Point(self.__start.x, self.__start.y)
        
        # Calculate the parameter t for the projection
        t = ((point.x - self.__start.x) * dx + (point.y - self.__start.y) * dy) / (dx * dx + dy * dy)
        
        # Compute the intersection point
        intersection_x = self.__start.x + t * dx
        intersection_y = self.__start.y + t * dy
        
        return Point(intersection_x, intersection_y)
    #end

    def __str__(self):
        s = ""
        s += str(self.__start) + "\n"
        s += str(self.__end) + "\n"
        return s
    #end 
    def to_str(self, is_first_ctrl_p):
        s = ""
        if is_first_ctrl_p:
            s += "M " + str(self.__start) + " "
        #end
        s += "L " + str(self.__end) + " "
        return s
    #end

    def __minus__(self, other):
        return LinearApproximateCurveControlPoint(self.__start - other, self.__end - other) 
#end

