from shapely.geometry import LineString
from shapely.ops import unary_union, polygonize

from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from model.container.layer import Layer
from model.container.canvas import Canvas


class RoughFillGenerator:

    @staticmethod
    def generate(stroke_canvas: Canvas) -> Canvas:
        """
        線画キャンバス（stroke_canvas）を解析し、交差関係から閉領域を自動抽出して、
        ラフ塗り用の面（POLYGON）で構成された新しいキャンバスを生成して返す。
        """
        fill_canvas = Canvas()
        fill_canvas.set_view_box(stroke_canvas.view_box)

        for stroke_layer in stroke_canvas:
            # 1. 各レイヤーに対応する「塗り用レイヤー」を新規作成
            fill_layer = Layer(f"{stroke_layer.name}_fill", stroke_layer.color)
            
            # 2. レイヤー内の全CurveからShapelyのLineStringを抽出
            lines = []
            for curve in stroke_layer:
                if len(curve.points) < 2:
                    continue
                #end if
                line = LineString([(p.x, p.y) for p in curve.points])
                lines.append(line)
            #end for

            if not lines:
                fill_canvas.append(fill_layer)
                continue
            #end if

            # 3. 交差点で線分を分解（ノード化）し、閉じた面（Polygon）を自動抽出
            intersected_lines = unary_union(lines)
            polygons = list(polygonize(intersected_lines))

            # 4. 抽出されたPolygon群を、塗りつぶし領域を表す新しいCurveオブジェクトとして格納
            for poly in polygons:
                coords = list(poly.exterior.coords)
                points = [Point(c[0], c[1]) for c in coords]
                
                # 線ではなく面であることを示す適切なCurveTypeを指定
                # ※ モデルの定義に合わせて調整してください（例: CurveType.POLYGON や FILL_AREA など）
                poly_curve = Curve(
                    points=points,
                    curve_type=CurveType.LINEAR_APPROXIMATE,
                    is_broad=False
                )
                fill_layer.append(poly_curve)
            #end for
            
            fill_canvas.append(fill_layer)
        #end for

        return fill_canvas
    #end
#end class