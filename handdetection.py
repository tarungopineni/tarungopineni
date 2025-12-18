# handetection.py
import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
from firebase_ import getdata
# Initialize mediapipe solutions
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_safety_email(sender_email, sender_password, recipient_email):
    subject = "⚠️ Safety Alert: Please Keep Your Hands Inside the Car"
    body = """
    Dear Passenger,

    We’ve detected that your hands are outside the car window.
    For your safety, please keep your hands inside the vehicle at all times while it is moving.

    Stay safe and enjoy your journey!

    Best regards,  
    Road Safety Monitoring System
    """

    # Create email structure
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Send email through Gmail SMTP
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Encrypt connection
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"✅ Safety email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")


def initialize_models():
    pose = mp_pose.Pose()
    hands = mp_hands.Hands()
    face = mp_face.FaceMesh()
    return pose, hands, face

def process_frame(frame, pose, hands, face):
    frame = cv2.resize(frame, (320, 240))
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    pose_res = pose.process(rgb)
    hands_res = hands.process(rgb)
    face_res = face.process(rgb)

    return frame, pose_res, hands_res, face_res

def draw_landmarks(frame, pose_res, hands_res, face_res):
    if pose_res.pose_landmarks:
        mp_drawing.draw_landmarks(frame, pose_res.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    if hands_res.multi_hand_landmarks:
        for lm in hands_res.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
    if face_res.multi_face_landmarks:
        for lm in face_res.multi_face_landmarks:
            mp_drawing.draw_landmarks(frame, lm, mp_face.FACEMESH_TESSELATION)
    return frame

def return_frame(frame):
    """
    Processes the frame for hand/pose detection and returns the processed frame
    and a warning message if hands are detected (indicating possible distraction).
    """
    pose, hands, face = initialize_models()
    frame, pose_res, hands_res, face_res = process_frame(frame, pose, hands, face)

    # Check for hands detected (proxy for hand/head peeping distraction)
    hand_detected = hands_res.multi_hand_landmarks is not None
    warning_text = "Hand detected: Distracted Driving!" if hand_detected else ""

    frame = draw_landmarks(frame, pose_res, hands_res, face_res)
    
    # Overlay warning text on frame for visibility
    if warning_text:
        cv2.putText(frame, "HAND DETECTED!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    sender_email = "tarungopineni@gmail.com"
    sender_password = "zvgz tmkp bttg cxib"
    recipient_email = getdata()
    send_safety_email(sender_email, sender_password, recipient_email)

    return frame, warning_text
