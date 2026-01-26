"""
main.py
-------------------------------------------------
RTSP映像を取得し、
- 一定間隔で人物検知
- 人物検知をトリガーに録画
を行うメイン制御スクリプト
-------------------------------------------------
"""
from pathlib import Path
import cv2
import torch
from dotenv import load_dotenv
import os

from app.rtsp import open_rtsp
from app.detector import PersonDetector
from app.recorder import Recorder


# ===== 設定 =====
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
RECORD_DIR = BASE_DIR / "records"

CONF_THRESHOLD = 0.6
PROCESS_EVERY_N_FRAMES = 5

#.env読み込み
load_dotenv(ENV_PATH, override=True)
RTSP_URL = os.getenv("RTSP_URL")
if not RTSP_URL:
    raise RuntimeError("RTSP_URL is not set")

"""初期化フェーズ"""
#RTSP 接続 =====
cap = open_rtsp(RTSP_URL)

#Device判定GPUが使えないPCはCPUで
device = "cuda" if torch.cuda.is_available() else "cpu"
print("device:", device)

#Detector 
#人物検知器 
detector = PersonDetector(device, CONF_THRESHOLD)

#Recorder
#録画管理
recorder = Recorder(RECORD_DIR, fps=20, stop_after_sec=10)

"""メインループ"""
frame_count = 0
print("Start monitoring...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("frame not received")
        break

    frame_count += 1
    detected = False
# --- 人物検知（間引き） ---
    if frame_count % PROCESS_EVERY_N_FRAMES == 0:
        detected, frame = detector.detect(frame)
# --- 録画制御 ---
    recorder.update(frame, detected)
# --- 表示 ---
    cv2.imshow("Person Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
