#import numpy as np

#import os
#import sys
#sys.path.append(os.path.join(os.path.dirname(__file__), '../model/primitive'))

from basic_handler import BasicHandler

class WriteHandler(BasicHandler):

    @staticmethod
    def process(layer_set, output_file_name):
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


            for i, curve in enumerate(layer):
                if layer.is_fill:
                    s += '  <path stroke="none" stroke-width="1.0" fill="' + layer.color + '" stroke-linecap="round" opacity="1" stroke-linejoin="round" '
                else:
                    s += '  <path stroke="' + layer.color + '" stroke-width="1.0" fill="none" stroke-linecap="round" opacity="1" stroke-linejoin="round" '
                s += r' d="'
                s += curve.to_str()
                s += r'" />' + '\n'
            #end
            s += '</g>\n'
        #end
        s += '</svg>'
        with open(output_file_name, mode='w', encoding='utf-8') as f:
            f.write(s)
        #end
    #end

#end
