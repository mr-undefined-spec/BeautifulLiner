from process.pipeline.canvas_pipeline import CanvasPipeline
from process.converter.delete_edge_converter import DeleteEdgeConverter
from model.container.canvas import Canvas
from model.container.layer import Layer


class DeleteEdgePipeline(CanvasPipeline):
    def __init__(self, name: str, delete_ratio: float):
        # 親クラスの初期化。converter には一旦 None（またはダミー）を渡します
        super().__init__(name, None)
        self.delete_ratio = delete_ratio

    def process(self, canvas: Canvas) -> Canvas:
        """
        キャンバス全体のレイヤーを走査し、各レイヤー内の「自分以外の線」を
        コンテキストとしてコンバータに与えながら端部を切り落とす。
        """
        output_canvas = Canvas()
        output_canvas.set_view_box(canvas.view_box)

        # ExecuteManager で計算されるステップ数用のカウント（進捗表示用）
        step_count = self._step_offset

        for layer in canvas:
            new_layer = Layer(layer.name, layer.color)
            
            # レイヤーに属するすべての曲線を取得
            all_curves_in_layer = list(layer)

            converter = DeleteEdgeConverter(
                other_curves=all_curves_in_layer, 
                delete_ratio=self.delete_ratio
            )

            for target_curve in layer:
                print(f"[{self._step_name}] Step: {step_count}")
                
                step_count += 1

                # 1対1（Curveを受け取りCurveを返す）の原則を完全に維持してコンバート
                trimmed_curve = converter.convert(target_curve)
                new_layer.append(trimmed_curve)
            #end for
            
            output_canvas.append(new_layer)
        #end for

        return output_canvas
    #end
#end class