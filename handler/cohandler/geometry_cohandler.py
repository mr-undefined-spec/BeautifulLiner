import math
import numpy as np

#import os
#import sys
#sys.path.append(os.path.join(os.path.dirname(__file__), '../model/primitive'))
import math
import numpy as np

class GeometryCohandler:

    @staticmethod
    def get_distance_point_to_segment(start, point, end):
        dx = end.x - start.x
        dy = end.y - start.y
        if dx == 0 and dy == 0:
            return math.hypot(point.x - start.x, point.y - start.y)
        # end if
        t = ((point.x - start.x) * dx + (point.y - start.y) * dy) / (dx * dx + dy * dy)
        intersection_x = start.x + t * dx
        intersection_y = start.y + t * dy
        dist = math.hypot(point.x - intersection_x, point.y - intersection_y)
        return dist
    # end get_distance_point_to_segment

    @staticmethod
    def calculate_angle_between_vectors(v1, v2):
        dot_product = v1[0]*v2[0] + v1[1]*v2[1]
        mag_v1 = math.hypot(v1[0], v1[1])
        mag_v2 = math.hypot(v2[0], v2[1])
        cos_theta = max(-1, min(1, dot_product / (mag_v1 * mag_v2)))
        return math.acos(cos_theta)
    # end calculate_angle_between_vectors

# end GeometryCohandler