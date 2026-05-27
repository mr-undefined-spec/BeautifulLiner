# model/container/layer.py
from enum import Enum
from model.primitive.curve import Curve

class EndpointStyle(Enum):
    BOTH_POINTED = "both_pointed"
    BOTH_WIDE = "both_wide"
#end class

class Layer:
    def __init__(self, name: str, color: str):
        if not isinstance(name, str):
            raise TypeError("The 1st argument 'name' must be a str")
        #end if
        if not isinstance(color, str):
            raise TypeError("The 2nd argument 'color' must be a str")
        #end if

        self._name = name
        self._color = color
        self._curve_list: list[Curve] = []   
        self._is_fill = False
        self._endpoint_style = EndpointStyle.BOTH_POINTED
    #end def

    @property
    def name(self) -> str:
        return self._name
    #end def

    @property
    def is_fill(self) -> bool:
        return self._is_fill
    #end def

    @property
    def color(self) -> str:
        return self._color
    #end def

    @property
    def endpoint_style(self) -> EndpointStyle:
        return self._endpoint_style
    #end def

    def __getitem__(self, i: int) -> Curve:
        return self._curve_list[i]
    #end def

    def __iter__(self):
        # 組み込みリストのイテレータをそのまま返す（自前インデックス管理を撤廃）
        return iter(self._curve_list)
    #end def

    def __len__(self) -> int:
        return len(self._curve_list)
    #end def

    def append(self, curve: Curve):
        if not isinstance(curve, Curve):
            raise TypeError("The argument of the append method must be a Curve")
        #end if if
        self._curve_list.append(curve)
    #end def

    def get_curves(self) -> list[Curve]:
        return self._curve_list
    #end def

    def set_write_options(self, is_fill: bool, color: str, endpoint_style: EndpointStyle):
        if not isinstance(endpoint_style, EndpointStyle):
            raise TypeError("The argument 'endpoint_style' must be an EndpointStyle")
        #end if
        self._is_fill = is_fill
        self._color = color
        self._endpoint_style = endpoint_style
    #end def

    def clone_empty(self) -> 'Layer':
        """自身の設定（名前、色、線のスタイルなど）を維持した、空のLayerを生成する"""
        cloned = Layer(self._name, self._color)
        cloned._is_fill = self._is_fill
        cloned._endpoint_style = self._endpoint_style
        return cloned
    #end def
#end class