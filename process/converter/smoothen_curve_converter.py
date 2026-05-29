import numpy as np
from scipy.special import comb

from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from process.converter.curve_list_converter_base import CurveListConverterBase
from process.converter.smoother.split_co_converter import SplitCoConverter


class SmoothenCurveConverter(CurveListConverterBase):
    """長い直線近似曲線のリストを受け取り、それぞれを内部で適切に分割・フィッティングして、
    滑らかな3次ベジェ曲線のリストへと変換するコンバーター。
    """

    @staticmethod
    def __get_bernstein_polynomial(n: int, t: float, k: int) -> float:
        """ Bernstein polynomial when a = 0 and b = 1. """
        return t ** k * (1 - t) ** (n - k) * comb(n, k)
    #end

    @staticmethod
    def __get_bernstein_matrix(degree: int, T: np.ndarray) -> np.ndarray:
        """ Bernstein matrix for Bezier curves. """
        matrix = []
        for t in T:
            row = []
            for k in range(degree + 1):
                row.append(SmoothenCurveConverter.__get_bernstein_polynomial(degree, t, k))
            #end
            matrix.append(row)
        #end
        return np.array(matrix)
    #end

    @staticmethod
    def __least_square_fit(points: np.ndarray, M: np.ndarray) -> np.ndarray:
        M_ = np.linalg.pinv(M)
        return np.matmul(M_, points)
    #end

    @staticmethod
    def __fit_single_curve(sub_curve: Curve) -> list[Point]:
        """単一の直線近似曲線を1本の3次ベジェ曲線（4つのPoint）にフィッティングする（内部用ヘルパー）"""
        degree = 3
        src_points = sub_curve.points

        x_data = np.array([p.x for p in src_points])
        y_data = np.array([p.y for p in src_points])

        T = np.linspace(0, 1, len(x_data))
        M = SmoothenCurveConverter.__get_bernstein_matrix(degree, T)
        points_matrix = np.array(list(zip(x_data, y_data)))

        fit = SmoothenCurveConverter.__least_square_fit(points_matrix, M).tolist()

        # 幾何的な連続性を厳密に守るため、始点と終点は元の実データを最優先する
        first_point = Point(x_data[0], y_data[0])
        control_point_1 = Point(fit[1][0], fit[1][1])
        control_point_2 = Point(fit[2][0], fit[2][1])
        last_point = Point(x_data[-1], y_data[-1])

        return [first_point, control_point_1, control_point_2, last_point]
    #end

    def convert(self, curves: list[Curve]) -> list[Curve]:
        """複数（または単一）の直線近似曲線のリストを受け取り、
        それぞれを平滑化した3次ベジェ曲線のリストにして返却する。
        """
        output_curves = []

        for linear_approximate_curve in curves:
            # 1. 下請け職人（SplitCoConverter）に依頼して、変曲点や急角で小分けにしてもらう
            sub_curves = SplitCoConverter.convert_to_multiple(linear_approximate_curve)
            
            combined_bezier_points = []
            
            # 2. 小分けにされた各セグメントをフィッティング
            for i, sub_curve in enumerate(sub_curves):
                bezier_four_points = self.__fit_single_curve(sub_curve)
                
                if i == 0:
                    # 最初のセグメントは4点すべてをそのまま追加
                    combined_bezier_points.extend(bezier_four_points)
                else:
                    # 2本目以降は「前のセグメントの終点」と「現在のセグメントの始点」が重複するため、
                    # 始点（0番目）をスキップして、制御点2つと終点の計3点を追加していく (3N + 1 のルールを自然に満たす)
                    combined_bezier_points.extend(bezier_four_points[1:])
                #end if
            #end for

            # 3. 連結された1本の新生CUBIC_BEZIERオブジェクトを構築
            smoothened_curve = Curve(
                points=combined_bezier_points,
                curve_type=CurveType.CUBIC_BEZIER,
                is_broad=linear_approximate_curve.is_broad
            )
            output_curves.append(smoothened_curve)
        #end for

        return output_curves
    #end
#end class