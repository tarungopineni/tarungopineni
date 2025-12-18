from ultralytics import YOLO
import cv2
from ocr import detect_license_plate_text
import matplotlib.pyplot as plt

def license_plate_detection(frame):
    license_plate_detector = YOLO('license_plate_detector.pt')
    license_plates = license_plate_detector(frame)[0]
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate
        license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]
        gray = cv2.cvtColor(license_plate_crop,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
        license_number = detect_license_plate_text(thresh)
        return (thresh,license_number)
