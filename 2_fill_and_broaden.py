from argparse import ArgumentParser

import os
import sys
from PIL import Image

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
            image_path=None, mode="CUI", progress_bar=None, log_text=None):
    # pre-process   
    read_canvas = Reader.create_canvas_from_file(reading_file_path)

    # initialize pipelines
    total_curve_num = read_canvas.get_total_curve_num()
    total_step_num = total_curve_num * 7

    linearize_pipeline = CanvasPipeline("linearize", LinearizeConverter())
    delete_edge_pipeline = DeleteEdgePipeline("delete_edge", delete_ratio)

    canvas = read_canvas

    # --- ステージ1相当：直線近似 ---
    linearize_pipeline.set_step_offset(0)
    canvas = linearize_pipeline.process(canvas)

    # 🌟 参照画像が指定されていればPILで開く
    ref_image = None
    if image_path and os.path.exists(image_path):
        if mode == "CUI":
            print(f"Loading reference image: {image_path}")
        #end if
        ref_image = Image.open(image_path)
    #end if

    # 🌟 綺麗にカットされた最新の canvas と、読み込んだ画像を渡してラフ塗りを生成
    fill_canvas = RoughFillGenerator.generate(canvas, reference_image=ref_image)

    # --- ステージ2相当：端部カット ---
    delete_edge_pipeline.set_step_offset(1 * total_step_num)
    canvas = delete_edge_pipeline.process(canvas)


    new_canvas = Canvas()
    new_canvas.set_view_box(canvas.view_box)
    for layer in canvas:
        new_layer = layer
        new_layer.set_write_options(False, layer.color, EndpointStyle.BOTH_POINTED)
        new_canvas.append(new_layer)
    #end

    if mode == "CUI":
        print("{} % complete @ {}".format(100.0, "finalize"))
    #end

    output_file_name = reading_file_path.replace(".svg", "_b.svg") 
    Writer.write_file(output_file_name, new_canvas, fill_canvas)

    if mode == "CUI":
        print("Create " + output_file_name )
        print("END OF JOB")
    #end

#end


def main():
    usage = 'Usage: python {} FILE [-i|--image <path>] [-C|--continuous_ratio <value>] [-d|--delete_ratio <value>] [-l|--linear_approximate_length <value>] [-b|--broad_width <value>] [--help]'\
            .format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('reading_file_path', type=str,
                            help='Reading svg file path.')
    
    # 🌟 カラー参照画像パス用のオプション引数を追加
    argparser.add_argument('-i', '--image',
                            type=str,
                            dest='image_path',
                            default=None,
                            help='Path to the reference color image for rough filling.')

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

    # executeへ image_path をフォワード
    execute(
        args.reading_file_path, 
        args.linear_approximate_length, 
        args.delete_ratio, 
        args.broad_width,
        image_path=args.image_path
    )

#end

if __name__ == '__main__':
    main()
#end