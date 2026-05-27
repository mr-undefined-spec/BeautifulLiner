import xml.etree.ElementTree as ET
from shapely.geometry import LineString
from svgpath2mpl import parse_path

# 1. 定義を修正したサンプルのSVGデータ（ファイルから直接読み込む場合は下の注釈を参照）
svg_data = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     xmlns:inkpad="http://taptrix.com/inkpad/svg_extensions" 
     width="1024" height="1024" viewBox="0 0 1024 1024">
<g id="Hair" inkpad:layerName="Hair">
<path stroke="#00ff00" stroke-width="1" d="M227.192+66.1948C227.192+62.9753+225.1+72.6394+225.1+74.0956C225.1+80.9509+224.845+87.9447+225.333+94.7769C226.675+113.575+231.743+138.335+242.993+153.335" fill="none"/>
</g>
</svg>"""

# --- メモ: 実際のファイル（○○.svg）から直接読み込む場合は以下のように書き換えてください ---
# tree = ET.parse("実際のファイル名.svg")
# root = tree.getroot()
# ----------------------------------------------------------------------------------

# 文字列からパースする（サンプルの場合）
root = ET.fromstring(svg_data)

# SVGの名前空間（xmlns）を指定して最初のpathを検索
namespaces = {"svg": "http://www.w3.org/2000/svg"}
first_path_element = root.find(".//svg:path", namespaces)

if first_path_element is not None:
    path_d = first_path_element.get("d")
    print("--- 抽出した最初のpathデータ (d属性) ---")
    print(path_d)

    # svgpath2mpl でパース
    mpl_path = parse_path(path_d)
    polygons = mpl_path.to_polygons()

    if len(polygons) > 0:
        coords = polygons[0]
        # shapely の LineString オブジェクトに変換
        shapely_line = LineString(coords)

        print(f"\n--- shapely オブジェクトに変換成功 ---")
        print(f"型: {type(shapely_line)}")
        print(f"始点: {shapely_line.coords[0]}")
        print(f"終点: {shapely_line.coords[-1]}")
        print(f"頂点数: {len(shapely_line.coords)}")
    else:
        print("パスのポリライン化に失敗しました。")
else:
    print("path要素が見つかりませんでした。")