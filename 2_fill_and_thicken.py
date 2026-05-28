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
from process.generator.thicken_generator import ThickenGenerator
from process.generator.junction_generator import JunctionGenerator

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

    # --- ステージ1：直線近似 ---
    linearize_pipeline.set_step_offset(0)
    canvas = linearize_pipeline.process(canvas)

    # --- ステージ2：端部カット ---
    delete_edge_pipeline.set_step_offset(1 * total_step_num)
    canvas = delete_edge_pipeline.process(canvas)

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

    # 🌟 2. トポロジーが残っている生データから三叉路ポリゴン（junction_canvas）を生成
    junction_canvas = JunctionGenerator.generate(canvas, triangle_size=20.0)

    # 🌟 3. 主線を強弱のある「面」にコンバート（thick_main_canvas）
    thick_main_canvas = ThickenGenerator.generate(canvas, base_max_width=broad_width)

    # 🌟 4. 【修正】統合はWriter側で行うので、ここではマージせず出力ファイル名を決定
    output_file_name = reading_file_path.replace(".svg", "_b.svg") 
    
    # 🌟 5. 【修正】改造したWriterの3引数（主線、三叉路、ラフ塗り）へ各キャンバスを渡して出力！
    # 重なり順（ラフ塗り ➡️ 主線 ➡️ 三叉路）はWriter側で自動制御されます。
    Writer.write_file(
        output_file_name, 
        thick_main_canvas,      # 主線（肉付け済）
        junction_canvas=junction_canvas#,  # 三叉路
        #fill_canvas=fill_canvas      # ラフ塗り（【復活】）
    )

    if mode == "CUI":
        print("{} % complete @ {}".format(100.0, "finalize"))
    #end

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
                            default=4.0,
                            help='Width size when broadening the curve')
    args = argparser.parse_args()

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