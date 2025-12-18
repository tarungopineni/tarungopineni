from ultralytics import YOLO
import cv2
import os

# Load the trained YOLO model
model = YOLO('best.pt')

def detect_accident(frame):
    global model
    class_names = model.names

    # Perform detection
    results = model(frame, conf=0.17)
    boxes = results[0].boxes
    accident_detected = False

    # Check each detected object
    if boxes is not None and len(boxes) > 0:
        for box in boxes:
            cls_id = int(box.cls[0].item())
            cls_name = class_names[cls_id]

            if cls_name.lower() == "accident":
                accident_detected = True
                break

    # Annotated frame
    annotated_frame = results[0].plot()
    return [accident_detected,boxes, annotated_frame]
