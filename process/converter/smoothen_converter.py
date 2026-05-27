import numpy as np
from scipy.special import comb

from model.primitive.point import Point
from model.primitive.curve import Curve, CurveType
from process.converter.converter_base import ConverterBase

class SmoothenConverter(ConverterBase):

    @staticmethod
    def __get_bernstein_polynomial(n, t, k):
        """ Bernstein polynomial when a = 0 and b = 1. """
        return t ** k * (1 - t) ** (n - k) * comb(n, k)
    #end

    @staticmethod
    def __get_bernstein_matrix(degree, T):
        """ Bernstein matrix for Bezier curves. """
        matrix = []
        for t in T:
            row = []
            for k in range(degree + 1):
                # 旧SmoothenHandlerからSmoothenConverterに修正
                row.append( SmoothenConverter.__get_bernstein_polynomial(degree, t, k) )
            #end
            matrix.append(row)
        #end
        return np.array(matrix)
    #end

    @staticmethod
    def __least_square_fit(points, M):
        M_ = np.linalg.pinv(M)
        return np.matmul(M_, points)
    #end

    @staticmethod
    def convert(linear_approximate_curve: Curve) -> Curve:
        """ Least square qbezier fit using penrose pseudoinverse.

        Based on https://stackoverflow.com/questions/12643079/b%C3%A9zier-curve-fitting-with-scipy
        and probably on the 1998 thesis by Tim Andrew Pastva, "Bezier Curve Fitting".
        """

        degree = 3 # only cubic bezier curve

        # 新生Curveのpointsプロパティから直接点列を取得
        src_points = linear_approximate_curve.points

        x_array = [p.x for p in src_points]
        y_array = [p.y for p in src_points]

        x_data = np.array(x_array)
        y_data = np.array(y_array)

        T = np.linspace(0, 1, len(x_data))
        # 旧SmoothenHandlerからSmoothenConverterに修正
        M = SmoothenConverter.__get_bernstein_matrix(degree, T)
        points = np.array(list(zip(x_data, y_data)))

        # 旧SmoothenHandlerからSmoothenConverterに修正
        fit = SmoothenConverter.__least_square_fit(points, M).tolist()

        # 始点と終点は元のデータから完全に一致させる
        first_point = Point(x_data[0], y_data[0])
        last_point  = Point(x_data[-1], y_data[-1])

        # フィッティングによって得られた制御点をPointオブジェクトに変換
        # fit[0] は始点、fit[3] は終点に対応しますが、誤差をなくすため元の端点を使用します
        control_point_1 = Point(fit[1][0], fit[1][1])
        control_point_2 = Point(fit[2][0], fit[2][1])

        # 新生Curveの「3次ベジェ（4点）」の仕様に合わせてリスト化
        bezier_points = [
            first_point,
            control_point_1,
            control_point_2,
            last_point
        ]

        # CUBIC_BEZIERを指定して、新生Curveのインスタンスを生成して返す
        return Curve(
            points=bezier_points, 
            curve_type=CurveType.CUBIC_BEZIER, 
            is_broad=linear_approximate_curve.is_broad
        )
    #end
#end