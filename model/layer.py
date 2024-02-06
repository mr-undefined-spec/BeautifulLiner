
import copy

from point import Point
from control_point import LinearApproximateCurveControlPoint

from curve import Curve
class Layer:
    def __init__(self):
        self.__curve_set = []
    #end

    def __getitem__(self, i):
        return self.__curve_set[i]
    #end def

    def __iter__(self):
        self.__index = 0
        return self
    #end def
    def __next__(self):
        if self.__index >= len(self.__curve_set): raise StopIteration
        self.__index += 1
        return self.__curve_set[self.__index-1]
    #end def

    def append(self, curve):
        if not isinstance(curve, Curve):
            raise TypeError("The argument of the append method must be a Curve(CubicBezierCurve or LinearApproximateCurve)")
        #end if
        self.__curve_set.append(curve)
    #end def

    def to_svg(self):
        s = ''
        for curve in self.__curve_set:
            s += '<path d="'
            s += curve.to_svg()
            s += '" fill="none" opacity="1" stroke="#ff0000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" />\n'
        #end
        return s
    #end

    def linearize(self, micro_segment_length):
        linear_approximate_layer = Layer()
        for curve in self.__curve_set:
            linear_approximate_curve = curve.linearize(micro_segment_length)
            linear_approximate_layer.append( linear_approximate_curve )
        #end
        return linear_approximate_layer
    #end

    def smoothen(self):
        new_layer = Layer()
        for curve in self.__curve_set:
            new_layer.append( curve.smoothen() )
        #end
        return new_layer
    #end

    def __get_edge_deleted_curve(self, target_curve, ratio):
        new_curve = copy.deepcopy(target_curve)

        intersected_curve_set = []
        for curve in self.__curve_set:
            if curve == target_curve:
                continue
            #end
            if target_curve.rect.test_collision(curve.rect):
                intersected_curve_set.append(curve)
            #end
        #end

        for intersected_curve in intersected_curve_set:
            new_curve.update_start_end_index_with_intersection(intersected_curve, ratio)
        #end

        return new_curve
    #end

    def delete_edge(self, ratio):
        new_layer = Layer()
        for curve in self.__curve_set:
            curve.create_intersect_judge_rectangle()
        #end
        for curve in self.__curve_set:
            new_layer.append( self.__get_edge_deleted_curve(curve, ratio) )
        #end
        return new_layer
    #end

    def broaden(self, broaden_width):
        new_layer = Layer()
        for curve in self.__curve_set:
            new_layer.append( curve.broaden(broaden_width) )
        #end
        return new_layer
    #end
#end

