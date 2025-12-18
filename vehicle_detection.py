import cv2
from ultralytics import YOLO

class VehicleDetector:
    def __init__(self, model_path="yolov8n.pt"):
        # Load YOLO model once
        self.model = YOLO(model_path)
        # COCO vehicle classes: 2=car, 3=motorcycle, 5=bus, 7=truck
        self.vehicle_classes = [2, 3, 5, 7]

    def is_vehicle(self, class_id):
        return class_id in self.vehicle_classes

    def detect(self, frame):
        """
        Detects vehicles in the frame.
        Returns:
            vehicles (list): list of bounding boxes [x, y, w, h]
        """
        results = self.model(frame)[0]
        vehicles = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            if self.is_vehicle(cls_id):
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                label = f"{self.model.names[cls_id]} {conf:.2f}"

                # Collect vehicles for main.py
                vehicles.append([x1, y1, x2 - x1, y2 - y1])

                # Draw box + label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return vehicles
