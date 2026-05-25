# test/util/test_reader.py
import unittest
import os
from util.reader import Reader

class TestReader(unittest.TestCase):
    def test_read(self):
        # プロジェクトルート基準でスマートにパスを指定
        svg_path = os.path.join("data", "test.svg")
        self.canvas = Reader.create_canvas_from_file(svg_path)

        # 座標アサーションの際、浮動小数点の微小な誤差で落ちないよう assertAlmostEqual を使うか、
        # あるいは単純なリスト比較にする場合は round 処理された値と比較する
        the_answer =  [(402.67, 127.291), (399.823, 128.714), (393.001, 175.251), (392.271, 181.822), (386.945, 229.751), (389.765, 292.499), (404.953, 338.063), (408.446, 348.544), (420.484, 380.166), (433.613, 380.166), (404.732, 288.481), (404.732, 308.04), (406.168, 339.391), (415.213, 357.48), (420.015, 367.085), (423.805, 376.613), (429.187, 386.302), (429.783, 387.375), (430.352, 389.796)]

        the_answer_index = 0

        for layer in self.canvas:
            for curve in layer:
                for point in curve.points:
                    # 浮動小数点の比較は、厳密一致より delta（許容誤差）を指定するとさらに堅牢になります
                    self.assertAlmostEqual(point.x, the_answer[the_answer_index][0], places=3)
                    self.assertAlmostEqual(point.y, the_answer[the_answer_index][1], places=3)
                    the_answer_index += 1
                #end for
            #end for
        #end for
        
        self.assertEqual(the_answer_index, len(the_answer))
    #end def
#end class

if __name__ == '__main__':
    unittest.main()
#end if