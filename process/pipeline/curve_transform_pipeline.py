from model.container.canvas import Canvas
from model.container.layer import Layer
from model.primitive.curve import Curve
from process.converter.abstract_curve_list_converter import AbstractCurveListConverter
from process.pipeline.preprocess_mode import PreProcessMode
from process.pipeline.post_process_mode import PostProcessMode

class CurveTransformPipeline:
    """前処理（抽出）、幾何変換（DIされたConverter）、後処理（再配置）の一連の流れを司る
    汎用的な線画トランスフォームパイプライン。
    """
    
    def __init__(
        self, 
        preprocess_mode: PreProcessMode,
        converter: AbstractCurveListConverter, 
        post_process_mode: PostProcessMode,
        layer_name_modifier: str = ""
    ):
        """
        :param preprocess_mode: データの抽出範囲（単一線ループ / レイヤー単位 / キャンバス一括）
        :param converter: 幾何計算を担当する具象CurveListConverterインスタンス
        :param post_process_mode: 出力先の配置ポリシー（レイヤー構造維持 / 単一新規レイヤー作成）
        :param layer_name_modifier: 
            KEEP_STRUCTURE の場合は、元のレイヤー名に付与するサフィックス（例: "_trimmed"）。
            GENERATE_NEW_LAYER の場合は、新設するレイヤー名そのもの（例: "rough_fill"）。
        """
        # ─── ガードレール：あり得ない組み合わせの完全除外 ───
        if preprocess_mode == PreProcessMode.SINGLE_CURVE and post_process_mode == PostProcessMode.GENERATE_NEW_LAYER:
            raise ValueError("破綻パターン: 1本ずつのループ処理に対して『新規レイヤー統合 PostProcessMode.GENERATE_NEW_LAYER』は指定できません。")
        #end if
            
        if preprocess_mode == PreProcessMode.CANVAS_LEVEL and post_process_mode == PostProcessMode.KEEP_STRUCTURE:
            raise ValueError("破綻パターン: キャンバス全集約処理では、元のレイヤー文脈が完全に消失するため『構造維持 PostProcessMode.KEEP_STRUCTURE』は指定できません。")
        #end if

        self.preprocess_mode = preprocess_mode
        self.converter = converter
        self.post_process_mode = post_process_mode
        self.layer_name_modifier = layer_name_modifier

    def process(self, src_canvas: Canvas) -> Canvas:
        """入力Canvasを受け取り、前処理・変換・後処理を適用した新しいCanvasを出力する。"""
        dst_canvas = Canvas()
        dst_canvas.view_box = src_canvas.view_box  # ビューボックスの引き継ぎ
        
        # ─── パターンA: 【CANVAS_LEVEL】キャンバス全データ集約型 ───
        # ガードレールにより、このルートの post_process_mode は必ず GENERATE_NEW_LAYER になる
        if self.preprocess_mode == PreProcessMode.CANVAS_LEVEL:
            # 1. PreProcess: 全レイヤーから全Curveを1つのフラットなリストに集約
            all_curves = []
            for layer in src_canvas:
                for curve in layer:
                    all_curves.append(curve)
                #end for
            #end for
            
            # 2. Conversion: 純粋幾何変換（DIされたコンバーターの実行）
            output_curves = self.converter.convert(all_curves)
            
            # 3. PostProcess: 新規レイヤーを1つだけ作成して全投入
            new_layer = Layer()
            new_layer.name = self.layer_name_modifier
            new_layer.is_fill = True  # キャンバス全集約系（ラフ塗りなど）は基本「塗り」
            new_layer.color = "#FFFFFF"
            
            for curve in output_curves:
                new_layer.append(curve)
            #end for
            dst_canvas.append(new_layer)
            
            return dst_canvas
        #end if

        # ─── パターンB: 【SINGLE_CURVE / LAYER_LEVEL】レイヤー単位の走査 ───
        for src_layer in src_canvas:
            
            # 該当レイヤーに属するCurve群をリスト化
            layer_curves = [curve for curve in src_layer]
            if not layer_curves:
                continue # 空レイヤーはスキップ
            #end if
            
            processed_curves = []
            
            # 1. PreProcess & 2. Conversion
            if self.preprocess_mode == PreProcessMode.SINGLE_CURVE:
                # 黄金パターン①：1本ずつループ型
                for curve in layer_curves:
                    res = self.converter.convert([curve])
                    processed_curves.extend(res)
                #end for
            else:
                # 黄金パターン②＆③：レイヤー内全本一括型
                res = self.converter.convert(layer_curves)
                processed_curves.extend(res)
            #end if
                
            # 3. PostProcess: ポリシーに応じた配置
            if self.post_process_mode == PostProcessMode.KEEP_STRUCTURE:
                # 黄金パターン①＆②：元のレイヤー構造を維持してミラー生成
                dst_layer = Layer()
                dst_layer.name = f"{src_layer.name}{self.layer_name_modifier}"
                dst_layer.color = src_layer.color
                dst_layer.is_fill = src_layer.is_fill
                
                for curve in processed_curves:
                    dst_layer.append(curve)
                #end for
                dst_canvas.append(dst_layer)
                
            elif self.post_process_mode == PostProcessMode.GENERATE_NEW_LAYER:
                # 黄金パターン③：レイヤーごと処理して、結果は特定の独立レイヤーへ（Junctionなど）
                target_layer = None
                for existing_layer in dst_canvas:
                    if existing_layer.name == self.layer_name_modifier:
                        target_layer = existing_layer
                        break
                    #end if
                #end for
                
                if target_layer is None:
                    target_layer = Layer()
                    target_layer.name = self.layer_name_modifier
                    target_layer.color = "#FF0000"  # デフォルト赤
                    target_layer.is_fill = True
                    dst_canvas.append(target_layer)
                #end if
                
                for curve in processed_curves:
                    target_layer.append(curve)
                #end for
            #end if
        #end for

        return dst_canvas
    #end def
#end class