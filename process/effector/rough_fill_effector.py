import numpy as np
from collections import Counter
from PIL import Image, ImageDraw
from shapely.geometry import LineString, box
from shapely.ops import unary_union, polygonize

from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType


class RoughFillEffector:
    """線画から閉領域（ポリゴン）を自動抽出し、参照画像から最頻色をサンプリングして
    塗りつぶし用の面（Curve群）を生成するエフェクター。
    """

    def __init__(self, view_box: str | tuple | list = None, reference_image: Image.Image = None):
        """
        :param view_box: キャンバスの外枠境界を指定するSVG準拠のviewBox（"x y w h" または [x, y, w, h]）。
                         None の場合は入力曲線全体のバウンディングボックスから外枠を自動決定します。
        :param reference_image: カラー参照用のPIL Imageオブジェクト（オプショナル）
        """
        self.view_box = view_box
        self.reference_image = reference_image
    #end def

    def apply(self, curves: list[Curve]) -> list[Curve]:
        """受け取った単線リストから閉領域を抽出し、サンプリングされたカラー属性付きの
        ポリゴン（Curve）のリストを新規に生成して返す。
        """
        if not curves:
            return []
        #end if

        # 1. view_box または入力点列からキャンバス全体を囲む外枠の矩形を算出
        minx, miny, maxx, maxy = self._calculate_bounds(curves)
        outer_box = box(minx, miny, maxx, maxy)
        outer_boundary_line = LineString(outer_box.exterior.coords)

        all_lines = [outer_boundary_line]

        # 2. すべてのCurveからLineStringを抽出
        for curve in curves:
            if len(curve.points) < 2:
                continue
            #end if
            line = LineString([(p.x, p.y) for p in curve.points])
            all_lines.append(line)
        #end for

        # 3. 外枠＋全線分をまとめて交差点で分解し、閉じた面（Polygon）を自動抽出
        intersected_lines = unary_union(all_lines)
        polygons = list(polygonize(intersected_lines))

        # カラー参照画像が存在する場合、RGBモードに変換してピクセルアクセスを高速化
        img_rgb = self.reference_image.convert("RGB") if self.reference_image is not None else None
        fill_curves = []

        # 4. 抽出されたすべてのPolygon群をCurveオブジェクトにパック
        for poly in polygons:
            if poly.area <= 0:
                continue
            #end if

            coords = list(poly.exterior.coords)
            points = [Point(c[0], c[1]) for c in coords]
            
            # 画像から最頻色をサンプリング
            sampled_color_str = self._sample_most_common_color(poly, coords, img_rgb) if img_rgb is not None else None

            poly_curve = Curve(
                points=points,
                curve_type=CurveType.LINEAR_APPROXIMATE,
                is_broad=False
            )
            # 動的にcolor属性を注入（Writer側で参照可能にする）
            poly_curve.color = sampled_color_str
            
            fill_curves.append(poly_curve)
        #end for

        return fill_curves
    #end def

    # -------------------------------------------------------------------------
    # 内部計算・サンプリングヘルパー
    # -------------------------------------------------------------------------

    def _calculate_bounds(self, curves: list[Curve]) -> tuple[float, float, float, float]:
        """外枠矩形の境界を決定する。"""
        if self.view_box is not None:
            try:
                if isinstance(self.view_box, str):
                    vb = [float(x) for x in self.view_box.split()]
                    return vb[0], vb[1], vb[0] + vb[2], vb[1] + vb[3]
                elif len(self.view_box) == 4:
                    return float(self.view_box[0]), float(self.view_box[1]), float(self.view_box[0] + self.view_box[2]), float(self.view_box[1] + self.view_box[3])
                #end if
            except Exception:
                pass
            #end try
        #end if

        # view_boxがない、あるいはパース失敗時は点列のbboxを算出
        all_x = [p.x for c in curves for p in c.points]
        all_y = [p.y for c in curves for p in c.points]
        if not all_x or not all_y:
            return 0.0, 0.0, 100.0, 100.0
        #end if
        return min(all_x), min(all_y), max(all_x), max(all_y)
    #end def

    def _sample_most_common_color(self, poly, coords: list, img_rgb: Image.Image) -> str | None:
        """ポリゴンマスクの内部から最も多く使われている色を抽出する。"""
        p_minx, p_miny, p_maxx, p_maxy = poly.bounds
        ix_min = max(0, int(p_minx))
        iy_min = max(0, int(p_miny))
        ix_max = min(img_rgb.width - 1, int(p_maxx))
        iy_max = min(img_rgb.height - 1, int(p_maxy))

        if ix_max < ix_min or iy_max < iy_min:
            return None
        #end if

        w = ix_max - ix_min + 1
        h = iy_max - iy_min + 1
        mask = Image.new("L", (w, h), 0)
        draw = ImageDraw.Draw(mask)
        
        local_coords = [(c[0] - ix_min, c[1] - iy_min) for c in coords]
        draw.polygon(local_coords, fill=255)

        pixels_in_poly = []
        for dy in range(h):
            for dx in range(w):
                if mask.getpixel((dx, dy)) == 255:
                    px = img_rgb.getpixel((ix_min + dx, iy_min + dy))
                    pixels_in_poly.append(px)
                #end if
            #end for
        #end for

        if pixels_in_poly:
            color_counts = Counter(pixels_in_poly)
            most_common_color, _ = color_counts.most_common(1)[0]
            return f"rgb({most_common_color[0]},{most_common_color[1]},{most_common_color[2]})"
        #end if
        return None
    #end def
#end class