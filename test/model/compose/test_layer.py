
import os
import sys
import math

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/compose'))

from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from cubic_bezier_curve import CubicBezierCurve
from linear_approximate_curve import LinearApproximateCurve

from layer import Layer

import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import test_helpers

class TestLayer(unittest.TestCase):
    def setUp(self):
        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 2.0)
        p2 = Point(10.0, 20.0)
        p3 = Point(100.0, 200.0)

        bezier_ctrl_p = CubicBezierCurveControlPoint(p0, p1, p2, p3)

        bezier_curve = CubicBezierCurve()
        bezier_curve.append(bezier_ctrl_p)
        bezier_curve.append(bezier_ctrl_p)

        self.bezier_layer = Layer()
        self.bezier_layer.append(bezier_curve)
        self.bezier_layer.append(bezier_curve)

        lin_p0 = Point(0.0, 0.0)
        lin_p1 = Point(1.0, 1.0)
        lin_p2 = Point(1.0, 0.0)
        lin_p3 = Point(0.0, 1.0)
        lin_p4 = Point(2.0, 1.0)

        linear_ctrl_p_0_1 = LinearApproximateCurveControlPoint(lin_p0, lin_p1)
        linear_ctrl_p_2_3 = LinearApproximateCurveControlPoint(lin_p2, lin_p3)
        linear_ctrl_p_2_4 = LinearApproximateCurveControlPoint(lin_p2, lin_p4)

        linear_curve = LinearApproximateCurve()
        linear_curve.append(linear_ctrl_p_0_1)
        linear_curve.append(linear_ctrl_p_2_3)
        linear_curve.append(linear_ctrl_p_2_4)

        self.linear_layer = Layer()
        self.linear_layer.append(linear_curve)
        self.linear_layer.append(linear_curve)
    #end

    def test_init_segment_set(self):
        self.assertEqual(self.linear_layer[0][0].s.x, 0.0)
        self.assertEqual(self.linear_layer[0][0].s.y, 0.0)
        self.assertEqual(self.linear_layer[0][0].e.x, 1.0)
        self.assertEqual(self.linear_layer[0][0].e.y, 1.0)

        self.assertEqual(self.linear_layer[0][1].s.x, 1.0)
        self.assertEqual(self.linear_layer[0][1].s.y, 0.0)
        self.assertEqual(self.linear_layer[0][1].e.x, 0.0)
        self.assertEqual(self.linear_layer[0][1].e.y, 1.0)
    #end

    def test_init_cubic_bezier_curve_set(self):
        self.assertEqual(self.bezier_layer[0][0].p0.x, 0.0)
        self.assertEqual(self.bezier_layer[0][0].p0.y, 0.0)
        self.assertEqual(self.bezier_layer[0][0].p1.x, 1.0)
        self.assertEqual(self.bezier_layer[0][0].p1.y, 2.0)
        self.assertEqual(self.bezier_layer[0][0].p2.x, 10.0)
        self.assertEqual(self.bezier_layer[0][0].p2.y, 20.0)
        self.assertEqual(self.bezier_layer[0][0].p3.x, 100.0)
        self.assertEqual(self.bezier_layer[0][0].p3.y, 200.0)
    #end

    def test_delete_edge(self):

        num_angle_divisions = 100
        radius = 100.0
        center = Point(0.0, 0.0)
        # LinearApproximateCurve of 0 ~ 90degree arc ( radius=100, center=(0.0,0.0) )
        linear_approximate_curve = test_helpers.create_arc(radius, center, 0.0, 90.0, num_angle_divisions)

        center2 = Point(100.0, 0.0)
        # LinearApproximateCurve of 90 ~ 180 degree arc ( radius=100, center=(100.0,0.0) )
        lin_curve2 = test_helpers.create_arc(radius, center2, 90.0, 180.0, num_angle_divisions)

        layer = Layer()
        layer.append(linear_approximate_curve)
        layer.append(lin_curve2)


        bbox = (0.0, 0.0, 180.0, 180.0)
        layer.create_intersect_judge_rectangle(bbox)
        new_layer = layer.delete_edge(bbox, 0.5, 0, "TEST")
        the_answer = '<path d="M 100.000 0.000 L 99.988 1.571 L 99.951 3.141 L 99.889 4.711 L 99.803 6.279 L 99.692 7.846 L 99.556 9.411 L 99.396 10.973 L 99.211 12.533 L 99.002 14.090 L 98.769 15.643 L 98.511 17.193 L 98.229 18.738 L 97.922 20.279 L 97.592 21.814 L 97.237 23.345 L 96.858 24.869 L 96.456 26.387 L 96.029 27.899 L 95.579 29.404 L 95.106 30.902 L 94.609 32.392 L 94.088 33.874 L 93.544 35.347 L 92.978 36.812 L 92.388 38.268 L 91.775 39.715 L 91.140 41.151 L 90.483 42.578 L 89.803 43.994 L 89.101 45.399 L 88.377 46.793 L 87.631 48.175 L 86.863 49.546 L 86.074 50.904 L 85.264 52.250 L 84.433 53.583 L 83.581 54.902 L 82.708 56.208 L 81.815 57.501 L 80.902 58.779 L 79.968 60.042 L 79.016 61.291 L 78.043 62.524 L 77.051 63.742 L 76.041 64.945 L 75.011 66.131 L 73.963 67.301 L 72.897 68.455 L 71.813 69.591 L 70.711 70.711 L 69.591 71.813 L 68.455 72.897 L 67.301 73.963 L 66.131 75.011 L 64.945 76.041 L 63.742 77.051 L 62.524 78.043 L 61.291 79.016 L 60.042 79.968 L 58.779 80.902 L 57.501 81.815 L 56.208 82.708 L 54.902 83.581 L 53.583 84.433 L 52.250 85.264 L 50.904 86.074 " fill="none" opacity="1" stroke="#ff0000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" />\n<path d="M 50.454 86.863 L 49.096 86.074 L 47.750 85.264 L 46.417 84.433 L 45.098 83.581 L 43.792 82.708 L 42.499 81.815 L 41.221 80.902 L 39.958 79.968 L 38.709 79.016 L 37.476 78.043 L 36.258 77.051 L 35.055 76.041 L 33.869 75.011 L 32.699 73.963 L 31.545 72.897 L 30.409 71.813 L 29.289 70.711 L 28.187 69.591 L 27.103 68.455 L 26.037 67.301 L 24.989 66.131 L 23.959 64.945 L 22.949 63.742 L 21.957 62.524 L 20.984 61.291 L 20.032 60.042 L 19.098 58.779 L 18.185 57.501 L 17.292 56.208 L 16.419 54.902 L 15.567 53.583 L 14.736 52.250 L 13.926 50.904 L 13.137 49.546 L 12.369 48.175 L 11.623 46.793 L 10.899 45.399 L 10.197 43.994 L 9.517 42.578 L 8.860 41.151 L 8.225 39.715 L 7.612 38.268 L 7.022 36.812 L 6.456 35.347 L 5.912 33.874 L 5.391 32.392 L 4.894 30.902 L 4.421 29.404 L 3.971 27.899 L 3.544 26.387 L 3.142 24.869 L 2.763 23.345 L 2.408 21.814 L 2.078 20.279 L 1.771 18.738 L 1.489 17.193 L 1.231 15.643 L 0.998 14.090 L 0.789 12.533 L 0.604 10.973 L 0.444 9.411 L 0.308 7.846 L 0.197 6.279 L 0.111 4.711 L 0.049 3.141 L 0.012 1.571 L 0.000 0.000 " fill="none" opacity="1" stroke="#ff0000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" />\n'
        self.assertEqual( new_layer.to_svg(), the_answer )
    #end

    def test_delete_edge(self):

        num_angle_divisions = 100
        radius = 100.0
        center = Point(0.0, 0.0)
        # LinearApproximateCurve of 0 ~ 90degree arc ( radius=100, center=(0.0,0.0) )
        linear_approximate_curve = test_helpers.create_arc(radius, center, 0.0, 90.0, num_angle_divisions)

        center2 = Point(100.0, 0.0)
        # LinearApproximateCurve of 90 ~ 180 degree arc ( radius=100, center=(100.0,0.0) )
        lin_curve2 = test_helpers.create_arc(radius, center2, 90.0, 180.0, num_angle_divisions)

        layer = Layer()
        layer.append(linear_approximate_curve)
        layer.append(lin_curve2)

        bbox = (0.0, 0.0, 180.0, 180.0)
        layer.create_intersect_judge_rectangle(bbox)
        new_layer = layer.delete_edge(bbox, 0.5, 0, "TEST")

        broad_layer = new_layer.broaden(1.0, 0, "TEST")
    #end

    def test_create_continuous_curve_index_group(self):

        num_angle_divisions = 100
        radius = 100.0
        center = Point(0.0, 0.0)

        # LinearApproximateCurve of 0 ~ 90 degree arc ( radius=100, center=(0.0,0.0) )
        linear_approximate_curve_0_90 = test_helpers.create_arc(radius, center, 0.0, 90.0, num_angle_divisions)

        # LinearApproximateCurve of 45 ~ 135 degree arc ( radius=100, center=(0.0,0.0) )
        linear_approximate_curve_45_135 = test_helpers.create_arc(radius, center, 45.0, 135.0, num_angle_divisions)

        # LinearApproximateCurve of 90 ~ 180 degree arc ( radius=100, center=(0.0,0.0) )
        linear_approximate_curve_90_180 = test_helpers.create_arc(radius, center, 90.0, 180.0, num_angle_divisions)

        # LinearApproximateCurve of 135 ~ 225 degree arc ( radius=100, center=(0.0,0.0) )
        linear_approximate_curve_135_225 = test_helpers.create_arc(radius, center, 135.0, 225.0, num_angle_divisions)

        bbox = (0.0, 0.0, 180.0, 180.0)

        layer = Layer()
        layer.append(linear_approximate_curve_0_90)
        layer.append(linear_approximate_curve_45_135)
        layer.append(linear_approximate_curve_90_180)
        layer.append(linear_approximate_curve_135_225)

        layer.create_intersect_judge_rectangle(bbox)
        layer.create_continuous_curve_index_group(1.0)

        #print(layer.continuous_curve_index_group)
        # [[0, 1, 2, 3]]
        self.assertEqual(layer.continuous_curve_index_group, [[0, 1, 2, 3]])

        layer2 = Layer()
        layer2.append(linear_approximate_curve_0_90)
        layer2.append(linear_approximate_curve_45_135)
        layer2.append(linear_approximate_curve_135_225)
        layer2.append(linear_approximate_curve_90_180)

        layer2.create_intersect_judge_rectangle(bbox)
        layer2.create_continuous_curve_index_group(1.0)
        #print(layer2.continuous_curve_index_group)
        # [[0, 1, 3, 2]]
        self.assertEqual(layer2.continuous_curve_index_group, [[0, 1, 3, 2]])

        layer3 = Layer()
        layer3.append(linear_approximate_curve_135_225)
        layer3.append(linear_approximate_curve_0_90)
        layer3.append(linear_approximate_curve_90_180)
        layer3.append(linear_approximate_curve_45_135)

        layer3.create_intersect_judge_rectangle(bbox)
        layer3.create_continuous_curve_index_group(1.0)
        #print(layer3.continuous_curve_index_group)
        # [[1, 3, 2, 0]]
        self.assertEqual(layer3.continuous_curve_index_group, [[1, 3, 2, 0]])

        center2 = Point(100.0, 0.0)

        # LinearApproximateCurve of 90 ~ 180 degree arc ( radius=100, center=(100.0,0.0) )
        lin_curve2_90_180 = test_helpers.create_arc(radius, center2, 90.0, 180.0, num_angle_divisions)

        # LinearApproximateCurve of 135 ~ 225 degree arc ( radius=100, center=(100.0,0.0) )
        lin_curve2_135_225 = test_helpers.create_arc(radius, center2, 135.0, 225.0, num_angle_divisions)

        # LinearApproximateCurve of 180 ~ 270 degree arc ( radius=100, center=(100.0,0.0) )
        lin_curve2_180_270 = test_helpers.create_arc(radius, center2, 180.0, 270.0, num_angle_divisions)

        layer4 = Layer()
        layer4.append(linear_approximate_curve_135_225)
        layer4.append(linear_approximate_curve_0_90)
        layer4.append(linear_approximate_curve_90_180)
        layer4.append(linear_approximate_curve_45_135)
        layer4.append(lin_curve2_90_180)
        layer4.append(lin_curve2_180_270)
        layer4.append(lin_curve2_135_225)

        layer4.create_intersect_judge_rectangle(bbox)
        layer4.create_continuous_curve_index_group(1.0)
        #print(layer4.continuous_curve_index_group)
        # [[1, 3, 2, 0], [4, 6, 5]]
        self.assertEqual(layer4.continuous_curve_index_group, [[1, 3, 2, 0], [4, 6, 5]])
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end

