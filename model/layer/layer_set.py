
from xml.dom import minidom

from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from cubic_bezier_curve import CubicBezierCurve
from layer import Layer

import tkinter as tk

import re

class LayerSet:
    #
    # public
    #
    def __init__(self):
        self.__layer_set = []

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

    '''

    def set_doc(self, val):
        self.__doc = val
    #end

    @property
    def doc(self):
        return self.__doc
    #end
    '''

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
        self.__layer_set.append(layer)
    #end def

    def __getitem__(self, i):
        return self.__layer_set[i]
    #end def

    def __iter__(self):
        self.__index = 0
        return self
    #end def
    def __next__(self):
        if self.__index >= len(self.__layer_set): raise StopIteration
        self.__index += 1
        return self.__layer_set[self.__index-1]
    #end def

#end

