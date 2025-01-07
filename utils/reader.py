


from xml.dom import minidom

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../model/curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../model/compose'))

from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from cubic_bezier_curve import CubicBezierCurve
from layer import Layer

from layer_set import LayerSet

import tkinter as tk

import re

def _split_to_xy(point_str):
    s2 = point_str.replace("-", " -")
    tmp_items = re.split(r'\s+|\+', s2)
    return list( filter(None, tmp_items) )
#end def

# IN  nodeValue of d in path of layer_set as string
# OUT CubicBezierCurve
def _make_cubic_bezier_curve_set(d_str):
    curve = CubicBezierCurve()

    point_strs = re.split("[C|L|M|Z]", d_str)
    point_strs.pop(0)
    # exception handling for 1st point
    items = _split_to_xy( point_strs[0].strip() )
    last_point = Point( float(items[0]), float(items[1]) )
    point_strs.pop(0)

    for point_str in point_strs:
        if point_str.strip() == "":
            break
        #end
        items = _split_to_xy( point_str.strip() )
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

def _make_layer(layer_name, paths):
    layer = Layer(layer_name)
    for path in paths:
        layer.append(  _make_cubic_bezier_curve_set( path.getAttributeNode('d').nodeValue )  )
    #end for
    return layer
#end

def _get_group_paths_tuple(doc):
    return_tuple = []
    for group in doc.getElementsByTagName("g"):
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

def create_layer_set_from_file(file_name, global_calc_step, mode, progress_bar=None, log_text=None):
    layer_set = LayerSet(global_calc_step, mode, progress_bar, log_text)

    if not type(file_name) is str:
        raise ValueError("file_name must be str")
    #end

    doc = minidom.parse(file_name)
    layer_set.set_doc(doc)

    for group_paths_set in _get_group_paths_tuple(doc):
        group = group_paths_set[0]
        paths = group_paths_set[1]
        layer_name = group.getAttributeNode('id').nodeValue

        layer_set.append(_make_layer(layer_name, paths) )
    #end
    root = doc.getElementsByTagName("svg")
    layer_set.set_view_box( root[0].attributes["viewBox"].value )

    return layer_set
#end


