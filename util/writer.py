import os
import sys
import random


class Writer():
    @staticmethod
    def write_file(canvas, fill_canvas, output_file_name):
        """
        線画キャンバス（canvas）と塗りキャンバス（fill_canvas）を重ね合わせて
        1つのSVGファイルとして出力する。
        """
        # 基準となるキャンバスのサイズ（bbox）を取得
        bbox = canvas.get_bbox()
        s = ""
        s += '<?xml version="1.0" encoding="UTF-8"?>\n'
        s += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
        s += '\n'
        s += '<svg xmlns:inkpad="http://taptrix.com/inkpad/svg_extensions" '
        s += 'height="' + str(bbox[3]) + 'pt" '
        s += 'xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" '
        s += 'width="' + str(bbox[2]) + 'pt" version="1.1" '
        s += ' viewBox="' + canvas.view_box + '" '
        s += '>\n'

        # ─── 1. 先に fill_canvas（塗り領域）を出力して背景にする ───
        if fill_canvas is not None:
            for layer in fill_canvas:
                s += '<g id="' + layer.name + '" inkpad:layerName="' + layer.name + '">\n'

                for i, curve in enumerate(layer):
                    # 各閉領域ごとにランダムなRGB色を生成（半透明 opacity=0.6）
                    r = random.randint(100, 230)
                    g = random.randint(100, 230)
                    b = random.randint(100, 230)
                    fill_color = f"rgb({r},{g},{b})"
                    
                    # 塗りなので strokeはnone、fillに色を指定
                    s += f'  <path stroke="none" stroke-width="1.0" fill="{fill_color}" stroke-linecap="round" opacity="0.6" stroke-linejoin="round" '
                    s += r' d="'
                    s += curve.to_str()
                    s += r'" />' + '\n'
                #end for
                s += '</g>\n'
            #end for
        #end if

        # ─── 2. 後から canvas（線画・主線）を重ねて描画する ───
        for layer in canvas:
            s += '<g id="' + layer.name + '" inkpad:layerName="' + layer.name + '">\n'

            for i, curve in enumerate(layer):
                if layer.is_fill:
                    s += '  <path stroke="none" stroke-width="1.0" fill="' + layer.color + '" stroke-linecap="round" opacity="1" stroke-linejoin="round" '
                else:
                    s += '  <path stroke="' + layer.color + '" stroke-width="1.0" fill="none" stroke-linecap="round" opacity="1" stroke-linejoin="round" '
                #end if
                
                s += r' d="'
                s += curve.to_str()
                s += r'" />' + '\n'
            #end for
            s += '</g>\n'
        #end for

        # 四隅のトンボ（BOX）レイヤー
        s += '<g id="BOX" inkpad:layerName="BOX">\n'
        s += '  <path d="M -10 -10 L 10 -10 L 10 10 L -10 10 Z" opacity="1" fill="#000000"/>\n'
        s += '  <path d="M ' + str(bbox[2]-10) + ' -10 L ' + str(bbox[2]+10) + ' -10 L ' + str(bbox[2]+10) + ' 10 L ' + str(bbox[2]-10) + ' 10 Z" opacity="1" fill="#000000"/>\n'
        s += '  <path d="M ' + str(bbox[2]-10) + ' ' + str(bbox[3]-10) + ' L ' + str(bbox[2]+10) + ' ' + str(bbox[3]-10) + ' L ' + str(bbox[2]+10) + ' ' + str(bbox[3]+10) + ' L ' + str(bbox[2]-10) + ' ' + str(bbox[3]+10) + ' Z" opacity="1" fill="#000000"/>\n'
        s += '  <path d="M -10 ' + str(bbox[3]-10) + ' L 10 ' + str(bbox[3]-10) + ' L 10 ' + str(bbox[3]+10) + ' L 10 ' + str(bbox[3]+10) + ' Z" opacity="1" fill="#000000"/>\n'
        s += '</g>\n'

        s += '</svg>'
        with open(output_file_name, mode='w', encoding='utf-8') as f:
            f.write(s)
        #end with
    #end def
#end class