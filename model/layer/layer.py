import os
import sys

import copy

sys.path.append(os.path.join(os.path.dirname(__file__), '../primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../curve'))

from point import Point

from curve_set import CurveSet
import tkinter as tk

from enum import Enum

class EndpointStyle(Enum):
    BOTH_POINTED = "both_pointed"
    BOTH_WIDE = "both_wide"
#end

class Layer:
    def __init__(self, name):
        if not type(name) is str:
            raise TypeError("The 1st argument \"layer_name\" of the append method must be a str")
        #end
        self.__name = name

        self.__curve_set_list = []   

        self.__is_fill = False
        self.__color   = "#000000"
        self.__endpoint_style   = EndpointStyle.BOTH_POINTED
    #end

    @property
    def name(self):
        return self.__name
    #end

    @property
    def is_fill(self):
        return self.__is_fill
    #end

    @property
    def color(self):
        return self.__color
    #end

    @property
    def endpoint_style(self):
        return self.__endpoint_style
    #end

    def __getitem__(self, i):
        return self.__curve_set_list[i]
    #end

    def __iter__(self):
        self.__index = 0
        return self
    #end
    def __next__(self):
        if self.__index >= len(self.__curve_set_list): raise StopIteration
        self.__index += 1
        return self.__curve_set_list[self.__index-1]
    #end

    def append(self, curve_set):
        if not isinstance(curve_set, CurveSet):
            raise TypeError("The argument of the append method must be a CurveSet(SingleCurveSet or MultiCurveSet)")
        #end if
        self.__curve_set_list.append(curve_set)
    #end

    def set_write_options(self, is_fill, color, endpoint_style):
        self.__is_fill = is_fill
        self.__color   = color

        if not isinstance(endpoint_style, EndpointStyle):
            raise TypeError("The argument \"endpoint_style\" of the set_write_options method must be an EndpointStyle")
        #end
        self.__endpoint_style   = endpoint_style
    #end


#end

