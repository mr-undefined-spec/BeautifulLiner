import os
import sys
import random


class Writer():
    @staticmethod
    def write_file(output_file_name, canvas, junction_canvas=None, fill_canvas=None):
        """
        指定された各種キャンバスを適切なレイヤー順序で1つのSVGファイルとして出力する。
        
        :param output_file_name: 出力するSVGファイルのパス
        :param canvas: 線画（主線）データが格納されたCanvas
        :param junction_canvas: 三叉路のインク溜まり（三角形ポリゴン）が格納されたCanvas（省略可能）
        :param fill_canvas: ラフ塗りデータが格納されたCanvas（省略可能）
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

        # ─── 1. ラフ塗り（fill_canvas）：最背面 ───
        if fill_canvas is not None:
            for layer in fill_canvas:
                s += '<g id="' + layer.name + '" inkpad:layerName="' + layer.name + '">\n'

                for i, curve in enumerate(layer):
                    if hasattr(curve, 'color') and curve.color is not None:
                        fill_color = curve.color
                        opacity = "1.0"
                    else:
                        r = random.randint(100, 230)
                        g = random.randint(100, 230)
                        b = random.randint(100, 230)
                        fill_color = f"rgb({r},{g},{b})"
                        opacity = "0.6"
                    #end if
                    
                    s += f'  <path stroke="none" stroke-width="1.0" fill="{fill_color}" stroke-linecap="round" opacity="{opacity}" stroke-linejoin="round" '
                    s += r' d="'
                    s += curve.to_str()
                    s += r'" />' + '\n'
                #end for
                s += '</g>\n'
            #end for
        #end if

        # ─── 2. 主線画（canvas）：中間層 ───
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

        # ─── 3. 三叉路（junction_canvas）：最前面 ───
        # ※主線の「面」の上に確実にオーバーレイさせるため、主線より後に描画します
        if junction_canvas is not None:
            for layer in junction_canvas:
                s += '<g id="' + layer.name + '" inkpad:layerName="' + layer.name + '">\n'

                for i, curve in enumerate(layer):
                    # ジャンクションは常に「塗りつぶし（面）」スタイルで出力
                    s += '  <path stroke="none" stroke-width="1.0" fill="' + layer.color + '" stroke-linecap="round" opacity="1" stroke-linejoin="round" '
                    s += r' d="'
                    s += curve.to_str()
                    s += r'" />' + '\n'
                #end for
                s += '</g>\n'
            #end for
        #end if

        # 四隅のトンボ（BOX）レイヤー
        s += '<g id="BOX" inkpad:layerName="BOX">\n'
        s += '  <path d="M -10 -10 L 10 -10 L 10 10 L -10 10 Z" opacity="1" fill="#000000"/>\n'
        s += '  <path d="M ' + str(bbox[2]-10) + ' -10 L ' + str(bbox[2]+10) + ' -10 L ' + str(bbox[2]+10) + ' 10 L ' + str(bbox[2]-10) + ' 10 Z" opacity="1" fill="#000000"/>\n'
        s += '  <path d="M ' + str(bbox[2]-10) + ' ' + str(bbox[3]-10) + ' L ' + str(bbox[2]+10) + ' ' + str(bbox[3]-10) + ' L ' + str(bbox[2]+10) + ' ' + str(bbox[3]+10) + ' Z" opacity="1" fill="#000000"/>\n'
        s += '  <path d="M -10 ' + str(bbox[3]-10) + ' L 10 ' + str(bbox[3]-10) + ' L 10 ' + str(bbox[3]+10) + ' L 10 ' + str(bbox[3]+10) + ' Z" opacity="1" fill="#000000"/>\n'
        s += '</g>\n'

        s += '</svg>'
        with open(output_file_name, mode='w', encoding='utf-8') as f:
            f.write(s)
        #end with
    #end def
#end class