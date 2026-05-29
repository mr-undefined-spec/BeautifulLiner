from enum import Enum, auto

class PreProcessMode(Enum):
    """入力Canvasから、どのスコープ（範囲）でCurve群を抽出するかを指定するモード"""
    SINGLE_CURVE = auto()   # 1本のCurve単位でループを回して抽出（1対1）
    LAYER_LEVEL = auto()    # Layer単位で所属する全Curveをまとめて抽出（多対多）
    CANVAS_LEVEL = auto()   # Canvas全体からすべてのCurveを1つに集約して抽出（多対多）
#end class