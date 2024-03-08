import os
import sys

global calc_step
calc_step = 0
global total_calc_step

sys.path.append(os.path.join(os.path.dirname(__file__), 'model'))

from argparse import ArgumentParser

from point import Point
from control_point import CubicBezierCurveControlPoint
from control_point import LinearApproximateCurveControlPoint
from curve import CubicBezierCurve
from curve import LinearApproximateCurve
from layer import Layer

from svg import Svg
def custom_run(mode, reading_file_path, linear_approximate_length, delete_ratio, broad_width, output_color, progress_bar=None, log_text=None):
    svg = Svg(0, mode, progress_bar, log_text)
    svg.read(reading_file_path)

    kage_svg = svg.get_single_layer_svg("Kage")
    kage_once_linearized = kage_svg.linearize(linear_approximate_length)
    kage_once_smoothened = kage_once_linearized.smoothen()
    kage_once_smoothened.set_write_options(is_fill=False, color="#0000ff")

    senga_svg = svg.get_single_layer_svg("Senga")
    once_linearized = senga_svg.linearize(linear_approximate_length)
    once_smoothened = once_linearized.smoothen()
    once_smoothened.set_write_options(is_fill=False, color="#00ff00")
    
    linearized  = once_smoothened.linearize(linear_approximate_length)
    delete_edge = linearized.delete_edge(delete_ratio)
    broadened   = delete_edge.broaden(broad_width)
    smoothened  = broadened.smoothen()
    smoothened.set_write_options(is_fill=True, color="#ff0000")

    writing_file_path = reading_file_path.replace(".svg", "_BeauL.svg")
    final = svg.combine(smoothened).combine(kage_once_smoothened).combine(once_smoothened)
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
