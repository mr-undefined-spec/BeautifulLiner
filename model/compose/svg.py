
from xml.dom import minidom

from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from cubic_bezier_curve import CubicBezierCurve
from layer import Layer

import tkinter as tk

import re
class LayerData:
    def __init__(self, name, path_data):
        self.name = name
        self.path_data = path_data
    #end
#end

class Svg:
    #
    # public
    #
    def __init__(self, global_calc_step, mode, progress_bar=None, log_text=None):
        self.__global_calc_step = global_calc_step

        self.__layers = []
        self.__view_box = ""
        self.__total_path_num = 0

        if not mode in ["CUI", "GUI", "TEST"]:
            raise ValueError('The arg "mode" can be "CUI", "GUI" or "TEST"')
        #end
        self.__mode = mode

        self.__progress_bar = progress_bar
        self.__log_text     = log_text

        self.__doc      = None
        self.__view_box = None
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


    def append(self, layer_name, layer):
        if not type(layer_name) is str:
            raise TypeError("The 1st argument \"layer_name\" of the append method must be a str")
        if not isinstance(layer, Layer):
            raise TypeError("The argument of the append method must be a Layer")
        #end if
        self.__layers.append( LayerData(layer_name, layer) )
    #end def

    def __getitem__(self, i):
        return self.__layers[i]
    #end def

    def __iter__(self):
        self.__index = 0
        return self
    #end def
    def __next__(self):
        if self.__index >= len(self.__layers): raise StopIteration
        self.__index += 1
        return self.__layers[self.__index-1]
    #end def

    def set_write_options(self, is_fill, color):
        for layer in self.__layers:
            layer.path_data.set_write_options(is_fill, color)
        #end
    #end

    def linearize(self, micro_segment_length):
        self.__global_calc_step += 1
        new_svg = Svg(self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
        new_svg.set_view_box( self.__view_box )
        for layer in self.__layers:
            new_layer = layer.path_data.linearize(micro_segment_length, self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
            new_svg.append(layer.name, new_layer)
        #end
        return new_svg
    #end

    def thin_smoothen(self):
        self.__global_calc_step += 1
        new_svg = Svg(self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
        new_svg.set_view_box( self.__view_box )
        for layer in self.__layers:
            new_svg.append(layer.name, layer.path_data.thin_smoothen(self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text) )
        #end
        return new_svg
    #end

    def special_smoothen_for_hair(self):
        self.__global_calc_step += 1
        new_svg = Svg(self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
        new_svg.set_view_box( self.__view_box )
        for layer in self.__layers:
            new_svg.append(layer.name, layer.path_data.special_smoothen_for_hair(self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text) )
        #end
        return new_svg
    #end

    def create_intersect_judge_rectangle(self):
        self.__global_calc_step += 1
        bbox = self.get_bbox()
        for layer in self.__layers:
            layer.path_data.create_intersect_judge_rectangle(bbox)
        #end
    #end

    def create_sequential_points_and_edge_sequential_points(self):
        self.__global_calc_step += 1
        for layer in self.__layers:
            layer.path_data.create_sequential_points_and_edge_sequential_points()
        #end
    #end

    def create_continuous_curve_index_group(self, distance_threshold):
        
        for layer in self.__layers:
            layer.path_data.create_continuous_curve_index_group( distance_threshold)
        #end
    #end

    def create_connection_point(self):
        for layer in self.__layers:
            layer.path_data.create_connection_point()
        #end
    #end


    def delete_edge(self, ratio):
        self.__global_calc_step += 1
        new_svg = Svg(self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
        new_svg.set_view_box( self.__view_box )
        bbox = self.get_bbox()
        for layer in self.__layers:
#            new_layer = layer.path_data.delete_edge(bbox, ratio, self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
            new_layer = layer.path_data.delete_edge2(bbox, ratio, self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
            new_layer.set_continuous_curve_index_group(layer.path_data.continuous_curve_index_group)
            new_svg.append(layer.name, new_layer)
        #end
        return new_svg
    #end

    def broaden(self, broaden_width):
        self.__global_calc_step += 2
        new_svg = Svg(self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
        # delete edge process has 2 global_calc_step, so increment 2
        new_svg.set_view_box( self.__view_box )
        for layer in self.__layers:
#            new_layer = layer.path_data.broaden(broaden_width, self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
            new_layer = layer.path_data.broaden2(broaden_width, self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
            new_layer.set_continuous_curve_index_group(layer.path_data.continuous_curve_index_group)
            #print(new_layer.continuous_curve_index_group)
            new_svg.append("B_" + layer.name, new_layer)
        #end
        return new_svg
    #end

    def broad_smoothen(self):
        self.__global_calc_step += 1
        new_svg = Svg(self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
        new_svg.set_view_box( self.__view_box )
        for layer in self.__layers:
            new_layer = layer.path_data.broad_smoothen(self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
            new_layer.set_continuous_curve_index_group(layer.path_data.continuous_curve_index_group)
            new_svg.append(layer.name, new_layer)
        #end
        return new_svg
    #end

    def combine(self, other_svg):
        new_svg = Svg(self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
        new_svg.set_view_box( self.__view_box )
        for layer in self.__layers:
            new_svg.append(layer.name, layer.path_data)
        #end
        for other_layer in other_svg:
            new_svg.append(other_layer.name, other_layer.path_data)
        #end
        return new_svg
    #end

    def get_single_layer_svg(self, target_layer_name):
        new_svg = Svg(self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
        new_svg.set_view_box( self.__view_box )
        for layer in self.__layers:
            if( layer.name == target_layer_name ):
                new_svg.append(layer.name, layer.path_data)
            #end
        #end
        return new_svg
    #end

    def printCurve(self):
        for layer in self.__layers:
            layer.path_data.printCurve()

        #end
    #end

#end

