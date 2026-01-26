# app/rtsp.py
import cv2

def open_rtsp(rtsp_url: str):
    cap = cv2.VideoCapture(
        f"{rtsp_url}?rtsp_transport=tcp",
        cv2.CAP_FFMPEG
    )
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        raise RuntimeError("RTSP stream could not be opened")

    print("RTSP opened successfully")
    return cap
