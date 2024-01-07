
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../model'))
from svg_data import SvgData

import unittest

class TestSvgData(unittest.TestCase):
    def setUp(self):
        self.data = SvgData("data/test.svg")
    #end

    def test_get_group_paths_tuple(self):
#        g_and_ps = self.data.get_group_paths_tuple()
        for group_paths_set in self.data.get_group_paths_tuple():
            group = group_paths_set[0]
            paths = group_paths_set[1]
            self.assertEqual(group.getAttributeNode('id').nodeValue, 'senga')
            self.assertEqual(paths[0].getAttributeNode('d').nodeValue, 'M532.031 499.344L531.844 499.438C532.649 500.227 533.803 501.251 534.688 502.094C533.871 501.215 532.761 500.17 532.031 499.344ZM534.688 502.094C555.617 524.626 604.021 563.031 653.625 555.281C653.826 555.221 654.089 555.187 654.281 555.125C654.289 555.102 654.286 555.069 654.312 555.062C654.4 555.04 654.467 555.01 654.562 554.969C654.884 554.829 655.271 554.459 655.656 554.125C605.701 561.662 557.416 523.748 534.688 502.094Z')
    #end

    def test_raise_error_with_set_file_name_as_int(self):

        with self.assertRaises(ValueError) as e:
            error = SvgData(1)
        #end with
        self.assertEqual(e.exception.args[0], 'file_name must be str')
    #end

#end

if __name__ == '__main__':
    unittest.main()
#end
