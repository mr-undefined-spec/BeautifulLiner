# util/reader.py
import xml.etree.ElementTree as ET
from svgpath2mpl import parse_path
from model.primitive.point import Point
from model.curve.thin_linear_approximate_curve import ThinLinearApproximateCurve
from model.curve.thin_cubic_bezier_curve import ThinCubicBezierCurve
from model.container.layer import Layer
from model.container.canvas import Canvas

class Reader:
    @staticmethod
    def create_canvas_from_file(file_name: str) -> Canvas:
        if not isinstance(file_name, str):
            raise ValueError("file_name must be str")
        #end if

        canvas = Canvas()
        
        # XMLパース
        tree = ET.parse(file_name)
        root = tree.getroot()
        
        # 旧実装の仕様を引き継ぎ、ドキュメントツリーを保持
        canvas.set_doc(tree)
        
        # SVG要素のネームスペース対応
        ns = {"svg": "http://www.w3.org/2000/svg"}
        
        # viewBoxの取得
        if "viewBox" in root.attrib:
            canvas.set_view_box(root.attrib["viewBox"])
        #end if

        # <g> (レイヤー) を走査
        for group in root.findall(".//svg:g", ns):
            layer_name = group.get("id", "default_layer")
            paths = group.findall(".//svg:path", ns)
            
            if not paths:
                continue
            #end if
            
            first_stroke = paths[0].get("stroke", "#000000")
            layer = Layer(layer_name, first_stroke)
            
            for path_elem in paths:
                d_str = path_elem.get("d", "")
                mpl_path = parse_path(d_str)
                
                # 頂点リストの生成（浮動小数点の精度を安定させる）
                raw_points = [Point(round(float(v[0]), 3), round(float(v[1]), 3)) for v in mpl_path.vertices]
                
                # 連続する全く同じ座標（重複点）を排除して、ベジエの3N+1制約を壊さないようにする
                points = []
                for p in raw_points:
                    if not points or p.x != points[-1].x or p.y != points[-1].y:
                        points.append(p)
                    #end if
                #end for
                
                if not points:
                    continue
                #end if

                # パス文字列のコマンドで叩き分け
                if "C" in d_str.upper():
                    layer.append(ThinCubicBezierCurve(points))
                else:
                    layer.append(ThinLinearApproximateCurve(points))
                #end if
            #end for
            
            canvas.append(layer)
        #end for
        
        return canvas
    #end def
#end class