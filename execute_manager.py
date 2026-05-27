from argparse import ArgumentParser

import os
import sys

from model.container.layer import Layer, EndpointStyle
from model.container.canvas import Canvas
from util.reader import Reader
#from util.writer import Writer

# debug function
def print_canvas(layer_set):
    template = r'<path stroke="#00ff00" stroke-width="1.5" fill="none" stroke-linecap="round" opacity="1" stroke-linejoin="round"'
    for layer in layer_set:
        for i, curve in enumerate(layer):
            s = ""
            s += template
            s += r' d="'
            s += curve.to_str()
            s += r'" />'
            print(s)
        #end
    #end
#end

class ExecuteManager:
    @staticmethod
    def execute(reading_file_path, linear_approximate_length, delete_ratio, broad_width, 
                mode="CUI", progress_bar=None, log_text=None):
        # pre-process   
        read_canvas = Reader.create_canvas_from_file(reading_file_path)
        #print_canvas(read_canvas)

        # initialize controllers
        total_curve_num = read_canvas.get_total_curve_num()
        total_step_num = total_curve_num * 7

        controllers = [
            # linearize_controller,
            # thin_smoothen_controller,
            # linearize_controller,
            # qtree_controller,
            #delete_edge_controller,
            #broaden_controller,
            #broad_smoothen_controller,
        ]

        canvas = read_canvas

        for i, controller in enumerate(controllers):
            controller.set_step_offset(i*total_curve_num)
            canvas = controller.process(canvas)
        #end

        new_canvas = Canvas()
        new_canvas.set_view_box(canvas.view_box)
        for layer in canvas:
            new_layer = layer
            #new_layer.set_write_options(True, layer.color, EndpointStyle.BOTH_POINTED)
            new_layer.set_write_options(False, layer.color, EndpointStyle.BOTH_POINTED)
            new_canvas.append(new_layer)
        #end

        if mode == "CUI":
            print("{} % complete @ {}".format(100.0, "finalize"))
        #end

        print_canvas(new_canvas)

        output_file_name = reading_file_path.replace(".svg", "_BeauL.svg") 
        # Writer.write_file(new_canvas, output_file_name)

        if mode == "CUI":
            print("Create " + output_file_name )
            print("END OF JOB")
        #end

    #end
#end
