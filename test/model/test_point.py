
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))
from point import Point

import unittest

class TestPoint(unittest.TestCase):
    def test(self):
        self.p = Point(1.2, 2.4)
        self.assertAlmostEqual(self.p.x, 1.2)
        self.assertAlmostEqual(self.p.y, 2.4)
        self.assertEqual(str(self.p), "1.200,2.400")
    #end

    def test_errorRaise(self):
        with self.assertRaises(TypeError) as e:
            error = Point(None, None)
        #end with
        self.assertEqual(e.exception.args[0], 'float() argument must be a string or a number, not \'NoneType\'')
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end
