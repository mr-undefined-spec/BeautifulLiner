
from xml.dom import minidom

from point import Point
from control_point import CubicBezierCurveControlPoint
from curve import CubicBezierCurve
from layer import Layer

import re
class LayerData:
    def __init__(self, name, path_data):
        self.name = name
        self.path_data = path_data
    #end
#end

class Svg:
    def __init__(self):
        self.__layers = []
    #end

    def read(self, file_name):
        if not type(file_name) is str:
            raise ValueError("file_name must be str")
        self.__doc = minidom.parse(file_name)

        for group_paths_set in self.get_group_paths_tuple():
            group = group_paths_set[0]
            paths = group_paths_set[1]
            layer_name = group.getAttributeNode('id').nodeValue
    
            if re.match("xxx", layer_name):
                print("skip layer {}".format(layer_name))
                continue
            #end if
            print("read layer {}".format(layer_name))
            self.append(layer_name, self.make_layer(paths) )
        #end for group_paths_set
    #end

    def split_to_xy(self, point_str):
        s2 = point_str.replace("-", " -")
        tmp_items = re.split(r'\s+', s2)
        return tmp_items
    #end def
    
    # IN  nodeValue of d in path of svg as string
    # OUT CubicBezierCurve
    def make_cubic_bezier_curve_set(self, d_str):
        curve = CubicBezierCurve()
    
        point_strs = re.split("[C|L|M|Z]", d_str)
        point_strs.pop(0)
        # exception handling for 1st point
        items = self.split_to_xy( point_strs[0].strip() )
        last_point = Point( float(items[0]), float(items[1]) )
        point_strs.pop(0)
    
        for point_str in point_strs:
            items = self.split_to_xy( point_str.strip() )
            #print(items)
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

    def make_layer(self, paths):
        layer = Layer()
        for path in paths:
            layer.append(  self.make_cubic_bezier_curve_set( path.getAttributeNode('d').nodeValue )  )
        #end for
        return layer
    #end

    def get_group_paths_tuple(self):
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

    def viewBoxString(self):
        root = self.__doc.getElementsByTagName("svg")
        return root[0].attributes["viewBox"].value
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
#end

