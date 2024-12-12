
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

from svg import Svg

import tkinter as tk

import re

def write(svg, path):
    bbox = svg.get_bbox()
    s = ""
    s += '<?xml version="1.0" encoding="UTF-8"?>\n'
    s += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
    s += '<!-- Created with Inkpad (http://www.taptrix.com/) -->\n'
    s += '<svg xmlns:inkpad="http://taptrix.com/inkpad/svg_extensions" '
    s += 'height="' + str(bbox[3]) + 'pt" '
    s += 'xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" '
    s += 'width="' + str(bbox[2]) + 'pt" version="1.1" '
    s += ' viewBox="' + svg.view_box + '" '
    s += '>\n'


    for layer in svg:
        #s += '<g id="' + layer.name + '" vectornator:layerName="' + layer.name + '">\n'
        s += '<g id="' + layer.name + '" inkpad:layerName="' + layer.name + '">\n'
        s += layer.to_svg2()
#            s += layer.path_data.to_svg()
        s += '</g>\n'
    #end
    s += '</svg>'
    with open(path, mode='w', encoding='utf-8') as f:
        f.write(s)
    #end
#end def
