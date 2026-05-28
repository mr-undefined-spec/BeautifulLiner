from argparse import ArgumentParser

import os
import sys

from model.container.layer import Layer, EndpointStyle
from model.container.canvas import Canvas

from process.pipeline.canvas_pipeline import CanvasPipeline
from process.pipeline.delete_edge_pipeline import DeleteEdgePipeline

from process.converter.linearize_converter import LinearizeConverter 
from process.converter.smoothen_converter import SmoothenConverter
from process.generator.rough_fill_generator import RoughFillGenerator

from util.reader import Reader
from util.writer import Writer




def execute(reading_file_path, linear_approximate_length, delete_ratio, broad_width, 
            mode="CUI", progress_bar=None, log_text=None):
    # pre-process   
    read_canvas = Reader.create_canvas_from_file(reading_file_path)
    #print_canvas(read_canvas)

    # initialize pipelines
    total_curve_num = read_canvas.get_total_curve_num()
    total_step_num = total_curve_num * 7

    thin_smoothen_pipeline = CanvasPipeline("smoothen", SmoothenConverter())

    canvas = read_canvas

    thin_smoothen_pipeline.set_step_offset(0)
    canvas = thin_smoothen_pipeline.process(canvas)

    output_file_name = reading_file_path.replace(".svg", "_a.svg") 
    Writer.write_file(output_file_name, canvas)

    if mode == "CUI":
        print("Create " + output_file_name )
        print("END OF JOB")
    #end

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
    args = argparser.parse_args()

    execute(args.reading_file_path, args.linear_approximate_length, args.delete_ratio, args.broad_width)

#end

if __name__ == '__main__':
    main()
#end

