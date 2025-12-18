<p align="center">
  <img src="images/logo.jpg" alt="Project Logo" width="150" height="150"/>
  <h1 align="center">Computer Vision-Based Intelligent Road Safety System</h1>
</p>



---

## Table of Contents
- [Introduction](#introduction) <br>
- [Abstract](#abstract) <br>
- [Requirements](#requirements) <br>
- [Installation and Usage](#installation-and-usage) <br>
- [How It Works](#how-it-works) <br>
- [Preview](#preview) <br>
- [Team](#team-details) <br>
- [Contribution](#contribution) <br>
- [Improvements](#improvements)

---

## Introduction
<p align="left">
With the rapid increase in vehicle density and high-speed travel on highways like the Outer Ring Road (ORR), road accidents and safety violations have become a growing concern. Traditional monitoring systems often rely heavily on human supervision, which can delay response times and overlook critical incidents.  
To address these challenges, this project leverages the power of <b>computer vision</b> and <b>artificial intelligence</b> to create an automated system capable of real-time surveillance and safety analysis using existing CCTV infrastructure. By detecting accidents, rash driving, unsafe passenger behavior, and other anomalies, the system aims to bridge the gap between surveillance and active intervention, ultimately saving lives and enhancing road safety management.
</p>


## Abstract
<p align="left">
The <b>Intelligent Road Safety System</b> is designed to enhance safety measures on the <b>Outer Ring Road (ORR)</b> using advanced computer vision and artificial intelligence. By leveraging existing <b>CCTV camera networks</b>, the system performs <b>real-time monitoring</b> and provides <b>automated responses</b> to critical safety incidents.  
<br><br>
Key features include:
<ul>
  <li><b>Accident Detection:</b> Continuous CCTV surveillance detects accidents and automatically alerts emergency services for rapid response.</li>
  <li><b>Rash Driving Detection:</b> Identifies abrupt lane changes, and erratic vehicle behavior to trigger warnings or generate safety alerts.</li>
  <li><b>Passenger Safety Monitoring:</b> Detects unsafe passenger behavior such as hands outside windows or clothing caught in doors, displaying safety alerts in real time.</li>
</ul>
By integrating <b>AI-powered visual monitoring</b> with <b>automated alert systems</b>, the solution strengthens traffic surveillance, boosts emergency responsiveness, and reduces road-related risks on major expressways like ORR.
</p>

---

## Requirements
|||
|--|--|
| Python | [3.10 or later](https://www.python.org/downloads/) |
| OpenCV | [4.9.0](https://pypi.org/project/opencv-python/) |
| NumPy | [1.26.4](https://numpy.org/) |
| Ultralytics YOLO | [8.0+](https://github.com/ultralytics/ultralytics) |
| EasyOCR | [1.7.1](https://github.com/JaidedAI/EasyOCR) |
| MediaPipe | [0.10.9](https://developers.google.com/mediapipe) |
| Streamlit | [1.32.0](https://streamlit.io/) |

---

## Installation and Usage

### Step 1: Clone the repository
```bash
https://github.com/AAC-Open-Source-Pool/Computer-Vision-Based-Intelligent-Road-Safety-System.git
```

### Step 2: Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # For Linux/Mac
venv\Scripts\activate         # For Windows
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the project
For terminal:
```bash
python main.py
```

For Streamlit interface:
```bash
streamlit run gui.py
```

---

## How It Works
1. **Live CCTV Feed Integration** – The system connects to existing camera networks for continuous road monitoring.  
2. **Object and Vehicle Detection** – YOLOv8 identifies vehicles, people, and potential hazards in real time.  
3. **Rash Driving Recognition** – Detects overspeeding, abrupt lane switching, and erratic movement patterns.  
4. **Accident Detection** – Flags collisions and triggers automated alerts to relevant authorities.    
5. **Passenger Behavior Analysis** – Uses MediaPipe-based pose and gesture detection to identify unsafe passenger actions.
6. **Automated Hospital Alert and Response System** – Once an accident is detected, the system automatically identifies nearby hospitals using their registered location data. Mails and real-time alerts are sent instantly through the connected hospital management website. Hospitals receive detailed information about the incident and can accept or deny the emergency case directly through their dashboard. This feature helps automate the emergency response chain, reducing manual delays and ensuring timely medical assistance. 

---

## Preview
Screenshots of the system in action<br>
<img src="https://github.com/AAC-Open-Source-Pool/25AACR08/blob/main/images/lane.png">
<img src="https://github.com/AAC-Open-Source-Pool/25AACR08/blob/main/images/hand.jpg"> 
<img src="https://github.com/AAC-Open-Source-Pool/25AACR08/blob/main/images/accident.jpg">
<img src="https://github.com/AAC-Open-Source-Pool/25AACR08/blob/main/images/hospital website.png">
<img src="https://github.com/AAC-Open-Source-Pool/25AACR08/blob/main/images/streamlit 1.png">
<img src="https://github.com/AAC-Open-Source-Pool/25AACR08/blob/main/images/streamlit 2.png">
<img src="https://github.com/AAC-Open-Source-Pool/25AACR08/blob/main/images/streamlit 3.png">
<img src="https://github.com/AAC-Open-Source-Pool/25AACR08/blob/main/images/streamlit 4.png">

---

## Team Details
<b>Team Number: </b><p>25AACR08</p>
<b>Senior Mentor:</b><p>Meghana</p>
<b>Junior Mentor:</b><p>Dwarak</p>
<b>Team Member 1:</b><p>M.Charan Tej</p>
<b>Team Member 2:</b><p>G.Lakshmi Sai Tarun</p>
<b>Team Member 2:</b><p>B.Charan Reddy</p>
 
## Contribution 
**This section provides instructions and details on how to submit a contribution via a pull request. It is important to follow these guidelines to make sure your pull request is accepted.**
1. Before choosing to propose changes to this project, it is advisable to go through the readme.md file of the project to get the philosophy and the motive that went behind this project. The pull request should align with the philosophy and the motive of the original poster of this project.
2. To add your changes, make sure that the programming language in which you are proposing the changes should be the same as the programming language that has been used in the project. The versions of the programming language and the libraries(if any) used should also match with the original code.
3. Write a documentation on the changes that you are proposing. The documentation should include the problems you have noticed in the code(if any), the changes you would like to propose, the reason for these changes, and sample test cases. Remember that the topics in the documentation are strictly not limited to the topics aforementioned, but are just an inclusion.
4. Submit a pull request via [Git etiquettes](https://gist.github.com/mikepea/863f63d6e37281e329f8) 


## Improvements
1. Integrate real-time speed estimation using frame differencing or radar data.  
2. Deploy an IoT-based alerting system for nearby emergency units.  
3. Add audio-based alert detection for horn/siren recognition.  
4. Create a centralized dashboard for live analytics and heatmap visualization.  
5. Develop a mobile app for instant alerts and traffic insights.  
