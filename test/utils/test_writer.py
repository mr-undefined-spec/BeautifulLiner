import os
import sys

from xml.dom import minidom

import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), '../../utils'))

import reader
import writer

import unittest

class TestSvgData(unittest.TestCase):
    def test_write(self):
        #just read
        svg_from_file = reader.create_svg_from_file("data/test.svg")
        # and just write
        writer.write(svg_from_file, "data/write.svg")

        the_answer = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<!-- Created with Inkpad (http://www.taptrix.com/) -->
<svg xmlns:inkpad="http://taptrix.com/inkpad/svg_extensions" height="1366.0pt" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" width="1024.0pt" version="1.1"  viewBox="0,0,1024,1366" >
<g id="senga" inkpad:layerName="senga">
<path d="M 402.670 127.291 C 399.823 128.714 393.001 175.251 392.271 181.822 C 386.945 229.751 389.765 292.499 404.953 338.063 C 408.446 348.544 420.484 380.166 433.613 380.166 " fill="none" opacity="1" stroke="#000000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" />
<path d="M 404.732 288.481 C 404.732 308.040 406.168 339.391 415.213 357.480 C 420.015 367.085 423.805 376.613 429.187 386.302 C 429.783 387.375 430.352 389.796 430.352 389.796 " fill="none" opacity="1" stroke="#000000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" />
</g>
</svg>'''

        with open("data/write.svg", "r") as file:
            s = file.read()
            self.assertEqual(s, the_answer)
        #end

        return 
    #end
#end

if __name__ == '__main__':
    unittest.main()
#end
