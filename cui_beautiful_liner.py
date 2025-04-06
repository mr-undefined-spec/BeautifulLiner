from argparse import ArgumentParser

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'model/curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'model/layer'))
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from linear_approximate_curve import LinearApproximateCurve
from layer import Layer
from layer_set import LayerSet

sys.path.append(os.path.join(os.path.dirname(__file__), 'handler'))

from read_handler import ReadHandler
from linearize_handler import LinearizeHandler

from residual_calculate_handler import ResidualCalculateHandler
from optimize_handler import OptimizeHandler
from curve_orientation_handler import CurveOrientationHandler

from smoothen_handler import SmoothenHandler

from delete_edge_handler import DeleteEdgeHandler


sys.path.append(os.path.join(os.path.dirname(__file__), 'controller'))
from read_controller import ReadController
from linearize_controller import LinearizeController

from smoothen_controller import SmoothenController

from qtree_controller import QtreeController
from delete_edge_controller import DeleteEdgeController

from write_controller import WriteController

def print_layer_set(layer_set):
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
    read_layer_set = read_controller.process(args.reading_file_path)

    # initialize controllers
    total_curve_num = read_layer_set.get_total_curve_num()
    total_step_num = total_curve_num * 6
    linearize_controller = LinearizeController(total_step_num)
    smoothen_controller = SmoothenController(total_step_num)
    qtree_controller = QtreeController(total_step_num)
    delete_edge_controller = DeleteEdgeController(total_step_num)


    # once linearize
    linearize_controller.set_step_offset(0)
    first_linearize_layer_set = linearize_controller.process(read_layer_set, args.linear_approximate_length)

    #print_layer_set(first_linearize_layer_set)


    # once smoothen
    smoothen_controller.set_step_offset(total_curve_num*1)
    first_smooth_layer_set = smoothen_controller.process(first_linearize_layer_set, args.linear_approximate_length, args.eps_smooth_curve)

    # second linearize
    linearize_controller.set_step_offset(total_curve_num*2)
    second_linearize_layer_set = linearize_controller.process(first_smooth_layer_set, args.linear_approximate_length)

    #print_layer_set(second_linearize_layer_set)

    # create qtree
    qtree_controller.set_step_offset(total_curve_num*3)
    second_linearize_layer_set = qtree_controller.process(second_linearize_layer_set)


    # delete edge
    delete_edge_controller.set_step_offset(total_curve_num*4)
    delete_edge_layer_set = delete_edge_controller.process(second_linearize_layer_set, args.delete_ratio)

    # second smoothen
    smoothen_controller.set_step_offset(total_curve_num*5)
    second_smooth_layer_set = smoothen_controller.process(delete_edge_layer_set, args.linear_approximate_length, args.eps_smooth_curve)

    #print_layer_set(second_smooth_layer_set)

    output_file_name = args.reading_file_path.replace(".svg", "_BeauL.svg") 

    write_controller = WriteController()
    write_controller.process(second_smooth_layer_set, output_file_name)


    print("Create " + output_file_name )
    print("END OF JOB")
#end

if __name__ == '__main__':
    main()
#end
