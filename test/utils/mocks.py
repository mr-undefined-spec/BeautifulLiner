
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../model/primitive'))
from point import Point

from unittest.mock import MagicMock

def create_mock_point(x, y):
    point = MagicMock(spec=Point, x=x, y=y)
    point.__str__.return_value = "{:.3f} {:.3f}".format( x, y )
    return point
#end

