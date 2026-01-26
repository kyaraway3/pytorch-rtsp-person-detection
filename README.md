システム構成
RTSP Camera
     ↓
 OpenCV (RTSP Capture)
     ↓
 PyTorch (Person Detection)
     ↓
 Recorder (MP4保存)

ディレクトリ構成
project/
├─ app/
│  ├─ main.py        # アプリ全体制御（エントリーポイント）
│  ├─ rtsp.py        # RTSP 接続管理
│  ├─ detector.py    # 人物検知ロジック（PyTorch）
│  └─ recorder.py    # 録画制御（開始・停止・保存）
│
├─ records/          # 録画ファイル保存先
├─ .env              # RTSP 接続情報
├─ requirements.txt
└─ README.md

| 項目     | 内容                    |
| ------ | --------------------- |
| OS     | Windows 10 / 11       |
| Python | 3.10                  |
| GPU    | NVIDIA GPU（CUDA対応）※任意 |
| Camera | RTSP対応カメラ             |


使用技術
# Python 3.10

# OpenCV（NumPy 2.x を要求しない最後の世代）
opencv-python-headless==4.8.1.78

# NumPy（PyTorch / OpenCV 両対応の最終安定）
numpy==1.26.4

# PyTorch（CUDA 11.8 固定）
torch==2.1.2+cu118
torchvision==0.16.2+cu118
--extra-index-url https://download.pytorch.org/whl/cu118

# python-dotenv

# RTSP (FFmpeg backend)


セットアップ
仮想環境作成
python -m venv venv
venv\Scripts\activate

依存ライブラリインストール

.env 設定
RTSP_URL=rtsp://xxx.xxx.xxx.xxx:1945/live

実行方法（appをパッケージとして）
python -m app.main

⚠Docker 化について
本システムは当初、Docker 化を検討していましたが、
Python パッケージ依存関係の解決問題により、現時点では Docker 化を見送っています。

背景
本システムでは以下の構成を前提としています。

PyTorch（CUDA 対応）
OpenCV（RTSP 入力・動画処理）
NumPy 1.26.4（PyTorch 2.1 系と互換性あり）

しかし、opencv-python / opencv-python-headless パッケージは
NumPy の上限バージョンを依存関係として明示していません。

その結果、Docker 環境（pip / conda）では依存解決時に以下の挙動が発生します。

NumPy 2.x（最新） が自動的に選択される
numpy==1.26.4 を明示指定しても、
OpenCV の再インストール時に NumPy 2.x が再度引き込まれる
PyTorch（2.1 系）が NumPy 2.x と非互換 のため実行時エラーが発生

発生する問題の例

pip install -r requirements.txt 実行後に NumPy が 2.x に上書きされる
opencv-python インストール時に NumPy が自動ダウングレード／アップグレードされる
コンテナ起動後に PyTorch 実行時エラー（Segmentation Fault / RuntimeError）

対応方針

以下の理由から、現時点では Docker 化を断念し、venv（ローカル仮想環境）での運用を採用しています。

NumPy / OpenCV / PyTorch のバージョン整合性を確実に保つため
GPU（CUDA）環境での安定動作を最優先するため
実運用での再現性・デバッグ性を重視したため

今後について

OpenCV 側で NumPy 2.x との互換性が明確化される

PyTorch が NumPy 2.x を正式サポートする

これが満たされた段階で、
Docker 化を再検討する余地があります。

⚠ 本システムはリアルタイムGPU推論を行うため、
推論頻度・解像度・GPUメモリ管理を誤ると
GPUクラッシュやシステムフリーズが発生します。
これを避けるため、
推論間引き・no_grad・eval・RTSPバッファ制御を入れています