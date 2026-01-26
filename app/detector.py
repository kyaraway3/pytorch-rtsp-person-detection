"""
detector.py
-------------------------------------------------
PyTorch人物検知モジュール
- 入力: BGRフレーム
- 出力: 検知有無, 描画済みフレーム
-------------------------------------------------
"""
import torch
from torchvision import models, transforms
import cv2


"""
device: 'cpu' or 'cuda'
threshold: 人物と判定する信頼度
"""

class PersonDetector:
    def __init__(self, device: str, threshold: float):
        self.device = device
        self.threshold = threshold

        self.model = models.detection.fasterrcnn_resnet50_fpn(
            weights="DEFAULT"
        )
        self.model.to(device)
        self.model.eval()

        self.transform = transforms.ToTensor()

    def detect(self, frame):
        input_tensor = self.transform(frame).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(input_tensor)[0]

        detected = False

        for box, label, score in zip(
            outputs["boxes"],
            outputs["labels"],
            outputs["scores"]
        ):
            if label == 1 and score >= self.threshold:
                detected = True
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"Person {score:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        return detected, frame
