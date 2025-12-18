import cv2
import time
import pandas as pd
from lanedetection import LaneDetector
from vehicle_detection import VehicleDetector
from indicatordetection import IndicatorDetector

def run_detection_pipeline(video_path, stop_check=lambda: False, frame_callback=None):
    lane_detector = LaneDetector(
        model_path=r"C:\Users\LENOVO\OneDrive\Desktop\PYTHON\CV PROJECT\lane.pt"
    )
    vehicle_detector = VehicleDetector()
    indicator_detector = IndicatorDetector(use_external_boxes=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video source: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    prev_lane_center = None
    lane_shift_warning = False
    warning_text = ""

    while True:
        if stop_check():
            print("Analysis stopped by user.")
            break

        ret, frame = cap.read()
        if not ret:
            break

        # ---- Run detections ----
        frame_lanes, lane_center = lane_detector.detect(frame)
        vehicles = vehicle_detector.detect(frame_lanes)
        indicators, indicator_status = indicator_detector.detect(frame_lanes, vehicles)

        # ---- Lane shift detection ----
        if prev_lane_center is not None and lane_center is not None:
            shift = abs(lane_center - prev_lane_center)

            # You can tune this threshold based on your video width
            if shift > 50:  # <-- adjust if needed (e.g. 40–80 pixels)
                if not indicator_status:  # no indicator detected
                    lane_shift_warning = True
                    warning_text = "Lane Shift Detected Without Indicator!"
                else:
                    lane_shift_warning = False
                    warning_text = ""
            else:
                lane_shift_warning = False
                warning_text = ""

        prev_lane_center = lane_center

        # ---- Overlay indicators ----
        if vehicles:
            for (x, y, w, h) in vehicles:
                cv2.rectangle(frame_lanes, (x, y), (x + w, y + h), (255, 0, 0), 2)

        if lane_shift_warning:
            cv2.putText(
                frame_lanes,
                warning_text,
                (15, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                3,
            )

        # ---- Display frame via callback (for Streamlit) ----
        if frame_callback:
            frame_callback(frame_lanes,warning_text)
        cv2.imshow("Detection Pipeline", frame_lanes)

    cap.release()
    return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
