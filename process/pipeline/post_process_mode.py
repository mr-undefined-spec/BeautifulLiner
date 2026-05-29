from enum import Enum, auto

class PostProcessMode(Enum):
    """変換後のCurve群を、どのようにLayer構造へマッピング（配置）するかを指定するモード"""
    KEEP_STRUCTURE = auto()     # 元のレイヤー構造を引き継いだ新レイヤーにミラー配置する
    GENERATE_NEW_LAYER = auto()  # 元の構造は無視し、指定した単一の特殊レイヤーを新設して統合配置する
#end class