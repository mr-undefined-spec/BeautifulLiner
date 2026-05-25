# model/curve/curve.py
from abc import ABC, abstractmethod
from shapely.geometry.base import BaseGeometry

class Curve(ABC):
    @property
    @abstractmethod
    def is_broad(self) -> bool:
        """厚みがある（面表現である）かどうかのフラグ"""
        pass
    #end def

    @property
    @abstractmethod
    def shapely(self) -> BaseGeometry:
        """Shapelyの幾何オブジェクト（LineString または Polygon）を返す"""
        pass
    #end def

    @abstractmethod
    def to_str(self) -> str:
        """SVGのパスデータ文字列（M... C... / M... L...）を返す"""
        pass
    #end def
#end class