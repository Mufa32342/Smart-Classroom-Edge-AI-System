# 🏫 Smart Classroom Edge AI System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://docker.com)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-8.2+-red.svg)](https://github.com/ultralytics/ultralytics)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.10+-orange.svg)](https://opencv.org)

---

## 📌 Project Overview

**Smart Classroom Edge AI System** is an end-to-end Edge AI solution for real-time classroom occupancy detection and automated HVAC (Air Conditioning) control. The system processes video footage locally on edge devices (laptop/Raspberry Pi/Jetson) without sending data to the cloud, ensuring privacy and low latency.

### 🎯 What It Does

1. **Detects** people in classroom video using YOLOv8
2. **Classifies** occupancy as LOW (0-3), MEDIUM (4-9), or HIGH (10+)
3. **Controls** simulated AC system based on occupancy level
4. **Displays** live dashboard with video feed, occupancy status, and AC controls

### 🔒 Privacy First

- All processing runs locally on edge device
- No data sent to cloud
- Faces are not recorded
- Complies with privacy regulations

---

## 🏗️ System Architecture
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                           SMART CLASSROOM EDGE AI SYSTEM                               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  ┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐    │
│  │       INPUT          │     │       PROCESS        │     │       OUTPUT         │    │
│  │                      │     │                      │     │                      │    │
│  │  📹 Classroom Video  │───▶│   Edge Inference     │───▶│   Live Dashboard      │   │
│  │  📷 Webcam           │     │   (YOLOv8)           │    │                      │    │
│  │  📁 Video File       │     │                      │    │   📊 Occupancy       │    │
│  └──────────────────────┘      └──────────┬──────────┘    │   ❄️ AC Control      │    │
│                                           │               │   📝 System Logs     │    │
│                                           ▼               └──────────────────────┘    │
│                              ┌──────────────────────┐                                 │
│                              │   Occupancy          │                                 │
│                              │   Classification     │                                 │
│                              │   LOW/MEDIUM/HIGH    │                                 │
│                              └──────────┬───────────┘                                 │
│                                         │                                             │
│                                         ▼                                             │
│                              ┌──────────────────────┐                                 │
│                              │   AC Control         │                                 │
│                              │   Simulation         │                                 │
│                              │   - / 24°C / 20°C    │                                 │
│                              └──────────────────────┘                                 │
└───────────────────────────────────────────────────────────────────────────────────────┘

---

## ✨ Features
🔍 **Real-time Detection** : YOLOv8-based people counting in video 
🖥️ **Edge Deployment** : Runs on laptop, Raspberry Pi, Jetson 
🐳 **Docker Containerized** : Portable and reproducible 
📊 **Live Dashboard** : Real-time monitoring with Socket.IO 
❄️ **AC Simulation** : Automated HVAC control based on occupancy 
⚙️ **Configurable Thresholds** : Customize LOW/MEDIUM/HIGH limits 
🔄 **MLOps Ready** : Retrain, update, redeploy workflow 
🔒 **Privacy First** : All processing local, no cloud dependency 

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Flask 2.3.3
- **Real-time:** Flask-SocketIO, Socket.IO
- **Computer Vision:** OpenCV 4.10.0.84
- **ML/AI:** YOLOv8 (Ultralytics 8.2.100)
- **Numerical:** NumPy 1.26.4
- **Async:** Eventlet 0.35.2

### Frontend
- **HTML5 + CSS3 + JavaScript**
- **Socket.IO Client** for real-time updates
- **Responsive Dashboard** design

### DevOps
- **Docker** + Docker Compose
- **Python 3.11+** (Recommended)

---

## 📁 Project Structure
smart-classroom-edge-ai/
├── backend/
│ ├── app.py # Flask main application
│ ├── edge_inference.py # YOLOv8 inference pipeline
│ ├── ac_simulator.py # AC control logic
│ ├── video_processor.py # Video capture & processing
│ ├── config.py # Configuration settings
│ ├── requirements.txt # Python dependencies
│ └── Dockerfile # Docker build file
├── frontend/
│ └── index.html # Dashboard UI (single page)
├── model/
│ └── model.pt # Trained YOLOv8 model (optional)
├── videos/
│ └── classroom_video.mp4 # Your classroom video
├── docker-compose.yml
├── requirements.txt
└── README.md

---

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.11 or 3.12** (Python 3.13 NOT supported yet)
- **pip** (Python package manager)
- **Git** (optional)
- **Docker** (optional, for containerized deployment)


📊 Dashboard Features
Live Video Feed
Real-time video stream with occupancy overlay
Person count displayed on video
Color-coded occupancy badge (Green/Yellow/Red)
AC Control Panel
Display current temperature, fan speed, mode
Manual override controls
Temperature slider (16°C - 30°C)
Fan speed selector (Low/Medium/High/Auto)
System Status
Current occupancy level
Person count
AC status
Uptime
Frames processed
Threshold Settings
Configure LOW→MEDIUM threshold
Configure MEDIUM→HIGH threshold
Real-time updates
System Logs
Real-time activity log
Auto-scrolling
Clear logs option


🐳 Docker Deployment
Build Docker Image
bash
docker build -t smart-classroom -f backend/Dockerfile .
Run Docker Container
bash
docker run -p 5000:5000 --device /dev/video0:/dev/video0 smart-classroom
Use Docker Compose
bash
docker-compose up --build


🧪 Testing
Test Video Processing
bash
# Test video file processing
cd backend
python -c "from video_processor import VideoProcessor; vp = VideoProcessor('../videos/classroom_video.mp4'); print('Video processor test passed')"
Test Inference (without model)
python
# Quick test script
from edge_inference import OccupancyDetector
detector = OccupancyDetector()
print("✅ Detector initialized")
Test All Imports
bash
python -c "import cv2; import numpy; import flask; from ultralytics import YOLO; print('✅ All imports OK')"
🚨 Troubleshooting
Issue: ModuleNotFoundError
bash
# Install missing package
pip install <package_name>
# Or install all
pip install -r requirements.txt
Issue: NumPy installation error (Python 3.13)
Solution: Use Python 3.11 instead



==================================================
🏫 Smart Classroom Edge AI System
==================================================
📹 Video source: Video File
   Path: ../videos/classroom_video.mp4
📊 Occupancy thresholds: LOW=3, HIGH=10
🌐 Server: http://localhost:5000
==================================================
Press Ctrl+C to stop


📹 Opening video file: ../videos/classroom_video.mp4
📊 Total frames: 12345
✅ Video source opened successfully
⚠️ Using pretrained YOLOv8n model
✅ Model loaded successfully!
🚀 Starting system...
✅ System started successfully


Dashboard Display
Element	Example
Video Feed	Live with green box overlay
Occupancy Badge	🟡 MEDIUM
Person Count	6 people
AC Temperature	23°C
Fan Speed	Medium
Mode	Normal


👥 Team
Product Owner :	Nipuni
Project Manager	: Mufazzeer 
App Developers	: Rikas, Dilukji, Sajitha
Data Scientists	: Kaveeshan, Pathum, Sanjeewa


📅 Timeline
GitHub Repository Created	July 24, 2026
Final Demo	August 3-5, 2026
Peer Evaluation	August 5, 2026

📝 License
This project is developed for academic purposes as part of the Edge AI course.

🙏 Acknowledgments
Edge AI Course Team

All team members for their contributions

Open-source community (Ultralytics YOLO, Flask, OpenCV)


🔗 Quick Links
Link	                URL
GitHub Repository	https://github.com/Mufa32342/Smart-Classroom-Edge-AI-System
Docker Download	https://www.docker.com/products/docker-desktop

🎯 Project Demo Script
What to Show
Start System (10 seconds)
Show terminal output
Explain system starting
Dashboard (30 seconds)
Show video feed
Explain each component
Show real-time updates
Occupancy Changes (30 seconds)
Show different occupancy levels
Show AC adjusting automatically
Explain threshold logic
Manual Controls (20 seconds)
Adjust temperature
Change fan speed
Update thresholds
System Logs (10 seconds)
Show log entries
Explain monitoring

✅ Checklist for Demo
□ System running (Python app)
□ Dashboard open in browser
□ Video playing in feed
□ People detected with count
□ Occupancy level changing
□ AC status updating
□ Logs showing activity
□ Manual controls working
□ Thresholds configurable

🔧 Customization
Adding Custom Model
bash
# Place your trained model in model/ folder
model/model.pt


Commit to GitHub:

bash
git add README.md
git commit -m "Add README file"
git push
🎯 Quick Reference - File Locations
File	Location	Purpose
README.md	S:\EdgeAi\	Project documentation
requirements.txt	S:\EdgeAi\	Python dependencies
app.py	S:\EdgeAi\backend\	Main application
config.py	S:\EdgeAi\backend\	Configuration
index.html	S:\EdgeAi\frontend\	Dashboard UI
