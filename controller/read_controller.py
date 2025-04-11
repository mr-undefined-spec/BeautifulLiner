import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../handler'))
from read_handler import ReadHandler

from basic_controller import BasicController

class ReadController(BasicController):
    @classmethod
    def process(cls, reading_file_path):

        # initialize handlers
        read_handler = ReadHandler()

        # read
        return read_handler.process(reading_file_path)
    #end
#end
