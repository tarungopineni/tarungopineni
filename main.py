import os
import cv2
import pandas as pd
from accident_detection import detect_accident
from handdetection import initialize_models, process_frame, draw_landmarks
from firebase_ import getmail
from sendmail import send_frame_via_email
from maps import near_by_hospitals

# Paths
save_path = r"C:\Users\tarun\OneDrive\Desktop\project\saved frames"
license_path = r"C:\Users\tarun\OneDrive\Desktop\project\lisence"
hands_path = r"C:\Users\tarun\OneDrive\Desktop\project\hands_detected"
os.makedirs(save_path, exist_ok=True)
os.makedirs(license_path, exist_ok=True)
os.makedirs(hands_path, exist_ok=True)


def run_detection_pipeline(video_path, stop_check=None):
    cap = cv2.VideoCapture(video_path)
    frame_no = 1
    camera_no = 'first_camera'
    loc = (17.385044, 78.486671)

    accident_records = []

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        # ---------------- Accident Detection ----------------
        accident_detected, boxes, annotated_frame = detect_accident(frame)

        if accident_detected and boxes:
            accident_filename = os.path.join(save_path, f"frame_{frame_no}.jpg")
            if cv2.imwrite(accident_filename, annotated_frame):
                accident_records.append({
                    "Frame No": frame_no,
                    "Bounding Boxes": len(boxes),
                    "Image Saved": accident_filename
                })

            # Send alert email (optional for GUI)
            send_frame_via_email(annotated_frame, loc)

        frame_no += 1

    cap.release()
    cv2.destroyAllWindows()

    accident_df = pd.DataFrame(accident_records)

    return accident_df
