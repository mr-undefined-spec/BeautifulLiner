from argparse import ArgumentParser

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'model/layer'))
from layer import Layer
from layer import EndpointStyle
from canvas import Canvas


sys.path.append(os.path.join(os.path.dirname(__file__), 'controller'))
from read_controller import ReadController
from linearize_controller import LinearizeController
from thin_smoothen_controller import ThinSmoothenController
from qtree_controller import QtreeController
from delete_edge_controller import DeleteEdgeController
from broaden_controller import BroadenController
from broad_smoothen_controller import BroadSmoothenController
from write_controller import WriteController

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

def main():
    usage = 'Usage: python {} FILE [-C|--continuous_ratio <value>(default: 0.25)] [-d|--delete_ratio <value>(default: 0.25)] [-l|--linear_approximate_length <value>(default: 1.0)] [-b|--broad_width <value>(default: 1.0)] [-n|--no_broad] [--help]'\
            .format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('reading_file_path', type=str,
                            help='Reading svg file path.')
    argparser.add_argument('-C', '--continuous_ratio',
                            type=float,
                            dest='continuous_ratio',
                            default=2.0,
                            help='Ratio of both end areas to check continuous curve')
    argparser.add_argument('-e', '--eps_smooth_curve',
                            type=float,
                            dest='eps_smooth_curve',
                            default=1.0,
                            help='Convergence condition for smooth approximate curve')
    argparser.add_argument('-d', '--delete_ratio',
                            type=float,
                            dest='delete_ratio',
                            default=0.25,
                            help='Ratio of both end areas to delete overhangs in the curve')
    argparser.add_argument('-l', '--linear_approximate_length',
                            type=float,
                            dest='linear_approximate_length',
                            default=1.0,
                            help='Length of the small segment when linearly approximating')
    argparser.add_argument('-b', '--broad_width',
                            type=float,
                            dest='broad_width',
                            default=1.0,
                            help='Width size when broadening the curve')
    argparser.add_argument('-c', '--color',
                            type=str,
                            dest='output_color',
                            default="black",
                            help='Output line color')
    args = argparser.parse_args()


    # pre-process   
    read_controller = ReadController()
    read_canvas = read_controller.process(args.reading_file_path)
    #print_canvas(read_canvas)

    # initialize controllers
    total_curve_num = read_canvas.get_total_curve_num()
    total_step_num = total_curve_num * 8

    linearize_controller = LinearizeController()
    linearize_controller.set_total_step_num(total_step_num)
    linearize_controller.set_linear_approximate_length(args.linear_approximate_length)

    thin_smoothen_controller = ThinSmoothenController()
    thin_smoothen_controller.set_total_step_num(total_step_num)
    
    qtree_controller = QtreeController()
    qtree_controller.set_total_step_num(total_step_num)

    delete_edge_controller = DeleteEdgeController()
    delete_edge_controller.set_total_step_num(total_step_num)
    delete_edge_controller.set_delete_ratio(args.delete_ratio)

    broaden_controller = BroadenController()
    broaden_controller.set_total_step_num(total_step_num)
    broaden_controller.set_broad_width(args.broad_width)

    broad_smoothen_controller = BroadSmoothenController()
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

    output_file_name = args.reading_file_path.replace(".svg", "_BeauL.svg") 

    write_controller = WriteController()
    write_controller.process(new_canvas, output_file_name)
    print("Create " + output_file_name )
    print("END OF JOB")
#end

if __name__ == '__main__':
    main()
#end
