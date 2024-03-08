# BeautifulLiner
BeautifulLinerはiPadアプリの"Linearity Curve"（URL）を使って作成した線画をいい感じに綺麗にするツールです。  
フリーハンドで描いたヘロヘロ線画を、滑らかな線画に変換します。  
図  
# 使い方（まず、試したい方用：GUI版・実行形式）
## インストール方法
Releaseから最新の実行形式のBeautifulLiner（URL）をダウンロードしてください。  
図  
ZIPファイルを解凍し、BeautifulLiner.exeをダブルクリックしてください。  
以下の画面が表示されたらOKです。  
図  
## 仮線画準備
Linearity Curveを使って原画から線画を描きましょう。  
線画といっても綺麗に描く必要はありません。  
全体的にざっとなぞる程度で大丈夫です。  
また、線がはみ出るように描いてください（変換によってはみ出た部分を自動で切り取ります）  
線画の例を以下に示します。  
図  
作成した線画をSVG形式で出力してください。  
図  
SVG形式の出力ファイルをPC側に転送してください。
## 変換
BeautifulLiner上段のファイル選択より先ほどのSVGファイルを選択してください。  
図  
BeautifulLiner中段の各種パラメータを変更してください（通常はデフォルト設定のままで問題ありません）。  
図  
「実行」ボタンを押すことで変換が開始します。しばらくお待ちください。  
図  
## 修正
一発で綺麗な線画が出来ればよいのですが、残念ながら本ツールではそうはいきません。  
変換後の線画ファイルは再度Linearity Curveで開き、適宜修正してください。  
# 作成のコツ
綺麗な線画を作るためのコツを以下に示します。参考になれば幸いです。
## 複雑な曲線を避ける
変曲点が二つ以上含まれる複雑な曲線は綺麗に変換されません。  
曲線を分解し、変曲点が一つの曲線の組み合わせで描くようにしてみてください。  
図

## 曲率の大きい曲線を避ける
曲率の大きな曲線は綺麗に変換されません。  
以下図を参考に曲率の小さい曲線を描くようにしてみてください。  
図  

## はみ出た部分の切り取りを調整する
はみ出した端部の切り取りは自動で行われますが、上手く調整しないと適切に切り取りができない場合があります。  
特に髪の毛を描く際などに顕著にこの傾向が出ます。  
図  
この場合、元の線画を描くときに以下図のような工夫を加えてください。  
図  

# 使い方（じっくり使いたい方：CUI版・python）
## 環境構築方法
ローカル環境にgit cloneしてください。  
コマンド  
BeautifulLinerディレクトリへ移動し、requirement.txtでライブラリを一括インストールしてください。  
コマンド  
## 実行方法
コマンドライン第一引数に対象のSVGファイルを指定してください。  
コマンド  
以下のオプションが使えます。  

# アルゴリズムの解説
URL

# For Linearity Curve Developers
I love Linearity Curve. This application and algorithm is open (MIT License). So, please add this application to Linearity Curve.  
As a reward, a perpetual license to Linearity Curve would suffice for me (just kidding, of course).