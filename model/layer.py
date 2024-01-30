
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

    def convert_to_linear_approximate_curve(self, micro_segment_length):
        linear_approximate_layer = Layer()
        for curve in self.__curve_set:
            linear_approximate_curve = curve.convert_to_linear_approximate_curve(micro_segment_length)
            linear_approximate_layer.append( linear_approximate_curve )
        #end
        return linear_approximate_layer
    #end
#end

