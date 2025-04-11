import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../handler'))
from write_handler import WriteHandler

from basic_controller import BasicController

class WriteController(BasicController):
    @classmethod
    def process(cls, layer_set, output_file_name):
        # write
        WriteHandler.process(layer_set, output_file_name)
    #end
#end
