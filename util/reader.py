# util/reader.py
import xml.etree.ElementTree as ET
from svgpath2mpl import parse_path  # インポートを追加
from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
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
        
        canvas.set_doc(tree)
        
        # 名前空間の定義
        ns = {
            "svg": "http://www.w3.org/2000/svg",
            "inkpad": "http://taptrix.com/inkpad/svg_extensions"
        }
        
        # viewBoxの取得
        if "viewBox" in root.attrib:
            canvas.set_view_box(root.attrib["viewBox"])
        #end if

        # <g> (レイヤー) を走査
        for group in root.findall(".//svg:g", ns):
            inkpad_layer_attr = f"{{{ns['inkpad']}}}layerName"
            layer_name = group.get(inkpad_layer_attr)
            
            if not layer_name:
                layer_name = group.get("id", "default_layer")
            #end if
            
            paths = group.findall(".//svg:path", ns)
            if not paths:
                continue
            #end if
            
            first_stroke = paths[0].get("stroke", "#000000")
            layer = Layer(layer_name, first_stroke)
            
            # --- 各 path 要素の解析と Curve の生成 ---
            for path_element in paths:
                path_d = path_element.get("d")
                if not path_d:
                    continue
                #end if
                
                # svgpath2mpl でパースして直線近似の点列(ポリゴン)を取得
                mpl_path = parse_path(path_d)
                polygons = mpl_path.to_polygons()
                
                # 想定外の複合パス（複数の独立した線が1つのpathタグに入っている等）は例外を飛ばす
                if len(polygons) > 1:
                    raise ValueError(f"複合パスはサポートしていません。Layer: {layer_name}, d: {path_d}")
                #end if
                
                if len(polygons) == 0:
                    continue  # 空のパスはスキップ
                #end if
                
                # polygons[0]（NumPy配列）から座標を取り出す
                coords = polygons[0]
                
                # to_polygons() が勝手に追加した「始点に戻る末尾の1点」を
                # スライス [:-1] を使って綺麗に削ぎ落とす
                curve_points = [Point(float(x), float(y)) for x, y in coords][:-1]
                
                # 純粋な一筆書きの線として Curve を生成
                curve = Curve(curve_points, CurveType.LINEAR_APPROXIMATE)
                
                # 生成したCurveをLayerに追加
                layer.append(curve)
            #end for
            
            # 1つ以上のCurveが無事に追加されたLayerのみCanvasに追加する
            if len(layer) > 0:
                canvas.append(layer)
            #end if
        #end for
        
        return canvas
    #end def
#end class