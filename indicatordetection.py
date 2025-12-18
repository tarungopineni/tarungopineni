import cv2
import numpy as np
from ultralytics import YOLO

class IndicatorDetector:
    def __init__(self,
                 model_path="yolov8n.pt",
                 conf_thresh=0.5,
                 vehicle_class_ids=(2, 3, 5, 7),  # car, motorbike, bus, truck
                 hsv_lower=(15, 70, 130),         # amber/indicator lower HSV (tune as needed)
                 hsv_upper=(35, 255, 255),        # amber/indicator upper HSV
                 pixel_thresh=50,                 # min yellow pixels per side to count as ON
                 use_external_boxes=True):
        self.model = YOLO(model_path)
        self.conf_thresh = float(conf_thresh)
        self.vehicle_class_ids = set(vehicle_class_ids)
        self.lower = np.array(hsv_lower, dtype=np.uint8)
        self.upper = np.array(hsv_upper, dtype=np.uint8)
        self.pixel_thresh = int(pixel_thresh)
        self.use_external_boxes = bool(use_external_boxes)

    def _detect_indicator_in_roi(self, roi):
        if roi is None or roi.size == 0:
            return "none"
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower, self.upper)

        h, w = mask.shape[:2]
        # For robustness, could focus on lower band: mask[int(h*0.6):, :]
        left_mask = mask[:, :w // 2]
        right_mask = mask[:, w // 2:]

        left_on = cv2.countNonZero(left_mask) > self.pixel_thresh
        right_on = cv2.countNonZero(right_mask) > self.pixel_thresh

        if left_on and right_on:
            return "both"
        if left_on:
            return "left"
        if right_on:
            return "right"
        return "none"

    def detect(self, frame, vehicles=None):
        """
        Args:
            frame: BGR frame
            vehicles: list of [x,y,w,h]; if None or use_external_boxes=False, YOLO is used.

        Returns:
            indicators: dict {id: "left"|"right"|"both"|"none"}
            boxes_xywh: list of [x,y,w,h] used for detection
        """
        h_img, w_img = frame.shape[:2]
        boxes_xywh = []

        if self.use_external_boxes and vehicles:
            for (x, y, w, h) in vehicles:
                x1 = max(0, int(x)); y1 = max(0, int(y))
                x2 = min(w_img - 1, int(x + w)); y2 = min(h_img - 1, int(y + h))
                if x2 <= x1 or y2 <= y1:
                    continue
                boxes_xywh.append([x1, y1, x2 - x1, y2 - y1])
        else:
            yres = self.model(frame)[0]
            for box in yres.boxes:
                cls = int(box.cls[0]); conf = float(box.conf[0])
                if cls in self.vehicle_class_ids and conf >= self.conf_thresh:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    x1 = max(0, x1); y1 = max(0, y1)
                    x2 = min(w_img - 1, x2); y2 = min(h_img - 1, y2)
                    if x2 <= x1 or y2 <= y1:
                        continue
                    boxes_xywh.append([x1, y1, x2 - x1, y2 - y1])

        indicators = {}
        for v_id, (x, y, w, h) in enumerate(boxes_xywh):
            roi = frame[y:y + h, x:x + w]
            status = self._detect_indicator_in_roi(roi)
            indicators[v_id] = status
            # Overlay tag (optional)
            color = (0,255,255) if status != "none" else (0, 255, 0)
            cv2.putText(frame, f"Ind: {status}", (x, y + h + 18),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return indicators, boxes_xywh
