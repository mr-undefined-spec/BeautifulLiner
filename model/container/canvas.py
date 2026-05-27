# model/container/canvas.py
import re
from model.container.layer import Layer

class Canvas:
    def __init__(self):
        self._layer_list: list[Layer] = []
        self._view_box = ""
        self._doc = None  # XMLドキュメント保持用
    #end def

    @property
    def doc(self):
        return self._doc
    #end def

    def set_doc(self, val):
        self._doc = val
    #end def

    @property
    def view_box(self) -> str:
        return self._view_box
    #end def

    def set_view_box(self, val: str):
        self._view_box = val
    #end def

    def get_bbox(self) -> tuple[float, float, float, float]:
        arr = re.split(r'[\s,]+', self._view_box.strip())
        return (float(arr[0]), float(arr[1]), float(arr[2]), float(arr[3]))
    #end def

    def append(self, layer: Layer):
        if not isinstance(layer, Layer):
            raise TypeError("The argument of the append method must be a Layer")
        #end if
        self._layer_list.append(layer)
    #end def

    def __getitem__(self, i: int) -> Layer:
        return self._layer_list[i]
    #end def

    def __iter__(self):
        return iter(self._layer_list)
    #end def

    def __len__(self) -> int:
        return len(self._layer_list)
    #end def

    def get_total_curve_num(self) -> int:
        total_curve_num = 0
        for layer in self._layer_list:
            total_curve_num += len(layer)  # Layer側の __len__ を利用
        #end for
        return total_curve_num
    #end def

    def clone_empty(self) -> 'Canvas':
        """自身の設定（view_boxなど）を維持した、空のCanvasを生成する"""
        cloned = Canvas()
        cloned.set_view_box(self.view_box) # 既存のプロパティをコピー
        return cloned
    #end def
#end class