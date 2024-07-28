# EduVantageへようこそ
## EducationにAdvantageを
EduVantageは、教育機関向け（笑）の学習管理システム（？）です。

## 利用しているライブラリ
- `tkinter`: GUIの作成に使用
- `pandas`: データの操作と解析に使用
- `PIL`: 画像の表示に使用
- `numpy`: 数値計算に使用
- `matplotlib`: グラフの描画に使用
- `scipy`: 統計計算に使用
- `ui_loader`：UIの作成に使用
- `reportlab`: PDFの作成に使用

## 簡単な使い方
1. プロジェクトをクローンします。
    ```sh
    git clone https://github.com/yourusername/EduVantage.git
    cd EduVantage
    ```

2. 仮想環境を作成し、必要なライブラリをインストールします。
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # Windowsの場合は .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. アプリケーションを起動します。
    ```sh
    python main.py
    ```

4. CSVファイルを読み込みます。
    - 「ファイルを開く」をクリックし、CSVファイルを選択します。
    - データを編集する場合、設定から変更できます。
    - また、各課題ごとに重要度と合格点を設定してください。

5. クラス画面について
   - ドロップダウンメニューから表示したい課題を選択します。
   - 「ID順」ボタンをクリックして、生徒ごとのデータを表示します。
   - また、Report全て、Exam全てに関しては、推移を見るために「推移」ボタンもあります。
6. 設定画面について
   - 設定画面では、各課題ごとの合格点の設定、評定の設定、もとデータの編集ができます。
      - なお、評定の設定は合計の点数でしか現状できません
7. 個人画面について
   - 個人画面では、生徒ごとのデータを成績表の形で表示します。
   - 生徒ごとにコメントを保存することもできます。
   - 成績表をPDFで出力することもできます。
     