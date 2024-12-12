
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/curve'))
from point import Point
from cubic_bezier_curve_control_point import CubicBezierCurveControlPoint
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from cubic_bezier_curve import CubicBezierCurve
from linear_approximate_curve import LinearApproximateCurve
from broad_cubic_bezier_curve import BroadCubicBezierCurve
from broad_linear_approximate_curve import BroadLinearApproximateCurve
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import test_helpers

import numpy as np
import math

class TestCurve(unittest.TestCase):
    def setUp(self):
        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 2.0)
        p2 = Point(10.0, 20.0)
        p3 = Point(100.0, 200.0)

        bezier_ctrl_p = CubicBezierCurveControlPoint(p0, p1, p2, p3)

        self.bezier_curve = CubicBezierCurve()
        self.bezier_curve.append(bezier_ctrl_p)
        self.bezier_curve.append(bezier_ctrl_p)

        lin_p0 = Point(0.0, 0.0)
        lin_p1 = Point(1.0, 1.0)
        lin_p2 = Point(1.0, 0.0)
        lin_p3 = Point(0.0, 1.0)
        lin_p4 = Point(2.0, 1.0)

        linear_ctrl_p_0_1 = LinearApproximateCurveControlPoint(lin_p0, lin_p1)
        linear_ctrl_p_2_3 = LinearApproximateCurveControlPoint(lin_p2, lin_p3)
        linear_ctrl_p_2_4 = LinearApproximateCurveControlPoint(lin_p2, lin_p4)

        self.linear_curve = LinearApproximateCurve()
        self.linear_curve.append(linear_ctrl_p_0_1)
        self.linear_curve.append(linear_ctrl_p_2_3)
        self.linear_curve.append(linear_ctrl_p_2_4)

    #end

    def test_create_intersect_judge_rectangle(self):
        # linear_curve
        self.linear_curve.create_intersect_judge_rectangle()
        self.assertEqual( self.linear_curve.rect.q.x, 0.0 )
        self.assertEqual( self.linear_curve.rect.q.y, 0.0 )
        self.assertEqual( self.linear_curve.rect.z.x, 0.0 )
        self.assertEqual( self.linear_curve.rect.z.y, 1.0 )
        self.assertEqual( self.linear_curve.rect.p.x, 2.0 )
        self.assertEqual( self.linear_curve.rect.p.y, 0.0 )
        self.assertEqual( self.linear_curve.rect.m.x, 2.0 )
        self.assertEqual( self.linear_curve.rect.m.y, 1.0 )

        #bezier_curve
        self.bezier_curve.create_intersect_judge_rectangle()
        self.assertEqual( self.bezier_curve.rect.q.x, 0.0 )
        self.assertEqual( self.bezier_curve.rect.q.y, 0.0 )
        self.assertEqual( self.bezier_curve.rect.z.x, 0.0 )
        self.assertEqual( self.bezier_curve.rect.z.y, 200.0 )
        self.assertEqual( self.bezier_curve.rect.p.x, 100.0 )
        self.assertEqual( self.bezier_curve.rect.p.y, 0.0 )
        self.assertEqual( self.bezier_curve.rect.m.x, 100.0 )
        self.assertEqual( self.bezier_curve.rect.m.y, 200.0 )
    #end

    def test_init_segment_set(self):
        self.assertEqual(self.linear_curve[0].s.x, 0.0)
        self.assertEqual(self.linear_curve[0].s.y, 0.0)
        self.assertEqual(self.linear_curve[0].e.x, 1.0)
        self.assertEqual(self.linear_curve[0].e.y, 1.0)

        self.assertEqual(self.linear_curve[1].s.x, 1.0)
        self.assertEqual(self.linear_curve[1].s.y, 0.0)
        self.assertEqual(self.linear_curve[1].e.x, 0.0)
        self.assertEqual(self.linear_curve[1].e.y, 1.0)
    #end

    def test_create_sequential_points(self):
        self.linear_curve.create_sequential_points()
        self.assertAlmostEqual(self.linear_curve.sequential_points[0].x, 0.0)
        self.assertAlmostEqual(self.linear_curve.sequential_points[0].y, 0.0)
        self.assertAlmostEqual(self.linear_curve.sequential_points[1].x, 1.0)
        self.assertAlmostEqual(self.linear_curve.sequential_points[1].y, 0.0)
        self.assertAlmostEqual(self.linear_curve.sequential_points[2].x, 1.0)
        self.assertAlmostEqual(self.linear_curve.sequential_points[2].y, 0.0)
        self.assertAlmostEqual(self.linear_curve.sequential_points[3].x, 2.0)
        self.assertAlmostEqual(self.linear_curve.sequential_points[3].y, 1.0)
    #end

    def test_create_edge_sequential_points(self):
        self.linear_curve.create_sequential_points()
        self.linear_curve.create_edge_sequential_points(0.5)
        self.assertAlmostEqual(self.linear_curve.start_side_sequential_points[0].x, 0.0)
        self.assertAlmostEqual(self.linear_curve.start_side_sequential_points[0].y, 0.0)
        self.assertAlmostEqual(self.linear_curve.start_side_sequential_points[1].x, 1.0)
        self.assertAlmostEqual(self.linear_curve.start_side_sequential_points[1].y, 0.0)

        self.assertAlmostEqual(self.linear_curve.end_side_sequential_points[0].x, 2.0)
        self.assertAlmostEqual(self.linear_curve.end_side_sequential_points[0].y, 1.0)
        self.assertAlmostEqual(self.linear_curve.end_side_sequential_points[1].x, 1.0)
        self.assertAlmostEqual(self.linear_curve.end_side_sequential_points[1].y, 0.0)
    #end

    def test_init_cubic_bezier_curve_set(self):
        self.assertEqual(self.bezier_curve[0].p0.x, 0.0)
        self.assertEqual(self.bezier_curve[0].p0.y, 0.0)
        self.assertEqual(self.bezier_curve[0].p1.x, 1.0)
        self.assertEqual(self.bezier_curve[0].p1.y, 2.0)
        self.assertEqual(self.bezier_curve[0].p2.x, 10.0)
        self.assertEqual(self.bezier_curve[0].p2.y, 20.0)
        self.assertEqual(self.bezier_curve[0].p3.x, 100.0)
        self.assertEqual(self.bezier_curve[0].p3.y, 200.0)
    #end

    def test_append_segment_set(self):
        p5 = Point(11.0, 22.0)
        p6 = Point(111.0, 222.0)

        linear_ctrl_p_5_6 = LinearApproximateCurveControlPoint(p5, p6)
        
        self.linear_curve.append(linear_ctrl_p_5_6)
        self.assertEqual(self.linear_curve[3].s.x, 11.0)
        self.assertEqual(self.linear_curve[3].s.y, 22.0)
        self.assertEqual(self.linear_curve[3].e.x, 111.0)
        self.assertEqual(self.linear_curve[3].e.y, 222.0)
    #end

    def test_append_cubic_bezier_curve(self):
        p0 = Point(0.0, 0.0)
        p1 = Point(1.0, 2.0)
        p4 = Point(11.0, 22.0)
        p5 = Point(111.0, 222.0)

        bezier_ctrl_p = CubicBezierCurveControlPoint(p0, p1, p4, p5)
        
        self.bezier_curve.append(bezier_ctrl_p)
        self.assertEqual(self.bezier_curve[2].p2.x, 11.0)
        self.assertEqual(self.bezier_curve[2].p2.y, 22.0)
        self.assertEqual(self.bezier_curve[2].p3.x, 111.0)
        self.assertEqual(self.bezier_curve[2].p3.y, 222.0)
    #end

    def test_iter_linear(self):
        s = ""
        for segment in self.linear_curve:
            s += str(segment)
        #end
        the_answer = "0.000 0.000\n1.000 1.000\n1.000 0.000\n0.000 1.000\n1.000 0.000\n2.000 1.000\n"
        self.assertEqual(s, the_answer)
    #end

    def test_iter_bezier(self):
        s = ""
        for curve in self.bezier_curve:
            s += str(curve)
        #end
        the_answer = "0.000 0.000\n1.000 2.000\n10.000 20.000\n100.000 200.000\n0.000 0.000\n1.000 2.000\n10.000 20.000\n100.000 200.000\n"
        self.assertEqual(s, the_answer)
    #end

    def test_linearize(self):

        # CubicBezierCurve of 90degree arc (radius=100)
        p0 = Point(100.0,                              0.0)
        p1 = Point(100.0,                              400.0*( math.sqrt(2.0) - 1.0 )/3.0)
        p2 = Point(400.0*( math.sqrt(2.0) - 1.0 )/3.0, 100.0)
        p3 = Point(0.0,                                100.0)
        ctrl_p = CubicBezierCurveControlPoint(p0, p1, p2, p3)

        curve = CubicBezierCurve()
        curve.append(ctrl_p)

        linear_approximate_curve = curve.linearize(0.1)

        origin = Point(0.0, 0.0)
        for ctrl_p in linear_approximate_curve:
            distance_from_origin = round( origin.distance(ctrl_p.s) )
            self.assertEqual(distance_from_origin, 100)
        #end
    #end

    def test_thin_smoothen(self):
        num_angle_divisions = 100
        radius = 100.0
        center = Point(0.0, 0.0)

        # LinearApproximateCurve of 0 ~ 90 degree arc ( radius=100, center=(0.0,0.0) )
        linear_approximate_curve_0_90 = test_helpers.create_arc(radius, center, 0.0, 90.0, num_angle_divisions)

        smooth_curve = linear_approximate_curve_0_90.thin_smoothen()
        ctrl_p = smooth_curve[0]

        self.assertAlmostEqual(round(ctrl_p.p0.x, 3), 100.000)
        self.assertAlmostEqual(round(ctrl_p.p0.y, 3),   0.000)
        self.assertAlmostEqual(round(ctrl_p.p1.x, 3), 101.572) 
        self.assertAlmostEqual(round(ctrl_p.p1.y, 3),  53.551) 
        self.assertAlmostEqual(round(ctrl_p.p2.x, 3),  53.551) 
        self.assertAlmostEqual(round(ctrl_p.p2.y, 3), 101.572)
        self.assertAlmostEqual(round(ctrl_p.p3.x, 3),   0.000)
        self.assertAlmostEqual(round(ctrl_p.p3.y, 3), 100.000)
    #end

    def test_broad_and_smoothen(self):
        linear_approximate_curve = LinearApproximateCurve()
        for i in range(100):
            linear_approximate_curve.append(  LinearApproximateCurveControlPoint( Point(float(i), 10.0), Point(float(i+1), 10.0) )  )
        #end

        broad_linear_curve = linear_approximate_curve.broaden(1.0)
        broad_smooth_curve = broad_linear_curve.broad_smoothen()
        the_answer = "M 0.000 10.000 C 33.333 11.658 66.667 11.658 100.000 10.000 C 66.667 8.342 33.333 8.342 0.000 10.000 Z"
        self.assertEqual(broad_smooth_curve.to_svg(), the_answer)
    #end

    def test_broaden(self):
        linear_approximate_curve = LinearApproximateCurve()
        for i in range(100):
            linear_approximate_curve.append(  LinearApproximateCurveControlPoint( Point(float(i), 10.0), Point(float(i+1), 10.0) )  )
        #end

        #broad_curve = linear_approximate_curve.broaden2(1.0, "first_last")
        broad_curve = linear_approximate_curve.broaden(1.0)
        broad_curve_svg_text = broad_curve.to_svg()
        the_answer = "M 0.000 10.000 L 1.000 10.520 L 2.000 10.540 L 3.000 10.560 L 4.000 10.580 L 5.000 10.600 L 6.000 10.620 L 7.000 10.640 L 8.000 10.660 L 9.000 10.680 L 10.000 10.700 L 11.000 10.720 L 12.000 10.740 L 13.000 10.760 L 14.000 10.780 L 15.000 10.800 L 16.000 10.820 L 17.000 10.840 L 18.000 10.860 L 19.000 10.880 L 20.000 10.900 L 21.000 10.920 L 22.000 10.940 L 23.000 10.960 L 24.000 10.980 L 25.000 11.000 L 26.000 11.020 L 27.000 11.040 L 28.000 11.060 L 29.000 11.080 L 30.000 11.100 L 31.000 11.120 L 32.000 11.140 L 33.000 11.160 L 34.000 11.180 L 35.000 11.200 L 36.000 11.220 L 37.000 11.240 L 38.000 11.260 L 39.000 11.280 L 40.000 11.300 L 41.000 11.320 L 42.000 11.340 L 43.000 11.360 L 44.000 11.380 L 45.000 11.400 L 46.000 11.420 L 47.000 11.440 L 48.000 11.460 L 49.000 11.480 L 50.000 11.500 L 51.000 11.480 L 52.000 11.460 L 53.000 11.440 L 54.000 11.420 L 55.000 11.400 L 56.000 11.380 L 57.000 11.360 L 58.000 11.340 L 59.000 11.320 L 60.000 11.300 L 61.000 11.280 L 62.000 11.260 L 63.000 11.240 L 64.000 11.220 L 65.000 11.200 L 66.000 11.180 L 67.000 11.160 L 68.000 11.140 L 69.000 11.120 L 70.000 11.100 L 71.000 11.080 L 72.000 11.060 L 73.000 11.040 L 74.000 11.020 L 75.000 11.000 L 76.000 10.980 L 77.000 10.960 L 78.000 10.940 L 79.000 10.920 L 80.000 10.900 L 81.000 10.880 L 82.000 10.860 L 83.000 10.840 L 84.000 10.820 L 85.000 10.800 L 86.000 10.780 L 87.000 10.760 L 88.000 10.740 L 89.000 10.720 L 90.000 10.700 L 91.000 10.680 L 92.000 10.660 L 93.000 10.640 L 94.000 10.620 L 95.000 10.600 L 96.000 10.580 L 97.000 10.560 L 98.000 10.540 L 99.000 10.520 L 100.000 10.000 L 99.000 9.480 L 98.000 9.460 L 97.000 9.440 L 96.000 9.420 L 95.000 9.400 L 94.000 9.380 L 93.000 9.360 L 92.000 9.340 L 91.000 9.320 L 90.000 9.300 L 89.000 9.280 L 88.000 9.260 L 87.000 9.240 L 86.000 9.220 L 85.000 9.200 L 84.000 9.180 L 83.000 9.160 L 82.000 9.140 L 81.000 9.120 L 80.000 9.100 L 79.000 9.080 L 78.000 9.060 L 77.000 9.040 L 76.000 9.020 L 75.000 9.000 L 74.000 8.980 L 73.000 8.960 L 72.000 8.940 L 71.000 8.920 L 70.000 8.900 L 69.000 8.880 L 68.000 8.860 L 67.000 8.840 L 66.000 8.820 L 65.000 8.800 L 64.000 8.780 L 63.000 8.760 L 62.000 8.740 L 61.000 8.720 L 60.000 8.700 L 59.000 8.680 L 58.000 8.660 L 57.000 8.640 L 56.000 8.620 L 55.000 8.600 L 54.000 8.580 L 53.000 8.560 L 52.000 8.540 L 51.000 8.520 L 50.000 8.500 L 49.000 8.520 L 48.000 8.540 L 47.000 8.560 L 46.000 8.580 L 45.000 8.600 L 44.000 8.620 L 43.000 8.640 L 42.000 8.660 L 41.000 8.680 L 40.000 8.700 L 39.000 8.720 L 38.000 8.740 L 37.000 8.760 L 36.000 8.780 L 35.000 8.800 L 34.000 8.820 L 33.000 8.840 L 32.000 8.860 L 31.000 8.880 L 30.000 8.900 L 29.000 8.920 L 28.000 8.940 L 27.000 8.960 L 26.000 8.980 L 25.000 9.000 L 24.000 9.020 L 23.000 9.040 L 22.000 9.060 L 21.000 9.080 L 20.000 9.100 L 19.000 9.120 L 18.000 9.140 L 17.000 9.160 L 16.000 9.180 L 15.000 9.200 L 14.000 9.220 L 13.000 9.240 L 12.000 9.260 L 11.000 9.280 L 10.000 9.300 L 9.000 9.320 L 8.000 9.340 L 7.000 9.360 L 6.000 9.380 L 5.000 9.400 L 4.000 9.420 L 3.000 9.440 L 2.000 9.460 L 1.000 9.480 Z"
        self.assertEqual(broad_curve_svg_text, the_answer)
    #end

    def test_broaden2(self):
        linear_approximate_curve = LinearApproximateCurve()
        for i in range(100):
            linear_approximate_curve.append(  LinearApproximateCurveControlPoint( Point(float(i), 10.0), Point(float(i+1), 10.0) )  )
        #end
        linear_approximate_curve2 = LinearApproximateCurve()
        for i in range(100, 200):
            linear_approximate_curve2.append(  LinearApproximateCurveControlPoint( Point(float(i), 10.0), Point(float(i+1), 10.0) )  )
        #end
        linear_approximate_curve3 = LinearApproximateCurve()
        for i in range(200, 300):
            linear_approximate_curve3.append(  LinearApproximateCurveControlPoint( Point(float(i), 10.0), Point(float(i+1), 10.0) )  )
        #end

        broad_curve = linear_approximate_curve.broaden2(1.0, "first")
        broad_curve_svg_text = broad_curve.to_svg()
        #print(broad_curve_svg_text)
        # M 0.000 10.000 L 1.000 10.520 L 2.000 10.540 L 3.000 10.560 L 4.000 10.580 L 5.000 10.600 L 6.000 10.620 L 7.000 10.640 L 8.000 10.660 L 9.000 10.680 L 10.000 10.700 L 11.000 10.720 L 12.000 10.740 L 13.000 10.760 L 14.000 10.780 L 15.000 10.800 L 16.000 10.820 L 17.000 10.840 L 18.000 10.860 L 19.000 10.880 L 20.000 10.900 L 21.000 10.920 L 22.000 10.940 L 23.000 10.960 L 24.000 10.980 L 25.000 11.000 L 26.000 11.020 L 27.000 11.040 L 28.000 11.060 L 29.000 11.080 L 30.000 11.100 L 31.000 11.120 L 32.000 11.140 L 33.000 11.160 L 34.000 11.180 L 35.000 11.200 L 36.000 11.220 L 37.000 11.240 L 38.000 11.260 L 39.000 11.280 L 40.000 11.300 L 41.000 11.320 L 42.000 11.340 L 43.000 11.360 L 44.000 11.380 L 45.000 11.400 L 46.000 11.420 L 47.000 11.440 L 48.000 11.460 L 49.000 11.480 L 50.000 11.500 L 51.000 11.500 L 52.000 11.500 L 53.000 11.500 L 54.000 11.500 L 55.000 11.500 L 56.000 11.500 L 57.000 11.500 L 58.000 11.500 L 59.000 11.500 L 60.000 11.500 L 61.000 11.500 L 62.000 11.500 L 63.000 11.500 L 64.000 11.500 L 65.000 11.500 L 66.000 11.500 L 67.000 11.500 L 68.000 11.500 L 69.000 11.500 L 70.000 11.500 L 71.000 11.500 L 72.000 11.500 L 73.000 11.500 L 74.000 11.500 L 75.000 11.500 L 76.000 11.500 L 77.000 11.500 L 78.000 11.500 L 79.000 11.500 L 80.000 11.500 L 81.000 11.500 L 82.000 11.500 L 83.000 11.500 L 84.000 11.500 L 85.000 11.500 L 86.000 11.500 L 87.000 11.500 L 88.000 11.500 L 89.000 11.500 L 90.000 11.500 L 91.000 11.500 L 92.000 11.500 L 93.000 11.500 L 94.000 11.500 L 95.000 11.500 L 96.000 11.500 L 97.000 11.500 L 98.000 11.500 L 99.000 11.500 L 100.000 10.000 L 99.000 8.500 L 98.000 8.500 L 97.000 8.500 L 96.000 8.500 L 95.000 8.500 L 94.000 8.500 L 93.000 8.500 L 92.000 8.500 L 91.000 8.500 L 90.000 8.500 L 89.000 8.500 L 88.000 8.500 L 87.000 8.500 L 86.000 8.500 L 85.000 8.500 L 84.000 8.500 L 83.000 8.500 L 82.000 8.500 L 81.000 8.500 L 80.000 8.500 L 79.000 8.500 L 78.000 8.500 L 77.000 8.500 L 76.000 8.500 L 75.000 8.500 L 74.000 8.500 L 73.000 8.500 L 72.000 8.500 L 71.000 8.500 L 70.000 8.500 L 69.000 8.500 L 68.000 8.500 L 67.000 8.500 L 66.000 8.500 L 65.000 8.500 L 64.000 8.500 L 63.000 8.500 L 62.000 8.500 L 61.000 8.500 L 60.000 8.500 L 59.000 8.500 L 58.000 8.500 L 57.000 8.500 L 56.000 8.500 L 55.000 8.500 L 54.000 8.500 L 53.000 8.500 L 52.000 8.500 L 51.000 8.500 L 50.000 8.500 L 49.000 8.520 L 48.000 8.540 L 47.000 8.560 L 46.000 8.580 L 45.000 8.600 L 44.000 8.620 L 43.000 8.640 L 42.000 8.660 L 41.000 8.680 L 40.000 8.700 L 39.000 8.720 L 38.000 8.740 L 37.000 8.760 L 36.000 8.780 L 35.000 8.800 L 34.000 8.820 L 33.000 8.840 L 32.000 8.860 L 31.000 8.880 L 30.000 8.900 L 29.000 8.920 L 28.000 8.940 L 27.000 8.960 L 26.000 8.980 L 25.000 9.000 L 24.000 9.020 L 23.000 9.040 L 22.000 9.060 L 21.000 9.080 L 20.000 9.100 L 19.000 9.120 L 18.000 9.140 L 17.000 9.160 L 16.000 9.180 L 15.000 9.200 L 14.000 9.220 L 13.000 9.240 L 12.000 9.260 L 11.000 9.280 L 10.000 9.300 L 9.000 9.320 L 8.000 9.340 L 7.000 9.360 L 6.000 9.380 L 5.000 9.400 L 4.000 9.420 L 3.000 9.440 L 2.000 9.460 L 1.000 9.480 Z
        the_answer = "M 0.000 10.000 L 1.000 10.520 L 2.000 10.540 L 3.000 10.560 L 4.000 10.580 L 5.000 10.600 L 6.000 10.620 L 7.000 10.640 L 8.000 10.660 L 9.000 10.680 L 10.000 10.700 L 11.000 10.720 L 12.000 10.740 L 13.000 10.760 L 14.000 10.780 L 15.000 10.800 L 16.000 10.820 L 17.000 10.840 L 18.000 10.860 L 19.000 10.880 L 20.000 10.900 L 21.000 10.920 L 22.000 10.940 L 23.000 10.960 L 24.000 10.980 L 25.000 11.000 L 26.000 11.020 L 27.000 11.040 L 28.000 11.060 L 29.000 11.080 L 30.000 11.100 L 31.000 11.120 L 32.000 11.140 L 33.000 11.160 L 34.000 11.180 L 35.000 11.200 L 36.000 11.220 L 37.000 11.240 L 38.000 11.260 L 39.000 11.280 L 40.000 11.300 L 41.000 11.320 L 42.000 11.340 L 43.000 11.360 L 44.000 11.380 L 45.000 11.400 L 46.000 11.420 L 47.000 11.440 L 48.000 11.460 L 49.000 11.480 L 50.000 11.500 L 51.000 11.500 L 52.000 11.500 L 53.000 11.500 L 54.000 11.500 L 55.000 11.500 L 56.000 11.500 L 57.000 11.500 L 58.000 11.500 L 59.000 11.500 L 60.000 11.500 L 61.000 11.500 L 62.000 11.500 L 63.000 11.500 L 64.000 11.500 L 65.000 11.500 L 66.000 11.500 L 67.000 11.500 L 68.000 11.500 L 69.000 11.500 L 70.000 11.500 L 71.000 11.500 L 72.000 11.500 L 73.000 11.500 L 74.000 11.500 L 75.000 11.500 L 76.000 11.500 L 77.000 11.500 L 78.000 11.500 L 79.000 11.500 L 80.000 11.500 L 81.000 11.500 L 82.000 11.500 L 83.000 11.500 L 84.000 11.500 L 85.000 11.500 L 86.000 11.500 L 87.000 11.500 L 88.000 11.500 L 89.000 11.500 L 90.000 11.500 L 91.000 11.500 L 92.000 11.500 L 93.000 11.500 L 94.000 11.500 L 95.000 11.500 L 96.000 11.500 L 97.000 11.500 L 98.000 11.500 L 99.000 11.500 L 100.000 10.000 L 99.000 8.500 L 98.000 8.500 L 97.000 8.500 L 96.000 8.500 L 95.000 8.500 L 94.000 8.500 L 93.000 8.500 L 92.000 8.500 L 91.000 8.500 L 90.000 8.500 L 89.000 8.500 L 88.000 8.500 L 87.000 8.500 L 86.000 8.500 L 85.000 8.500 L 84.000 8.500 L 83.000 8.500 L 82.000 8.500 L 81.000 8.500 L 80.000 8.500 L 79.000 8.500 L 78.000 8.500 L 77.000 8.500 L 76.000 8.500 L 75.000 8.500 L 74.000 8.500 L 73.000 8.500 L 72.000 8.500 L 71.000 8.500 L 70.000 8.500 L 69.000 8.500 L 68.000 8.500 L 67.000 8.500 L 66.000 8.500 L 65.000 8.500 L 64.000 8.500 L 63.000 8.500 L 62.000 8.500 L 61.000 8.500 L 60.000 8.500 L 59.000 8.500 L 58.000 8.500 L 57.000 8.500 L 56.000 8.500 L 55.000 8.500 L 54.000 8.500 L 53.000 8.500 L 52.000 8.500 L 51.000 8.500 L 50.000 8.500 L 49.000 8.520 L 48.000 8.540 L 47.000 8.560 L 46.000 8.580 L 45.000 8.600 L 44.000 8.620 L 43.000 8.640 L 42.000 8.660 L 41.000 8.680 L 40.000 8.700 L 39.000 8.720 L 38.000 8.740 L 37.000 8.760 L 36.000 8.780 L 35.000 8.800 L 34.000 8.820 L 33.000 8.840 L 32.000 8.860 L 31.000 8.880 L 30.000 8.900 L 29.000 8.920 L 28.000 8.940 L 27.000 8.960 L 26.000 8.980 L 25.000 9.000 L 24.000 9.020 L 23.000 9.040 L 22.000 9.060 L 21.000 9.080 L 20.000 9.100 L 19.000 9.120 L 18.000 9.140 L 17.000 9.160 L 16.000 9.180 L 15.000 9.200 L 14.000 9.220 L 13.000 9.240 L 12.000 9.260 L 11.000 9.280 L 10.000 9.300 L 9.000 9.320 L 8.000 9.340 L 7.000 9.360 L 6.000 9.380 L 5.000 9.400 L 4.000 9.420 L 3.000 9.440 L 2.000 9.460 L 1.000 9.480 Z"
        self.assertEqual(broad_curve_svg_text, the_answer)

        broad_curve2 = linear_approximate_curve2.broaden2(1.0, "middle")
        broad_curve2_svg_text = broad_curve2.to_svg()
        #print(broad_curve2_svg_text)
        the_answer2="M 100.000 10.000 L 101.000 11.500 L 102.000 11.500 L 103.000 11.500 L 104.000 11.500 L 105.000 11.500 L 106.000 11.500 L 107.000 11.500 L 108.000 11.500 L 109.000 11.500 L 110.000 11.500 L 111.000 11.500 L 112.000 11.500 L 113.000 11.500 L 114.000 11.500 L 115.000 11.500 L 116.000 11.500 L 117.000 11.500 L 118.000 11.500 L 119.000 11.500 L 120.000 11.500 L 121.000 11.500 L 122.000 11.500 L 123.000 11.500 L 124.000 11.500 L 125.000 11.500 L 126.000 11.500 L 127.000 11.500 L 128.000 11.500 L 129.000 11.500 L 130.000 11.500 L 131.000 11.500 L 132.000 11.500 L 133.000 11.500 L 134.000 11.500 L 135.000 11.500 L 136.000 11.500 L 137.000 11.500 L 138.000 11.500 L 139.000 11.500 L 140.000 11.500 L 141.000 11.500 L 142.000 11.500 L 143.000 11.500 L 144.000 11.500 L 145.000 11.500 L 146.000 11.500 L 147.000 11.500 L 148.000 11.500 L 149.000 11.500 L 150.000 11.500 L 151.000 11.500 L 152.000 11.500 L 153.000 11.500 L 154.000 11.500 L 155.000 11.500 L 156.000 11.500 L 157.000 11.500 L 158.000 11.500 L 159.000 11.500 L 160.000 11.500 L 161.000 11.500 L 162.000 11.500 L 163.000 11.500 L 164.000 11.500 L 165.000 11.500 L 166.000 11.500 L 167.000 11.500 L 168.000 11.500 L 169.000 11.500 L 170.000 11.500 L 171.000 11.500 L 172.000 11.500 L 173.000 11.500 L 174.000 11.500 L 175.000 11.500 L 176.000 11.500 L 177.000 11.500 L 178.000 11.500 L 179.000 11.500 L 180.000 11.500 L 181.000 11.500 L 182.000 11.500 L 183.000 11.500 L 184.000 11.500 L 185.000 11.500 L 186.000 11.500 L 187.000 11.500 L 188.000 11.500 L 189.000 11.500 L 190.000 11.500 L 191.000 11.500 L 192.000 11.500 L 193.000 11.500 L 194.000 11.500 L 195.000 11.500 L 196.000 11.500 L 197.000 11.500 L 198.000 11.500 L 199.000 11.500 L 200.000 10.000 L 199.000 8.500 L 198.000 8.500 L 197.000 8.500 L 196.000 8.500 L 195.000 8.500 L 194.000 8.500 L 193.000 8.500 L 192.000 8.500 L 191.000 8.500 L 190.000 8.500 L 189.000 8.500 L 188.000 8.500 L 187.000 8.500 L 186.000 8.500 L 185.000 8.500 L 184.000 8.500 L 183.000 8.500 L 182.000 8.500 L 181.000 8.500 L 180.000 8.500 L 179.000 8.500 L 178.000 8.500 L 177.000 8.500 L 176.000 8.500 L 175.000 8.500 L 174.000 8.500 L 173.000 8.500 L 172.000 8.500 L 171.000 8.500 L 170.000 8.500 L 169.000 8.500 L 168.000 8.500 L 167.000 8.500 L 166.000 8.500 L 165.000 8.500 L 164.000 8.500 L 163.000 8.500 L 162.000 8.500 L 161.000 8.500 L 160.000 8.500 L 159.000 8.500 L 158.000 8.500 L 157.000 8.500 L 156.000 8.500 L 155.000 8.500 L 154.000 8.500 L 153.000 8.500 L 152.000 8.500 L 151.000 8.500 L 150.000 8.500 L 149.000 8.500 L 148.000 8.500 L 147.000 8.500 L 146.000 8.500 L 145.000 8.500 L 144.000 8.500 L 143.000 8.500 L 142.000 8.500 L 141.000 8.500 L 140.000 8.500 L 139.000 8.500 L 138.000 8.500 L 137.000 8.500 L 136.000 8.500 L 135.000 8.500 L 134.000 8.500 L 133.000 8.500 L 132.000 8.500 L 131.000 8.500 L 130.000 8.500 L 129.000 8.500 L 128.000 8.500 L 127.000 8.500 L 126.000 8.500 L 125.000 8.500 L 124.000 8.500 L 123.000 8.500 L 122.000 8.500 L 121.000 8.500 L 120.000 8.500 L 119.000 8.500 L 118.000 8.500 L 117.000 8.500 L 116.000 8.500 L 115.000 8.500 L 114.000 8.500 L 113.000 8.500 L 112.000 8.500 L 111.000 8.500 L 110.000 8.500 L 109.000 8.500 L 108.000 8.500 L 107.000 8.500 L 106.000 8.500 L 105.000 8.500 L 104.000 8.500 L 103.000 8.500 L 102.000 8.500 L 101.000 8.500 Z"
        self.assertEqual(broad_curve2_svg_text, the_answer2)

        broad_curve3 = linear_approximate_curve3.broaden2(1.0, "last")
        broad_curve3_svg_text = broad_curve3.to_svg()
        #print(broad_curve3_svg_text)
        the_answer3="M 200.000 10.000 L 201.000 11.500 L 202.000 11.500 L 203.000 11.500 L 204.000 11.500 L 205.000 11.500 L 206.000 11.500 L 207.000 11.500 L 208.000 11.500 L 209.000 11.500 L 210.000 11.500 L 211.000 11.500 L 212.000 11.500 L 213.000 11.500 L 214.000 11.500 L 215.000 11.500 L 216.000 11.500 L 217.000 11.500 L 218.000 11.500 L 219.000 11.500 L 220.000 11.500 L 221.000 11.500 L 222.000 11.500 L 223.000 11.500 L 224.000 11.500 L 225.000 11.500 L 226.000 11.500 L 227.000 11.500 L 228.000 11.500 L 229.000 11.500 L 230.000 11.500 L 231.000 11.500 L 232.000 11.500 L 233.000 11.500 L 234.000 11.500 L 235.000 11.500 L 236.000 11.500 L 237.000 11.500 L 238.000 11.500 L 239.000 11.500 L 240.000 11.500 L 241.000 11.500 L 242.000 11.500 L 243.000 11.500 L 244.000 11.500 L 245.000 11.500 L 246.000 11.500 L 247.000 11.500 L 248.000 11.500 L 249.000 11.500 L 250.000 11.500 L 251.000 11.480 L 252.000 11.460 L 253.000 11.440 L 254.000 11.420 L 255.000 11.400 L 256.000 11.380 L 257.000 11.360 L 258.000 11.340 L 259.000 11.320 L 260.000 11.300 L 261.000 11.280 L 262.000 11.260 L 263.000 11.240 L 264.000 11.220 L 265.000 11.200 L 266.000 11.180 L 267.000 11.160 L 268.000 11.140 L 269.000 11.120 L 270.000 11.100 L 271.000 11.080 L 272.000 11.060 L 273.000 11.040 L 274.000 11.020 L 275.000 11.000 L 276.000 10.980 L 277.000 10.960 L 278.000 10.940 L 279.000 10.920 L 280.000 10.900 L 281.000 10.880 L 282.000 10.860 L 283.000 10.840 L 284.000 10.820 L 285.000 10.800 L 286.000 10.780 L 287.000 10.760 L 288.000 10.740 L 289.000 10.720 L 290.000 10.700 L 291.000 10.680 L 292.000 10.660 L 293.000 10.640 L 294.000 10.620 L 295.000 10.600 L 296.000 10.580 L 297.000 10.560 L 298.000 10.540 L 299.000 10.520 L 300.000 10.000 L 299.000 9.480 L 298.000 9.460 L 297.000 9.440 L 296.000 9.420 L 295.000 9.400 L 294.000 9.380 L 293.000 9.360 L 292.000 9.340 L 291.000 9.320 L 290.000 9.300 L 289.000 9.280 L 288.000 9.260 L 287.000 9.240 L 286.000 9.220 L 285.000 9.200 L 284.000 9.180 L 283.000 9.160 L 282.000 9.140 L 281.000 9.120 L 280.000 9.100 L 279.000 9.080 L 278.000 9.060 L 277.000 9.040 L 276.000 9.020 L 275.000 9.000 L 274.000 8.980 L 273.000 8.960 L 272.000 8.940 L 271.000 8.920 L 270.000 8.900 L 269.000 8.880 L 268.000 8.860 L 267.000 8.840 L 266.000 8.820 L 265.000 8.800 L 264.000 8.780 L 263.000 8.760 L 262.000 8.740 L 261.000 8.720 L 260.000 8.700 L 259.000 8.680 L 258.000 8.660 L 257.000 8.640 L 256.000 8.620 L 255.000 8.600 L 254.000 8.580 L 253.000 8.560 L 252.000 8.540 L 251.000 8.520 L 250.000 8.500 L 249.000 8.500 L 248.000 8.500 L 247.000 8.500 L 246.000 8.500 L 245.000 8.500 L 244.000 8.500 L 243.000 8.500 L 242.000 8.500 L 241.000 8.500 L 240.000 8.500 L 239.000 8.500 L 238.000 8.500 L 237.000 8.500 L 236.000 8.500 L 235.000 8.500 L 234.000 8.500 L 233.000 8.500 L 232.000 8.500 L 231.000 8.500 L 230.000 8.500 L 229.000 8.500 L 228.000 8.500 L 227.000 8.500 L 226.000 8.500 L 225.000 8.500 L 224.000 8.500 L 223.000 8.500 L 222.000 8.500 L 221.000 8.500 L 220.000 8.500 L 219.000 8.500 L 218.000 8.500 L 217.000 8.500 L 216.000 8.500 L 215.000 8.500 L 214.000 8.500 L 213.000 8.500 L 212.000 8.500 L 211.000 8.500 L 210.000 8.500 L 209.000 8.500 L 208.000 8.500 L 207.000 8.500 L 206.000 8.500 L 205.000 8.500 L 204.000 8.500 L 203.000 8.500 L 202.000 8.500 L 201.000 8.500 Z"
        self.assertEqual(broad_curve3_svg_text, the_answer3)

    def test_is_continuaous(self):
        num_angle_divisions = 100
        radius = 100.0
        center = Point(0.0, 0.0)

        # LinearApproximateCurve of 0 ~ 90 degree arc ( radius=100, center=(0.0,0.0) )
        linear_approximate_curve_0_90 = test_helpers.create_arc(radius, center, 0.0, 90.0, num_angle_divisions)

        # LinearApproximateCurve of 45 ~ 135 degree arc ( radius=100, center=(0.0,0.0) )
        linear_approximate_curve_45_135 = test_helpers.create_arc(radius, center, 45.0, 135.0, num_angle_divisions)

        self.assertEqual( linear_approximate_curve_0_90.is_continuaous_at_end_side(linear_approximate_curve_45_135, 0.1), True)

        self.assertEqual( linear_approximate_curve_0_90.is_continuaous_at_start_side(linear_approximate_curve_45_135, 0.1), False)

    #end



#end

if __name__ == '__main__':
    unittest.main()
#end

