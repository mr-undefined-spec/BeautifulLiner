from argparse import ArgumentParser

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'controller'))
from read_controller import ReadController
from linearize_controller import LinearizeController
from smoothen_controller import SmoothenController
from qtree_controller import QtreeController
from delete_edge_controller import DeleteEdgeController
from broaden_controller import BroadenController
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
                            default="red",
                            help='Output line color')
    args = argparser.parse_args()


    # pre-process   
    read_controller = ReadController()
    read_canvas = read_controller.process(args.reading_file_path)
    #print_canvas(read_canvas)

    # initialize controllers
    total_curve_num = read_canvas.get_total_curve_num()
    total_step_num = total_curve_num * 6
    linearize_controller = LinearizeController(total_step_num)
    smoothen_controller = SmoothenController(total_step_num)
    qtree_controller = QtreeController(total_step_num)
    broaden_controller = BroadenController(total_step_num)
    delete_edge_controller = DeleteEdgeController(total_step_num)


    # once linearize
    linearize_controller.set_step_offset(0)
    first_linearize_canvas = linearize_controller.process(read_canvas, args.linear_approximate_length)
    #print_canvas(first_linearize_canvas)

    # once smoothen
    smoothen_controller.set_step_offset(total_curve_num*1)
    first_smooth_canvas = smoothen_controller.process(first_linearize_canvas, args.linear_approximate_length, args.eps_smooth_curve)
    #print_canvas(first_smooth_canvas)

    # second linearize
    linearize_controller.set_step_offset(total_curve_num*2)
    second_linearize_canvas = linearize_controller.process(first_smooth_canvas, args.linear_approximate_length)
    #print_canvas(second_linearize_canvas)

    # create qtree
    qtree_controller.set_step_offset(total_curve_num*3)
    second_linearize_canvas = qtree_controller.process(second_linearize_canvas)

    # delete edge
    delete_edge_controller.set_step_offset(total_curve_num*4)
    delete_edge_canvas = delete_edge_controller.process(second_linearize_canvas, args.delete_ratio)

    # broaden
    broaden_controller.set_step_offset(total_curve_num*5)
    broad_canvas = broaden_controller.process(delete_edge_canvas, args.broad_width)
    print_canvas(broad_canvas)

    # second smoothen
    #smoothen_controller.set_step_offset(total_curve_num*6)
    #second_smooth_canvas = smoothen_controller.process(broad_canvas, args.linear_approximate_length, args.eps_smooth_curve)
    #print_canvas(second_smooth_canvas)

    output_file_name = args.reading_file_path.replace(".svg", "_BeauL.svg") 

    write_controller = WriteController()
    write_controller.process(broad_canvas, output_file_name)
    print("Create " + output_file_name )
    print("END OF JOB")
#end

if __name__ == '__main__':
    main()
#end
