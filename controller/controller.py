import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../model'))
from point import Point
from control_point import CubicBezierCurveControlPoint
from control_point import LinearApproximateCurveControlPoint
from curve import CubicBezierCurve
from curve import LinearApproximateCurve
from layer import Layer

from svg import Svg

class Controller:
    def run(self, reading_file_path, linear_approximate_length, delete_ratio, broad_width):
        svg = Svg()
        svg.read(reading_file_path)
        
        once_linearized = svg.linearize(linear_approximate_length)
        once_smoothened = once_linearized.smoothen()
        once_smoothened.set_write_options(is_fill=False, color="#00FF00")
        
        linearized  = once_smoothened.linearize(linear_approximate_length)
        delete_edge = linearized.delete_edge(delete_ratio)
        broadened   = delete_edge.broaden(broad_width)
        smoothened  = broadened.smoothen()
        smoothened.set_write_options(is_fill=True, color="#FF0000")

        writing_file_path = reading_file_path.replace(".svg", "_BeauL.svg")
        
        final       = smoothened.combine(once_smoothened)
        final.write(writing_file_path)
    #end
#end



def main():
    usage = 'Usage: python {} FILE [-d|--delete_ratio <value>(default: 0.25)] [-l|--linear_approximate_length <value>(default: 1.0)] [-b|--broad_width <value>(default: 1.0)] [-n|--no_broad] [--help]'\
            .format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('fname', type=str,
                            help='echo fname')
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
    argparser.add_argument('-n', '--no_broad',
                            action='store_false',
                            help='Donot broaden path')
    args = argparser.parse_args()

    cubic_bezier_curve, view_box_data = readCubicBezierCurveFromSvgFile(args.fname)
    linear_approximate_curve = convertBezierToLinearApproximateCurve(cubic_bezier_curve, args.linear_approximate_length)
    once_iikanji_curve = finalizeSingleCubicBezierCurve(linear_approximate_curve)

    if( args.no_broad ):
        linear_approximate_curve = convertBezierToLinearApproximateCurve(once_iikanji_curve, args.linear_approximate_length)
        segment_space = makeSegmentSpace(linear_approximate_curve, view_box_data)
        all_layer_deleted_curves = deleteOverHangs(linear_approximate_curve, segment_space, args.delete_ratio)
        broad_curve = broadenLinearApproximateCurveSet(all_layer_deleted_curves, args.broad_width)


        final_curve = finalizeBroadCubicBezierCurve(broad_curve)
    else:
        final_curve = finalizeSingleCubicBezierCurve(linear_approximate_curve)
    #end if

    writeSvg(args.fname, final_curve)
    print("Create " + args.fname.replace(".svg", "_BeauL.svg") )
    print("END OF JOB")
    #print( all_layer_deleted_curves.to_svg_str() )
#end

if __name__ == '__main__':
    main()
#end
