from argparse import ArgumentParser

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'model/layer'))
from layer import Layer
from layer import EndpointStyle
from canvas import Canvas


sys.path.append(os.path.join(os.path.dirname(__file__), 'controller'))
from linearize_controller import LinearizeController
from thin_smoothen_controller import ThinSmoothenController
from qtree_controller import QtreeController
from delete_edge_controller import DeleteEdgeController
from broaden_controller import BroadenController
from broad_smoothen_controller import BroadSmoothenController

sys.path.append(os.path.join(os.path.dirname(__file__), 'util'))
from reader import Reader
from writer import Writer

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

        linearize_controller = LinearizeController(mode, progress_bar, log_text)
        linearize_controller.set_total_step_num(total_step_num)
        linearize_controller.set_linear_approximate_length(linear_approximate_length)

        thin_smoothen_controller = ThinSmoothenController(mode, progress_bar, log_text)
        thin_smoothen_controller.set_total_step_num(total_step_num)
        
        qtree_controller = QtreeController(mode, progress_bar, log_text)
        qtree_controller.set_total_step_num(total_step_num)

        delete_edge_controller = DeleteEdgeController(mode, progress_bar, log_text)
        delete_edge_controller.set_total_step_num(total_step_num)
        delete_edge_controller.set_delete_ratio(delete_ratio)

        broaden_controller = BroadenController(mode, progress_bar, log_text)
        broaden_controller.set_total_step_num(total_step_num)
        broaden_controller.set_broad_width(broad_width)

        broad_smoothen_controller = BroadSmoothenController(mode, progress_bar, log_text)
        broad_smoothen_controller.set_total_step_num(total_step_num)

        controllers = [
            linearize_controller,
            thin_smoothen_controller,
            linearize_controller,
            qtree_controller,
            delete_edge_controller,
            broaden_controller,
            broad_smoothen_controller,
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
            new_layer.set_write_options(True, layer.color, EndpointStyle.BOTH_POINTED)
            new_canvas.append(new_layer)
        #end

        if mode == "CUI":
            print("{} % complete @ {}".format(100.0, "finalize"))
        #end

        output_file_name = reading_file_path.replace(".svg", "_BeauL.svg") 
        Writer.write_file(new_canvas, output_file_name)

        if mode == "CUI":
            print("Create " + output_file_name )
            print("END OF JOB")
        #end

    #end
#end
