import os
import sys

global calc_step
calc_step = 0
global total_calc_step

sys.path.append(os.path.join(os.path.dirname(__file__), 'model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'model/curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'model/compose'))

sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from argparse import ArgumentParser

from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from cubic_bezier_curve import CubicBezierCurve
from linear_approximate_curve import LinearApproximateCurve
from layer import Layer
from layer import EndpointStyle

from layer_set import LayerSet

import reader
import writer

from events import Events
from logger import Logger

def get_smoothened(
    single_layer, 
    linear_approximate_length, 
    continuous_ratio, 
    delete_ratio, 
    broad_width, 
    color,
    endpoint_style
    ):

    once_linearized = single_layer.linearize(linear_approximate_length)
    once_smoothened = once_linearized.thin_smoothen()
    
    linearized  = once_smoothened.linearize(linear_approximate_length)

    linearized.create_continuous_curve_index_group(2.0)
    delete_edge = linearized.delete_edge(delete_ratio)
    broadened   = delete_edge.broaden(broad_width)
    smoothened  = broadened.broad_smoothen()
    smoothened.set_write_options(is_fill=True, color=color, endpoint_style=endpoint_style)

    return smoothened  
#end


def custom_run(mode, reading_file_path, linear_approximate_length, continuous_ratio, delete_ratio, broad_width, output_color, progress_bar=None, log_text=None):
    layer_set = reader.create_layer_set_from_file(reading_file_path, 0, mode)

    body = get_smoothened( layer_set.get_single_layer_as_layer_set("Body"), 
        linear_approximate_length, 
        continuous_ratio, 
        delete_ratio, 
        broad_width, 
        "#00ff00",
        EndpointStyle.BOTH_WIDE
        )
    hair = get_smoothened( layer_set.get_single_layer_as_layer_set("Hair"), 
        linear_approximate_length, 
        continuous_ratio, 
        delete_ratio, 
        broad_width, 
        "#ff0000",
        EndpointStyle.BOTH_POINTED
        )
    cloth = get_smoothened( layer_set.get_single_layer_as_layer_set("Cloth"), 
        linear_approximate_length, 
        continuous_ratio, 
        delete_ratio, 
        broad_width, 
        "#0000ff",
        EndpointStyle.BOTH_WIDE
        )

    writing_file_path = reading_file_path.replace(".svg", "_BeauL.svg")
    final = body.combine(hair).combine(cloth)
    writer.write(final, writing_file_path)
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
                            default=0.1,
                            help='Ratio of both end areas to check continuous curve')
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

    #events = Events()

    #logger = Logger(mode="CUI")

    #events.on("print_step", logger.log)

    custom_run("CUI", args.reading_file_path, args.linear_approximate_length, args.continuous_ratio, args.delete_ratio, args.broad_width, args.output_color)
    print("Create " + args.reading_file_path.replace(".svg", "_BeauL.svg") )
    print("END OF JOB")
#end

if __name__ == '__main__':
    main()
#end
