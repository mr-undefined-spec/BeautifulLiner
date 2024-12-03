
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
    # private
    #
    def __split_to_xy(self, point_str):
        s2 = point_str.replace("-", " -")
        tmp_items = re.split(r'\s+|\+', s2)
        return list( filter(None, tmp_items) )
    #end def
    
    # IN  nodeValue of d in path of svg as string
    # OUT CubicBezierCurve
    def __make_cubic_bezier_curve_set(self, d_str):
        curve = CubicBezierCurve()
    
        point_strs = re.split("[C|L|M|Z]", d_str)
        point_strs.pop(0)
        # exception handling for 1st point
        items = self.__split_to_xy( point_strs[0].strip() )
        last_point = Point( float(items[0]), float(items[1]) )
        point_strs.pop(0)
    
        for point_str in point_strs:
            items = self.__split_to_xy( point_str.strip() )
            if len(items)==2:
                p3 = Point( float(items[0]), float(items[1]) )
                x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0
                if (last_point.x < p3.x):
                    x1 = (last_point.x*2.0 + p3.x*1.0)/3.0
                    x2 = (last_point.x*1.0 + p3.x*2.0)/3.0
                else:
                    x1 = (last_point.x*1.0 + p3.x*2.0)/3.0
                    x2 = (last_point.x*2.0 + p3.x*1.0)/3.0
                #end if
                if (last_point.y < p3.y):
                    y1 = (last_point.y*2.0 + p3.y*1.0)/3.0
                    y2 = (last_point.y*1.0 + p3.y*2.0)/3.0
                else:
                    y1 = (last_point.y*1.0 + p3.y*2.0)/3.0
                    y2 = (last_point.y*2.0 + p3.y*1.0)/3.0
                #end if
                p1 = Point(x1, y1)
                p2 = Point(x2, y2)
            elif len(items)==6:
                p1 = Point( float(items[0]), float(items[1]) )
                p2 = Point( float(items[2]), float(items[3]) )
                p3 = Point( float(items[4]), float(items[5]) )
            #end if
            curve.append( CubicBezierCurveControlPoint(last_point, p1, p2, p3) )
            last_point = p3
        #end for
    
        return curve
    #end def

    def __make_layer(self, paths):
        layer = Layer()
        for path in paths:
            layer.append(  self.__make_cubic_bezier_curve_set( path.getAttributeNode('d').nodeValue )  )
            self.__total_path_num += 1
        #end for
        return layer
    #end

    def __get_group_paths_tuple(self):
        return_tuple = []
        for group in self.__doc.getElementsByTagName("g"):
            the_tuple = []
            the_tuple.append(group)

            the_paths = []
            for path in group.getElementsByTagName("path"):
                the_paths.append(path)
            #end for
            the_tuple.append(the_paths)

            return_tuple.append(the_tuple)
        #end for
        return tuple(return_tuple)
    #end

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
    #end

    def read(self, file_name):
        if not type(file_name) is str:
            raise ValueError("file_name must be str")
        self.__doc = minidom.parse(file_name)

        for group_paths_set in self.__get_group_paths_tuple():
            group = group_paths_set[0]
            paths = group_paths_set[1]
            layer_name = group.getAttributeNode('id').nodeValue

            self.append(layer_name, self.__make_layer(paths) )
        #end
        root = self.__doc.getElementsByTagName("svg")
        self.__view_box = root[0].attributes["viewBox"].value
    #end


    def set_view_box(self, val):
        self.__view_box = val
    #end

    def get_bbox(self):
        arr = self.__view_box.split(",")
        return ( float(arr[0]), float(arr[1]), float(arr[2]), float(arr[3]) )
    #end

    @property
    def doc(self):
        return self.__doc
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

    def write(self, path):
        bbox = self.get_bbox()
        s = ""
        s += '<?xml version="1.0" encoding="UTF-8"?>\n'
        s += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
        s += '<!-- Created with Inkpad (http://www.taptrix.com/) -->\n'
        s += '<svg xmlns:inkpad="http://taptrix.com/inkpad/svg_extensions" '
        s += 'height="' + str(bbox[3]) + 'pt" '
        s += 'xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" '
        s += 'width="' + str(bbox[2]) + 'pt" version="1.1" '
        s += ' viewBox="' + self.__view_box + '" '
        s += '>\n'

        for layer in self.__layers:
            #s += '<g id="' + layer.name + '" vectornator:layerName="' + layer.name + '">\n'
            s += '<g id="' + layer.name + '" inkpad:layerName="' + layer.name + '">\n'
            s += layer.path_data.to_svg()
            s += '</g>\n'
        #end
        s += '</svg>'
        with open(path, mode='w', encoding='utf-8') as f:
            f.write(s)
        #end
    #end def

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

    def create_continuous_curve_index_group(self, distance_threshold):
        
        self.__global_calc_step += 1
        new_svg = Svg(self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
        new_svg.set_view_box( self.__view_box )
        bbox = self.get_bbox()
        for layer in self.__layers:
            layer.path_data.create_continuous_curve_index_group( distance_threshold, self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
        #end
    #end

    def delete_edge(self, ratio):
        self.__global_calc_step += 1
        new_svg = Svg(self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
        new_svg.set_view_box( self.__view_box )
        bbox = self.get_bbox()
        for layer in self.__layers:
            new_layer = layer.path_data.delete_edge(bbox, ratio, self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
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
            new_layer = layer.path_data.broaden(broaden_width, self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
            new_svg.append("B_" + layer.name, new_layer)
        #end
        return new_svg
    #end

    def broad_smoothen(self):
        self.__global_calc_step += 1
        new_svg = Svg(self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text)
        new_svg.set_view_box( self.__view_box )
        for layer in self.__layers:
            new_svg.append(layer.name, layer.path_data.broad_smoothen(self.__global_calc_step, self.__mode, self.__progress_bar, self.__log_text) )
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

#end

