import streamlit as st
import cv2
import tempfile
import os
import time
import numpy as np
from accident_detection import AccidentDetector
from main_lane import run_detection_pipeline as run_lane_detection
from handdetection import return_frame


# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Computer Vision-Based Intelligent Road Safety System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS STYLING ---
background_css = """
<style>
.stApp {
    background-image: url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
}
.stApp > div > div > div.block-container {
    background: linear-gradient(135deg, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.6) 100%) !important;
    padding: 2rem !important;
    border-radius: 15px !important;
    margin: 1rem !important;
}
.title-text {
    color: #ffffff !important;
    text-shadow: 3px 3px 6px rgba(0,0,0,0.8) !important;
    font-family: 'Arial Black', sans-serif !important;
    font-size: 3.5rem !important;
    text-align: center !important;
    margin: 2rem 0 !important;
    padding: 1rem !important;
    background: rgba(0, 50, 100, 0.7) !important;
    border-radius: 15px !important;
    letter-spacing: 2px !important;
}
.subtitle-text {
    color: #f0f0f0 !important;
    font-size: 1.2rem !important;
    text-align: center !important;
    margin-bottom: 2rem !important;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.7) !important;
}
.section-header {
    background: linear-gradient(45deg, #007bff, #0056b3) !important;
    color: white !important;
    font-weight: bold !important;
    text-align: center !important;
    padding: 15px !important;
    border-radius: 10px !important;
    margin-bottom: 10px !important;
    font-size: 1.3rem !important;
}
.stButton > button {
    background: linear-gradient(45deg, #007bff, #0056b3) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.8rem 2rem !important;
    font-weight: bold !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0,123,255,0.3) !important;
}
.stButton > button:hover {
    background: linear-gradient(45deg, #0056b3, #007bff) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,123,255,0.4) !important;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 5px !important;
    justify-content: center !important;
    background: rgba(0,0,0,0.3) !important;
    padding: 10px !important;
    border-radius: 10px !important;
    margin-bottom: 20px !important;
}

.stTabs [data-baseweb="tab"] {
     background: rgba(255,255,255,0.1) !important;
     border: 1px solid rgba(255,255,255,0.2) !important;
     border-radius: 10px !important;
     padding: 12px 24px !important;
     color: #ffffff !important;
     font-weight: bold !important;
     font-size: 1.1rem !important;
     transition: all 0.3s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
     background: rgba(255,255,255,0.2) !important;
     transform: scale(1.05) !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
     background: linear-gradient(45deg, #ffd700, #ffed4e) !important;
     color: #000 !important;
     box-shadow: 0 4px 15px rgba(255,215,0,0.4) !important;
}
.overview-card {
    background: rgba(255, 255, 255, 0.15) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 15px !important;
    padding: 2rem !important;
    margin: 1rem 0 !important;
    color: #ffffff !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
}

.overview-card h2 {
    color: #ffd700 !important;
    text-align: center !important;
    font-size: 2rem !important;
    margin-bottom: 1rem !important;
}

.overview-card ul {
    list-style-type: none !important;
    padding: 0 !important;
}

.overview-card li {
    margin: 0.5rem 0 !important;
    padding: 0.5rem !important;
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    border-left: 4px solid #ffd700 !important;
}


</style>
"""
st.markdown(background_css, unsafe_allow_html=True)

# --- SESSION STATE ---
if "current_mode" not in st.session_state:
    st.session_state.current_mode = None

# --- STOP CHECK FUNCTION ---
def check_for_stop():
    return not st.session_state.analysis_running


# --- MAIN PAGE ---
tab1, tab2 = st.tabs(["Home", " Video Analysis"])
# --- HOME TAB ---
with tab1:
    st.markdown('<h1 class="title-text">Computer Vision-Based Intelligent Road Safety System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Enhancing Road Safety Through Advanced Computer Vision</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div class="overview-card">
            <h2> Project Overview</h2>
            <p>This cutting-edge system uses state-of-the-art computer vision techniques to monitor and prevent road hazards in real-time. By analyzing video feeds from highways and urban roads, it identifies critical safety issues to promote safer driving.</p>
            <ul>
                 <li><strong> Accident Detection:</strong> Detects collisions, sudden stops, or erratic vehicle movements using optical flow and object tracking algorithms.</li>
                <li><strong> Hand/Head Peeping Detection:</strong> Identifies distractions such as hands or heads extending out of vehicle windows, which can lead to accidents.</li>
                <li><strong> Lane Shifting Without Indicators:</strong> Monitors vehicle paths to flag unsafe lane changes without proper signaling, reducing the risk of side-swipes.</li>
            </ul>
            <p><em>Upload a video in the Analysis tab to experience the system's capabilities.</em></p>
        </div>
        """, unsafe_allow_html=True)

# --- LIVE ANALYSIS TAB ---
with tab2:
    st.markdown('<h1 class="title-text">Live Road Safety Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Upload a traffic video and watch detections in real time</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Upload and Analyze Video</h2>', unsafe_allow_html=True)
    detection_type = st.radio(
        "Choose Detection Type:",
        ["Accident Detection", "Lane Detection", "Hand Detection"],
        horizontal=True
    )

    uploaded_file = st.file_uploader(
        "Choose a video file (MP4, AVI, MOV recommended)",
        type=['mp4', 'avi', 'mov'],
        help="Upload a road or traffic video to start real-time analysis."
    )

    if uploaded_file is not None:
        video_bytes = uploaded_file.read()
        uploaded_file.seek(0)
        st.success("Video uploaded successfully")

        # Save video temporarily
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        with open(tfile.name, 'wb') as f:
            f.write(video_bytes)
        video_path = tfile.name

        # Display a preview frame
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.image(frame_rgb, caption="Sample Frame", width='stretch')
        cap.release()

        
        start_button, stop_button = st.columns(2)
        if "analysis_running" not in st.session_state:
            st.session_state.analysis_running = False

        if start_button.button (f"Start {detection_type}",width='stretch', disabled=st.session_state.analysis_running):
            st.session_state.analysis_running = True
            st.session_state.current_mode = detection_type

        if stop_button.button ("Stop Analysis",width='stretch', disabled=not st.session_state.analysis_running):
            st.session_state.analysis_running = False
            st.warning("Analysis manually stopped.")
            st.experimental_rerun()

        if st.session_state.analysis_running:
            # Placeholder for the video frame
            frame_placeholder = st.empty()
            
            # Placeholder for the warning text (separate from the video)
            warning_placeholder = st.empty()
            
            with st.spinner(f"Running real-time {detection_type} analysis..."):

                if detection_type == "Accident Detection":
                    detector = AccidentDetector()
                    cap = cv2.VideoCapture(video_path)
                    warning_placeholder.info("Accident detection running...")
                    while cap.isOpened() and st.session_state.analysis_running:
                        ret, frame = cap.read()
                        if not ret:
                            break
                        accident_detected, _, annotated = detector.detect_accident(frame)
                        
                        if accident_detected:
                            warning_placeholder.error("ACCIDENT DETECTED! IMMEDIATE HAZARD!")
                        else:
                            warning_placeholder.empty()
                        
                        frame_placeholder.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), width='stretch')
                        # time.sleep(0.03)
                    cap.release()

                elif detection_type == "Lane Detection":
                    
                    def lane_frame_callback(frame, warning_text):
                        frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), width='stretch')
                        if warning_text:
                            warning_placeholder.warning(f"LANE WARNING: {warning_text}")
                        else:
                            warning_placeholder.info("Lane detection running. Lane discipline looks good.")

                    # run_lane_detection now passes warning_text via the callback
                    run_lane_detection(video_path, stop_check=check_for_stop, frame_callback=lane_frame_callback)

                elif detection_type == "Hand Detection":
                    cap = cv2.VideoCapture(video_path)
                    warning_placeholder.info("Monitoring for distracted driving...")
                    while cap.isOpened() and st.session_state.analysis_running:
                        ret, frame = cap.read()
                        if not ret:
                            break
                        # return_frame now returns the processed frame AND a warning_text
                        processed, warning_text = return_frame(frame) 
                        
                        if warning_text:
                            warning_placeholder.error(f"DISTRACTION ALERT: {warning_text}")
                        else:
                            warning_placeholder.info("Monitoring for distracted driving. All clear.")
                            
                        frame_placeholder.image(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB), width='stretch')
                        # time.sleep(0.003)
                    cap.release()

            st.session_state.analysis_running = False
            st.session_state.current_mode = None
            st.success("Analysis completed.")
            warning_placeholder.empty()

            if st.button("Restart Analysis", use_container_width=True):
                st.session_state.analysis_running = False
                st.experimental_rerun()
    else:
        st.info("Please upload a video to start analysis.")
