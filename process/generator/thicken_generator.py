import numpy as np
from shapely.geometry import LineString, Polygon

from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from model.container.layer import Layer
from model.container.canvas import Canvas


class ThickenGenerator:
    IS_DEBUG = False

    @staticmethod
    def generate(stroke_canvas: Canvas, base_max_width: float = 4.0) -> Canvas:
        """
        線画キャンバス内の各曲線を解析し、入り・払い（テーパリング）のついた
        強弱のある美しいベクター面（Polygonとしての曲線）に変換して新しいキャンバスを返す。
        
        :param stroke_canvas: カット処理等が一通り終わった線画Canvas
        :param base_max_width: 線の最も太い部分の基準幅（ピクセル）
        """
        thicken_canvas = Canvas()
        thicken_canvas.set_view_box(stroke_canvas.view_box)

        if ThickenGenerator.IS_DEBUG:
            print("\n--- [ThickenGenerator] Start Variable Width Generation ---")
        #end if

        for stroke_layer in stroke_canvas:
            # 強弱のついた線は「面（塗りつぶし）」として出力するため、is_fill=True でレイヤーを作成
            thicken_layer = Layer(f"{stroke_layer.name}_thick", stroke_layer.color)
            thicken_layer.set_write_options(True, stroke_layer.color, stroke_layer.endpoint_style)
            for curve in stroke_layer:
                if len(curve.points) < 2:
                    continue
                #end if

                # 1. 頂点列の抽出と曲線の全長の計算
                coords = [(p.x, p.y) for p in curve.points]
                line = LineString(coords)
                total_length = line.length

                if total_length == 0:
                    continue
                #end if

                # 短い線は最大幅を制限する（短い線ほど最大でも細くなる）
                # 例: 全長が10ピクセル以下なら、本来の最大幅よりさらに細くスケールダウン
                length_scale = min(1.0, total_length / 30.0)
                actual_max_width = base_max_width * length_scale

                # 2. 左右へのオフセット頂点列を生成していく
                left_coords = []
                right_coords = []

                accumulated_dist = 0.0
                
                for i in range(len(coords)):
                    p_curr = np.array(coords[i])

                    # 進行方向の法線ベクトル（線の横を向くベクトル）を計算
                    if i == 0:
                        # 始点は次の点との方向
                        p_next = np.array(coords[i+1])
                        v_dir = p_next - p_curr
                    elif i == len(coords) - 1:
                        # 終点は前の点との方向
                        p_prev = np.array(coords[i-1])
                        v_dir = p_curr - p_prev
                    else:
                        # 中間点は前後のブレンド方向
                        p_next = np.array(coords[i+1])
                        p_prev = np.array(coords[i-1])
                        v_dir = p_next - p_prev
                    #end if

                    # 長さの累計から進行度 t (0.0 〜 1.0) を計算
                    if i > 0:
                        p_prev_exact = np.array(coords[i-1])
                        accumulated_dist += np.linalg.norm(p_curr - p_prev_exact)
                    #end if
                    t = clip(accumulated_dist / total_length, 0.0, 1.0)

                    # 🌟 サインカーブによる太さの変調 (入り・払いを細く、中央を太く)
                    # 太さ width = 最大太さ * sin(π * t)
                    current_width = actual_max_width * np.sin(np.pi * t)
                    half_w = current_width / 2.0

                    # 法線ベクトル（90度回転させて単位ベクトル化）
                    norm_dir = np.linalg.norm(v_dir)
                    if norm_dir > 0:
                        v_dir_unit = v_dir / norm_dir
                        # (x, y) -> (-y, x) で左側への法線
                        v_normal = np.array([-v_dir_unit[1], v_dir_unit[0]])
                    else:
                        v_normal = np.array([0.0, 0.0])
                    #end if

                    # 左右に広げた点を算出
                    p_left = p_curr + v_normal * half_w
                    p_right = p_curr - v_normal * half_w

                    left_coords.append(p_left)
                    # 右側は帰りのパスとして使うため逆順に繋ぐために一旦ストック
                    right_coords.insert(0, p_right)
                #end for

                # 3. 往路（左側）と復路（右側）を一本に繋いで閉じた外周（Polygon）にする
                # 始点と終点に向かって幅が0に収束するため、綺麗な一本の閉じたリボン状のループになります
                poly_coords = left_coords + right_coords
                
                # 始点に戻るように閉じる
                if poly_coords:
                    poly_coords.append(poly_coords[0])
                #end if

                # Curve オブジェクトにパックして格納
                thick_points = [Point(c[0], c[1]) for c in poly_coords]
                thick_curve = Curve(
                    points=thick_points,
                    curve_type=CurveType.LINEAR_APPROXIMATE,
                    is_broad=False
                )
                thicken_layer.append(thick_curve)
            #end for

            thicken_canvas.append(thicken_layer)
        #end for

        if ThickenGenerator.IS_DEBUG:
            print("--- [ThickenGenerator] End Generation ---\n")
        #end if

        return thicken_canvas
    #end

def clip(n, smallest, largest):
    return max(smallest, min(n, largest))
#end