from shapely.geometry import LineString, MultiLineString, box
from shapely.ops import unary_union, polygonize

from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from model.container.layer import Layer
from model.container.canvas import Canvas


class RoughFillGenerator:
    IS_DEBUG = False

    @staticmethod
    def generate(stroke_canvas: Canvas) -> Canvas:
        """
        キャンバス全体を取り囲む矩形（外枠）を追加し、全レイヤーの曲線と統合。
        外枠にぶつかって閉じた領域も含めて、すべての閉領域（面）を抽出する。
        """
        fill_canvas = Canvas()
        fill_canvas.set_view_box(stroke_canvas.view_box)

        if RoughFillGenerator.IS_DEBUG:
            print("\n--- [RoughFillGenerator] Start Generation (Global Outer Boundary Mode) ---")
        #end if

        # 1. view_box からキャンバス全体を囲む外枠の線分（矩形）を生成する
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

        if RoughFillGenerator.IS_DEBUG:
            print(f"  - Canvas Boundary Detected: L:{minx}, T:{miny}, R:{maxx}, B:{maxy}")
        #end if

        # Shapelyのbox関数から外枠のポリゴンを作り、その外周をLineString（線分データ）として取得
        outer_box = box(minx, miny, maxx, maxy)
        outer_boundary_line = LineString(outer_box.exterior.coords)

        # 全ての線分を集めるリスト（最初に外枠を入れておく）
        all_lines = [outer_boundary_line]
        total_input_curves = 0

        # 2. 全レイヤーのすべてのCurveから一挙にShapelyのLineStringを抽出して追加
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

        if RoughFillGenerator.IS_DEBUG:
            print(f"  - Total input curves across all layers: {total_input_curves}")
            print(f"  - Combined LineString count (including Outer Box): {len(all_lines)}")
        #end if

        fill_layer = Layer("rough_fill", "#000000")

        # 3. 外枠＋全線分をまとめて交差点で分解（ノード化）し、閉じた面（Polygon）を自動抽出
        intersected_lines = unary_union(all_lines)
        polygons = list(polygonize(intersected_lines))
        
        if RoughFillGenerator.IS_DEBUG:
            print(f"  - Total extracted polygons (with Outer Boundary): {len(polygons)}")
        #end if

        # 4. 抽出されたすべてのPolygon群を、Curveオブジェクトにパックして単一レイヤーへ格納
        for idx, poly in enumerate(polygons):
            coords = list(poly.exterior.coords)
            points = [Point(c[0], c[1]) for c in coords]
            
            if RoughFillGenerator.IS_DEBUG:
                print(f"    -> Polygon [{idx}]: Area = {poly.area:.2f}, Points = {len(points)}")
            #end if

            poly_curve = Curve(
                points=points,
                curve_type=CurveType.LINEAR_APPROXIMATE,
                is_broad=False
            )
            fill_layer.append(poly_curve)
        #end for
        
        fill_canvas.append(fill_layer)

        if RoughFillGenerator.IS_DEBUG:
            print("--- [RoughFillGenerator] End Generation ---\n")
        #end if
        
        return fill_canvas
    #end
#end class