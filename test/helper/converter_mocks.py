import math
from enum import Enum, auto
from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from model.container.layer import Layer

class ArcDirection(Enum):
    CLOCKWISE = auto()
    COUNTER_CLOCKWISE = auto()
#end class


def create_mock_linear_approximate_curve_of_arc(
    radius: float, 
    center_x: float, 
    center_y: float, 
    start_angle: float, 
    end_angle: float, 
    num_divisions: int, 
    arc_direction: ArcDirection
) -> Curve:
    """円弧をサンプリングして、新生Curve（LINEAR_APPROXIMATE）を生成する"""
    
    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    
    # 分割数に応じた角度のステップを計算
    t_steps = [i / num_divisions for i in range(num_divisions + 1)]
    
    # 反時計回りの場合は、媒介変数の走査順を逆転させるだけでスマートに解決
    if arc_direction == ArcDirection.COUNTER_CLOCKWISE:
        t_steps.reverse()
    #end if

    points = []
    for t in t_steps:
        # start_rad から end_rad への線形補間
        theta = start_rad + (end_rad - start_rad) * t
        
        x = radius * math.cos(theta) + center_x
        y = radius * math.sin(theta) + center_y
        points.append(Point(x, y))
    #end for

    # モックではなく、本物の新生Curveオブジェクトを生成して返す
    return Curve(points=points, curve_type=CurveType.LINEAR_APPROXIMATE)
#end def


def create_mock_layer_set_of_cubic_bezier_curve_arc() -> list[Layer]:
    """テスト用の3次ベジェ曲線を含むレイヤーセット（Canvas等で利用）を生成する"""
    
    # 半径100、90度円弧のコントロールポイントを幾何計算
    p0 = Point(100.0, 0.0)
    p1 = Point(100.0, 400.0 * (math.sqrt(2.0) - 1.0) / 3.0)
    p2 = Point(400.0 * (math.sqrt(2.0) - 1.0) / 3.0, 100.0)
    p3 = Point(0.0, 100.0)
    
    # 4つの点をフラットに渡してCUBIC_BEZIERを生成
    bezier_curve = Curve(
        points=[p0, p1, p2, p3], 
        curve_type=CurveType.CUBIC_BEZIER
    )
    
    # 新生Layerクラス（本物）を生成して詰め込む
    layer = Layer(name="test_layer", color="#00ff00")
    layer.append(bezier_curve)
    
    return [layer]
#end def


def create_mock_linear_layer_set_of_arc(
    radius: float, 
    center_x: float, 
    center_y: float, 
    start_angle: float, 
    end_angle: float, 
    num_divisions: int,
    arc_direction: ArcDirection = ArcDirection.CLOCKWISE
) -> list[Layer]:
    """テスト用の直線近似円弧を含むレイヤーセットを生成する"""
    
    # 上で作った関数を再利用してCurveを取得
    linear_curve = create_mock_linear_approximate_curve_of_arc(
        radius, center_x, center_y, start_angle, end_angle, num_divisions, arc_direction
    )
    
    layer = Layer(name="test_linear_layer", color="#ff0000")
    layer.append(linear_curve)
    
    return [layer]
#end def