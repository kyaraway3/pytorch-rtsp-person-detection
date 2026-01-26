"""
recorder.py
-------------------------------------------------
人物検知をトリガーに録画を開始・停止するクラス
- 検知 → 録画開始
- 一定時間未検知 → 録画停止
-------------------------------------------------
"""

import cv2
from datetime import datetime
from pathlib import Path
import time

class Recorder:
    def __init__(self, save_dir: Path, fps=20, stop_after_sec=10):
        self.save_dir = save_dir
        self.save_dir.mkdir(exist_ok=True)

        self.fps = fps
        self.stop_after_sec = stop_after_sec

        self.writer = None
        self.recording = False

        self.last_detected_time = None

    def start(self, frame):
        h, w = frame.shape[:2]
        filename = self.save_dir / f"person_{datetime.now():%Y%m%d_%H%M%S}.mp4"

        self.writer = cv2.VideoWriter(
            str(filename),
            cv2.VideoWriter_fourcc(*"mp4v"),
            self.fps,
            (w, h)
        )

        self.recording = True
        self.last_detected_time = time.time()
        print(f"Start recording: {filename}")

    def stop(self):
        if self.writer:
            self.writer.release()

        self.writer = None
        self.recording = False
        self.last_detected_time = None
        print("Recording stopped")

    def update(self, frame, detected):
        now = time.time()

        """
        毎フレーム呼ばれる更新関数
        detected=True の間は録画を継続
        """
        # 人物検知された
        if detected:
            if not self.recording:
                self.start(frame)
            self.last_detected_time = now

        # 録画中ならフレーム書き込み
        if self.recording:
            self.writer.write(frame)

            # 一定時間検知されなければ停止
            if (
                self.last_detected_time is not None
                and now - self.last_detected_time >= self.stop_after_sec
            ):
                self.stop()
