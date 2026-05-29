from abc import ABC, abstractmethod
from model.primitive.curve import Curve

class CurveListConverterBase(ABC):
    """すべての線画トランスフォーム処理が継承すべき基底クラス。
    CanvasやLayerといったコンテナの構造には一切依存せず、純粋なCurveのリストのみを処理する。
    """
    
    @abstractmethod
    def convert(self, curves: list[Curve]) -> list[Curve]:
        """受け取ったCurveのリストに対して幾何学的な計算・変換を行い、
        新しく生成されたCurveのリストを返却する。
        """
        pass
    #end def

#end class