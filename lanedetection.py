import cv2
import numpy as np
from ultralytics import YOLO

class LaneDetector:
    def __init__(self, model_path=r"C:\Users\LENOVO\OneDrive\Desktop\PYTHON\CV PROJECT\lane.pt"):
        """
        model_path: YOLO model that proposes lane/road-marking regions. Replace with a local path.
        """
        self.model = YOLO(model_path)

    def detect(self, frame):
        """
        Detect lanes and draw line segments.

        Returns:
            frame_out: frame with lane segments drawn
            lane_change: bool (placeholder False)
        """
        frame_out = frame.copy()
        results = self.model(frame_out)[0]
        lane_change = False 
         # TODO: implement per-vehicle lane assignment & crossing detection
            

        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            x1 = max(0, x1); y1 = max(0, y1)
            x2 = min(frame_out.shape[1]-1, x2); y2 = min(frame_out.shape[0]-1, y2)
            if x2 <= x1 or y2 <= y1:
                continue

            roi = frame_out[y1:y2, x1:x2]
            if roi.size == 0:
                continue

            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blurred, 70, 150)
            lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50,
                                    minLineLength=30, maxLineGap=10)
            if lines is not None:
                for line in lines:
                    lx1, ly1, lx2, ly2 = line[0]
                    angle = np.degrees(np.arctan2((ly2 - ly1), (lx2 - lx1)))
                    # keep roughly diagonal lines typical of lanes in ROI
                    if abs(angle) < 40 or abs(angle) > 160:
                        continue
                    cv2.line(frame_out, (x1 + lx1, y1 + ly1), (x1 + lx2, y1 + ly2), (0, 200, 0),2)

        return frame_out, lane_change
