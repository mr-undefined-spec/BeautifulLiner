from model.container.canvas import Canvas
from process.converter.converter_base import ConverterBase

class CanvasPipeline:
    def __init__(self, step_name: str, converter: ConverterBase):
        self._step_name = step_name
        self._converter = converter
        self._step_offset = 0

    def set_step_offset(self, offset: int):
        self._step_offset = offset

    def process(self, canvas: Canvas) -> Canvas:
        # 1. メタデータを引き継いだ空のCanvasを生成
        new_canvas = canvas.clone_empty()
        step_count = self._step_offset
        
        # 2. すべてのパイプラインで共通の3重ループ
        for layer in canvas:
            new_layer = layer.clone_empty()
            
            for curve in layer:
                # ログ出力用のステップ名も動的に対応
                print(f"[{self._step_name}] Step: {step_count}")
                step_count += 1
                
                # 注入されたコンバータで1対1変換
                processed_curve = self._converter.convert(curve)
                new_layer.append(processed_curve)
            # end for
                
            new_canvas.append(new_layer)
        # end for
            
        return new_canvas
# end class