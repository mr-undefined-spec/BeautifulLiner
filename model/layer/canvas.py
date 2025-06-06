#import numpy as np

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../layer'))
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from cubic_bezier_curve import CubicBezierCurve
from layer import Layer


class Canvas:
    #
    # public
    #
    def __init__(self):
        self.__layer_list = []

        self.__view_box = ""
        self.__doc      = None
        '''
        self.__total_path_num = 0

        if not mode in ["CUI", "GUI", "TEST"]:
            raise ValueError('The arg "mode" can be "CUI", "GUI" or "TEST"')
        #end
        self.__mode = mode

        self.__progress_bar = progress_bar
        self.__log_text     = log_text

        self.__view_box = None
        '''
    #end

    def set_doc(self, val):
        self.__doc = val
    #end

    @property
    def doc(self):
        return self.__doc
    #end

    def set_view_box(self, val):
        self.__view_box = val
    #end

    @property
    def view_box(self):
        return self.__view_box
    #end

    def get_bbox(self):
        arr = self.__view_box.split(",")
        return ( float(arr[0]), float(arr[1]), float(arr[2]), float(arr[3]) )
    #end

    def append(self, layer):
        if not isinstance(layer, Layer):
            raise TypeError("The argument of the append method must be a Layer")
        #end if
        self.__layer_list.append(layer)
    #end def

    def __getitem__(self, i):
        return self.__layer_list[i]
    #end def

    def __iter__(self):
        self.__index = 0
        return self
    #end def
    def __next__(self):
        if self.__index >= len(self.__layer_list): raise StopIteration
        self.__index += 1
        return self.__layer_list[self.__index-1]
    #end def

    def get_total_curve_num(self):
        total_curve_num = 0
        for layer in self.__layer_list:
            for curve in layer:
                total_curve_num += 1
            #end
        #end
        return total_curve_num
    #end

#end

