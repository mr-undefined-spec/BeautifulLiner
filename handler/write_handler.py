


from xml.dom import minidom

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../model/curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../model/layer'))

from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from cubic_bezier_curve import CubicBezierCurve

from layer import Layer
from layer_set import LayerSet

from basic_handler import BasicHandler

class WriteHandler(BasicHandler):

    @classmethod
    def write(cls, layer_set, output_file_name):
        bbox = layer_set.get_bbox()
        s = ""
        s += '<?xml version="1.0" encoding="UTF-8"?>\n'
        s += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
        s += '<!-- Created with Inkpad (http://www.taptrix.com/) -->\n'
        s += '<svg xmlns:inkpad="http://taptrix.com/inkpad/svg_extensions" '
        s += 'height="' + str(bbox[3]) + 'pt" '
        s += 'xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" '
        s += 'width="' + str(bbox[2]) + 'pt" version="1.1" '
        s += ' viewBox="' + layer_set.view_box + '" '
        s += '>\n'


        for layer in layer_set:
            #s += '<g id="' + layer.name + '" vectornator:layerName="' + layer.name + '">\n'
            s += '<g id="' + layer.name + '" inkpad:layerName="' + layer.name + '">\n'
            s += '<path stroke="#00fb00" stroke-width="2.01172" fill="none" stroke-linecap="round" opacity="1" stroke-linejoin="round" d="'
            for i, curve in enumerate(layer):
                for j, ctrl_p in enumerate(curve):
                    if i==0:
                        s += "M " + str(ctrl_p.start) + " "
                    #end
                    s += "L " + str(ctrl_p.end) + " "
                #end
            #end
            s += '"/>\n'
            s += '</g>\n'
        #end
        s += '</svg>'
        with open(output_file_name, mode='w', encoding='utf-8') as f:
            f.write(s)
        #end
    #end

#end
