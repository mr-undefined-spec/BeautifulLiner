from argparse import ArgumentParser

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'model/primitive'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'model/curve'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'model/layer'))
from linear_approximate_curve_control_point import LinearApproximateCurveControlPoint
from linear_approximate_curve import LinearApproximateCurve
from layer import Layer
from layer_set import LayerSet

sys.path.append(os.path.join(os.path.dirname(__file__), 'handler'))

from write_handler import WriteHandler

from basic_controller import BasicController

class WriteController(BasicController):
    @classmethod
    def process(cls, layer_set, output_file_name):
        # write
        WriteHandler.process(layer_set, output_file_name)
    #end
#end
