from shapely.geometry import LineString, MultiLineString, box
from shapely.ops import unary_union, polygonize
from PIL import Image, ImageDraw
from collections import Counter

from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from model.container.layer import Layer
from model.container.canvas import Canvas


class RoughFillGenerator:
    IS_DEBUG = False

    @staticmethod
    def generate(stroke_canvas: Canvas, reference_image: Image.Image = None) -> Canvas:
        """
        キャンバス全体を取り囲む矩形（外枠）を追加し、全レイヤーの曲線と統合して閉領域を抽出。
        引数に reference_image (PIL Image) が与えられた場合、領域内で最も多く使われている色で塗りつぶす。
        与えられない場合は、従来どおり色指定なし（Writer側でランダム着色）として生成する。
        
        :param stroke_canvas: 線画データが格納されたCanvas
        :param reference_image: カラー参照用のPIL Imageオブジェクト（オプショナル）
        """
        fill_canvas = Canvas()
        fill_canvas.set_view_box(stroke_canvas.view_box)

        if RoughFillGenerator.IS_DEBUG:
            print("\n--- [RoughFillGenerator] Start Generation (Global Outer Boundary Mode) ---")
        #end if

        # 1. view_box からキャンバス全体を囲む外枠の線分（矩形）を生成
        try:
            if isinstance(stroke_canvas.view_box, str):
                vb = [float(x) for x in stroke_canvas.view_box.split()]
                minx, miny, maxx, maxy = vb[0], vb[1], vb[0] + vb[2], vb[1] + vb[3]
            else:
                bbox = stroke_canvas.get_bbox()
                minx, miny, maxx, maxy = 0.0, 0.0, bbox[2], bbox[3]
            #end if
        except Exception:
            bbox = stroke_canvas.get_bbox()
            minx, miny, maxx, maxy = 0.0, 0.0, bbox[2], bbox[3]
        #end try

        outer_box = box(minx, miny, maxx, maxy)
        outer_boundary_line = LineString(outer_box.exterior.coords)

        all_lines = [outer_boundary_line]
        total_input_curves = 0

        # 2. 全レイヤーのすべてのCurveからLineStringを抽出して追加
        for stroke_layer in stroke_canvas:
            total_input_curves += len(stroke_layer)
            for curve in stroke_layer:
                if len(curve.points) < 2:
                    continue
                #end if
                line = LineString([(p.x, p.y) for p in curve.points])
                all_lines.append(line)
            #end for
        #end for

        fill_layer = Layer("rough_fill", "#000000")

        # 3. 外枠＋全線分をまとめて交差点で分解し、閉じた面（Polygon）を自動抽出
        intersected_lines = unary_union(all_lines)
        polygons = list(polygonize(intersected_lines))
        
        if RoughFillGenerator.IS_DEBUG:
            print(f"  - Total extracted polygons: {len(polygons)}")
        #end if

        # カラー参照画像が存在する場合、RGBモードに変換してピクセルアクセスを高速化
        img_rgb = None
        if reference_image is not None:
            img_rgb = reference_image.convert("RGB")
        #end if

        # 4. 抽出されたすべてのPolygon群を、Curveオブジェクトにパック
        for idx, poly in enumerate(polygons):
            coords = list(poly.exterior.coords)
            points = [Point(c[0], c[1]) for c in coords]
            
            # デフォルトは色指定なし（None）
            sampled_color_str = None

            # 画像から最頻色をサンプリングするロジック
            if img_rgb is not None and poly.area > 0:
                # ポリゴンの外接矩形を取得して画像範囲内にクリップ（高速化のため）
                p_minx, p_miny, p_maxx, p_maxy = poly.bounds
                ix_min = max(0, int(p_minx))
                iy_min = max(0, int(p_miny))
                ix_max = min(img_rgb.width - 1, int(p_maxx))
                iy_max = min(img_rgb.height - 1, int(p_maxy))

                if ix_max >= ix_min and iy_max >= iy_min:
                    # ポリゴンのローカルマスク画像を生成
                    w = ix_max - ix_min + 1
                    h = iy_max - iy_min + 1
                    mask = Image.new("L", (w, h), 0)
                    draw = ImageDraw.Draw(mask)
                    
                    # ローカル座標系に変換してポリゴンを描画（塗りつぶし）
                    local_coords = [(c[0] - ix_min, c[1] - iy_min) for c in coords]
                    draw.polygon(local_coords, fill=255)

                    # マスク内部のピクセルの色を集計
                    pixels_in_poly = []
                    for dy in range(h):
                        for dx in range(w):
                            if mask.getpixel((dx, dy)) == 255:
                                px = img_rgb.getpixel((ix_min + dx, iy_min + dy))
                                pixels_in_poly.append(px)
                            #end if
                        #end for
                    #end for

                    # 最も頻出する（多く含まれる）色を決定
                    if pixels_in_poly:
                        color_counts = Counter(pixels_in_poly)
                        most_common_color, _ = color_counts.most_common(1)[0]
                        sampled_color_str = f"rgb({most_common_color[0]},{most_common_color[1]},{most_common_color[2]})"
                    #end if
                #end if
            #end if

            if RoughFillGenerator.IS_DEBUG:
                print(f"    -> Polygon [{idx}]: Area = {poly.area:.2f}, Color = {sampled_color_str}")
            #end if

            poly_curve = Curve(
                points=points,
                curve_type=CurveType.LINEAR_APPROXIMATE,
                is_broad=False
            )
            # 動的にcolorプロパティを持たせる
            poly_curve.color = sampled_color_str
            
            fill_layer.append(poly_curve)
        #end for
        
        fill_canvas.append(fill_layer)

        if RoughFillGenerator.IS_DEBUG:
            print("--- [RoughFillGenerator] End Generation ---\n")
        #end if
        
        return fill_canvas
    #end
#end class