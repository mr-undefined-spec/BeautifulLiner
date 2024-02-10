import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../model'))
from point import Point
from control_point import CubicBezierCurveControlPoint
from control_point import LinearApproximateCurveControlPoint
from curve import CubicBezierCurve
from curve import LinearApproximateCurve
from layer import Layer

from svg import Svg

class Controller:
    def run(self, mode, reading_file_path, linear_approximate_length, delete_ratio, broad_width, progress_bar=None, log_text=None):
        svg = Svg(0, mode, progress_bar, log_text)
        svg.read(reading_file_path)

        once_linearized = svg.linearize(linear_approximate_length)
        once_smoothened = once_linearized.smoothen()
        
        linearized  = once_smoothened.linearize(linear_approximate_length)
        delete_edge = linearized.delete_edge(delete_ratio)
        broadened   = delete_edge.broaden(broad_width)
        smoothened  = broadened.smoothen()
        smoothened.set_write_options(is_fill=True, color="#FF0000")

        writing_file_path = reading_file_path.replace(".svg", "_BeauL.svg")
        smoothened.write(writing_file_path)
    #end
#end
