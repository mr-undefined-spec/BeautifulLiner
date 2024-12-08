import os
import sys

global calc_step
calc_step = 0
global total_calc_step

sys.path.append(os.path.join(os.path.dirname(__file__), 'model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'model/curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'model/compose'))

from argparse import ArgumentParser

from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from cubic_bezier_curve import CubicBezierCurve
from linear_approximate_curve import LinearApproximateCurve
from layer import Layer

from svg import Svg

def get_special_smoothened_for_hair(single_layer_svg, linear_approximate_length, delete_ratio, broad_width, color):
    once_linearized = single_layer_svg.linearize(linear_approximate_length)
    once_smoothened = once_linearized.thin_smoothen()
    
    linearized  = once_smoothened.linearize(linear_approximate_length)

    linearized.create_intersect_judge_rectangle()
    linearized.create_sequential_points_and_edge_sequential_points()
    linearized.create_continuous_curve_index_group(1.0)
    linearized.create_connection_point()

    delete_edge = linearized.delete_edge(delete_ratio)
    broadened   = delete_edge.broaden(broad_width)
    smoothened  = broadened.broad_smoothen()
    smoothened.set_write_options(is_fill=True, color=color)

    return smoothened
#end

def get_smoothened(single_layer_svg, linear_approximate_length, delete_ratio, broad_width, color):
    once_linearized = single_layer_svg.linearize(linear_approximate_length)
    once_smoothened = once_linearized.thin_smoothen()
    
    linearized  = once_smoothened.linearize(linear_approximate_length)

    linearized.create_intersect_judge_rectangle()
    linearized.create_sequential_points_and_edge_sequential_points()
    linearized.create_continuous_curve_index_group(1.0)
    linearized.create_connection_point()

    delete_edge = linearized.delete_edge(delete_ratio)
    broadened   = delete_edge.broaden(broad_width)
    smoothened  = broadened.broad_smoothen()
    smoothened.set_write_options(is_fill=True, color=color)

    return smoothened
#end


def custom_run(mode, reading_file_path, linear_approximate_length, delete_ratio, broad_width, output_color, progress_bar=None, log_text=None):
    svg = Svg(0, mode, progress_bar, log_text)
    svg.read(reading_file_path)

    hair_smoothened = get_smoothened( svg.get_single_layer_svg("Hair"), linear_approximate_length, delete_ratio, broad_width, "#ff0000" )
    body_smoothened = get_smoothened( svg.get_single_layer_svg("Body"), linear_approximate_length, delete_ratio, broad_width, "#00ff00" )
    cloth_smoothened = get_smoothened( svg.get_single_layer_svg("Cloth"), linear_approximate_length, delete_ratio, broad_width, "#0000ff" )
    others_smoothened = get_smoothened( svg.get_single_layer_svg("Hand"), linear_approximate_length, delete_ratio, broad_width, "#0000ff" )
#    detail_smoothened = get_smoothenend( svg.get_single_layer_svg("Detail"), linear_approximate_length, broad_width )

    writing_file_path = reading_file_path.replace(".svg", "_BeauL.svg")
    final = hair_smoothened.combine(body_smoothened).combine(cloth_smoothened).combine(others_smoothened)
    final.write(writing_file_path)
#end

def main():
    usage = 'Usage: python {} FILE [-d|--delete_ratio <value>(default: 0.25)] [-l|--linear_approximate_length <value>(default: 1.0)] [-b|--broad_width <value>(default: 1.0)] [-n|--no_broad] [--help]'\
            .format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('reading_file_path', type=str,
                            help='Reading svg file path.')
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

    custom_run("CUI", args.reading_file_path, args.linear_approximate_length, args.delete_ratio, args.broad_width, args.output_color)
    print("Create " + args.reading_file_path.replace(".svg", "_BeauL.svg") )
    print("END OF JOB")
#end

if __name__ == '__main__':
    main()
#end
