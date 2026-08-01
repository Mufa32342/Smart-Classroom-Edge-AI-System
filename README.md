# 🏫 Smart Classroom Edge AI System

## Tech Stack & Badges

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-FF6B35?style=for-the-badge&logo=yolo&logoColor=white)](https://ultralytics.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Google Colab](https://img.shields.io/badge/Training-Google%20Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)](https://colab.research.google.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![University](https://img.shields.io/badge/University%20of%20Jaffna-Class%20of%202026-8B0000?style=for-the-badge)](https://www.jfn.ac.lk)

**YOLOv8-powered real-time classroom occupancy detection with automated AC climate control simulation.**

*Edge Computing — University of Jaffna · Group 02 · Class of 2026*

---

## 📋 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Google Colab Training](#-google-colab-training)
- [Using the Dashboards](#-using-the-dashboards)
- [API Reference](#-api-reference)
- [AC Simulation Rules](#-ac-simulation-rules)
- [Project Structure](#-project-structure)
- [Team](#-team)
- [License](#-license)

---

## 🌐 Overview

The **Smart Classroom Edge AI System** is an edge-computing solution that uses a custom-trained **YOLOv8** object detection model to monitor classroom occupancy in real-time. Based on the number and type of people detected, the system automatically simulates **air-conditioning (AC) control decisions** — reducing energy consumption and improving comfort without any manual intervention.

Designed and built as part of the **Edge Computing** module at the **University of Jaffna**, this system demonstrates practical edge AI deployment using a FastAPI backend and browser-based dashboards.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT SOURCES                            │
│         📷 Webcam / 🖼️ Image Upload / 🎞️ Video Upload          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND  (port 8000)                  │
│                                                                 │
│   ┌─────────────────┐        ┌──────────────────────────────┐   │
│   │   main.py       │◄──────►│   detector.py                │   │
│   │  REST API layer │        │   YOLOv8 Inference Engine    │   │
│   └─────────────────┘        │   (best.pt / best.onnx)      │   │
│                               └──────────────────────────────┘  │
│                                                                 │
│   Classes Detected: Janitor · Lecture · Person                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│               OCCUPANCY CLASSIFICATION ENGINE                   │
│                                                                 │
│   LOW    (0–2 persons)  →  AC OFF                               │
│   MEDIUM (3–9 persons)  →  AC ON @ 24°C                         │
│   HIGH   (10+ persons)  →  AC ON @ 20°C                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BROWSER DASHBOARDS                          │
│   🖥️  index.html       — Video/Image Detection Dashboard        │
│   ❄️  ac_dashboard.html — Smart AC Control Dashboard            │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

- 🎯 **Custom YOLOv8 Detection** — Trained on classroom-specific classes: `Janitor`, `Lecture`, `Person`
- ❄️ **Automated AC Simulation** — Dynamic AC state based on real-time occupancy level
- ⚡ **Edge-Ready FastAPI Backend** — Lightweight REST API suitable for edge deployment
- 📷 **Multi-Source Input** — Supports live webcam frames, image uploads, and video uploads
- 📊 **Live Dashboards** — Two browser-based HTML dashboards for detection and AC monitoring
- 📈 **Session Statistics** — Track detection counts, class distributions, and AC state changes
- 🔧 **Configurable Settings** — Adjust confidence threshold and occupancy thresholds via API
- 🚀 **ONNX Support** — Includes exported `best.onnx` for optimized edge inference
- 🌐 **CORS Enabled** — Dashboard and backend communicate seamlessly across origins

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following:

| Requirement | Version | Purpose |
|---|---|---|
| 🐍 Python | 3.10+ | Backend runtime |
| 📦 pip | Latest | Package management |
| 🐳 Docker Desktop | Latest | Containerized deployment |
| 🌐 Google Colab | Free account | Model training |
| 🤖 Trained Model | `best.pt` + `best.onnx` | YOLOv8 inference |
| 🖥️ Modern Browser | Chrome / Firefox / Edge | Dashboard access |

> **⚠️ Important:** The `best.pt` and `best.onnx` model files are **not included** in this repository. You must train the model using the provided Google Colab notebook and export the weights yourself (see [Google Colab Training](#-google-colab-training)).

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/classroom-detector.git
cd classroom-detector
```

### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

> 💡 It is recommended to use a virtual environment:
> ```bash
> python -m venv venv
> # Windows
> venv\Scripts\activate
> # Linux / macOS
> source venv/bin/activate
> pip install -r requirements.txt
> ```

### 3. Place Trained Model Files

After training with Google Colab (see below), download and place your model files:

```
backend/
└── models/
    ├── best.pt       ← Place your trained PyTorch weights here
    └── best.onnx     ← Place your exported ONNX model here
```

### 4. Run the FastAPI Server

```bash
# From the backend/ directory
python main.py
```

The server will start at **http://localhost:8000**

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     YOLOv8 model loaded successfully
```

### 5. Open the Dashboard

Open either dashboard directly in your browser:

| Dashboard | File | Purpose |
|---|---|---|
| 🖼️ Detection Dashboard | `dashboard/index.html` | Upload images/video for detection |
| ❄️ AC Control Dashboard | `dashboard/ac_dashboard.html` | Live occupancy & AC status |

```bash
# Simply open the file in your browser (Windows)
start dashboard\ac_dashboard.html
start dashboard\index.html
```

> 📡 Ensure the FastAPI server is running on port **8000** before opening the dashboards.

---

## 🔬 Google Colab Training

The model was trained using **Google Colab's GPU runtime** with a custom dataset annotated for classroom occupancy detection.

### Steps to Train

1. **Open the notebook**
   - Upload `classroom_yolo_train.ipynb` to [Google Colab](https://colab.research.google.com)
   - Or open it directly from your Google Drive

2. **Set Runtime to GPU**
   - Go to `Runtime` → `Change runtime type` → Select **GPU (T4 recommended)**

3. **Prepare Your Dataset**
   - Upload your annotated dataset (YOLO format) to Google Drive or Colab storage
   - Ensure the dataset contains annotations for: `Janitor`, `Lecture`, `Person`
   - Update the dataset YAML path in the notebook

4. **Run Training**
   - Execute all cells in order
   - Training will produce `runs/detect/train/weights/best.pt`

5. **Export to ONNX**
   ```python
   from ultralytics import YOLO
   model = YOLO("runs/detect/train/weights/best.pt")
   model.export(format="onnx")
   ```

6. **Download Model Files**
   - Download `best.pt` and `best.onnx` from Colab
   - Place them in `backend/models/`

### Recommended Training Config

```yaml
# dataset.yaml
path: /content/dataset
train: images/train
val: images/val

nc: 3
names:
  0: Janitor
  1: Lecture
  2: Person
```

```python
# Training command (inside notebook)
model = YOLO("yolov8n.pt")  # Start from pretrained nano model
model.train(
    data="dataset.yaml",
    epochs=100,
    imgsz=640,
    batch=16,
    name="classroom_yolo"
)
```

---

## 🖥️ Using the Dashboards

### ❄️ AC Control Dashboard (`ac_dashboard.html`)

The primary dashboard for smart classroom monitoring:

1. Open `dashboard/ac_dashboard.html` in your browser
2. Allow **camera access** when prompted
3. The dashboard will:
   - Capture live webcam frames every second
   - Send frames to `POST /detect/frame`
   - Display detected persons, occupancy level, and current AC state
   - Show real-time bounding boxes over detected individuals
4. AC state and temperature update automatically based on occupancy

### 🖼️ Detection Dashboard (`index.html`)

For static image or video analysis:

1. Open `dashboard/index.html` in your browser
2. **Image Detection:** Click "Upload Image" → select a photo → view detection results
3. **Video Detection:** Click "Upload Video" → select a video file → process and view annotated output
4. Results display bounding boxes, class labels, confidence scores, and occupancy summary

---

## 📡 API Reference

Base URL: `http://localhost:8000`

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `GET` | `/health` | Server health check | — |
| `GET` | `/classes` | List detected classes | — |
| `POST` | `/detect/frame` | Detect from base64 webcam frame | `{ "frame": "<base64>" }` |
| `POST` | `/detect/image` | Detect from uploaded image file | `multipart/form-data` |
| `POST` | `/detect/video` | Detect from uploaded video file | `multipart/form-data` |
| `GET` | `/stats` | Retrieve session statistics | — |
| `POST` | `/stats/reset` | Reset session statistics | — |
| `GET` | `/settings` | Get current system settings | — |
| `POST` | `/settings` | Update system settings | `{ "confidence": 0.5, ... }` |

### Example: `/detect/frame` Response

```json
{
  "occupancy_level": "MEDIUM",
  "person_count": 7,
  "ac_action": "AC ON",
  "ac_temperature": 24,
  "detections": [
    {
      "class": "Person",
      "confidence": 0.91,
      "bbox": [120, 80, 280, 420]
    }
  ],
  "annotated_frame": "<base64_encoded_image>"
}
```

### Interactive API Docs

FastAPI provides auto-generated documentation:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## ❄️ AC Simulation Rules

The system automatically determines the AC state based on the **total number of persons** detected in the classroom frame.

| Occupancy Level | Person Count | AC State | Temperature | Description |
|:-:|:-:|:-:|:-:|---|
| 🟢 **LOW** | 0 – 2 | ❌ OFF | — | Classroom empty or nearly empty; AC not required |
| 🟡 **MEDIUM** | 3 – 9 | ✅ ON | **24°C** | Moderate occupancy; comfortable cooling activated |
| 🔴 **HIGH** | 10+ | ✅ ON | **20°C** | High occupancy; full cooling engaged for comfort |

> **ℹ️ Note:** The `Lecture` class (instructor/lecturer) is counted separately but contributes to the total occupancy count. The `Janitor` class is detected for awareness but may be excluded from AC logic depending on your settings configuration.

---

## 📁 Project Structure

```
classroom-detector/
│
├── 📓 classroom_yolo_train.ipynb     # Google Colab training notebook
├── 📄 README.md                      # Project documentation (this file)
│
├── 🖥️ backend/
│   ├── main.py                       # FastAPI server (runs on port 8000)
│   ├── detector.py                   # YOLOv8 inference & occupancy logic
│   ├── requirements.txt              # Python dependencies
│   └── models/
│       ├── best.pt                   # Trained YOLOv8 weights (PyTorch)
│       └── best.onnx                 # Exported ONNX model (edge-optimized)
│
└── 🌐 dashboard/
    ├── ac_dashboard.html             # Smart Classroom AC Control Dashboard
    └── index.html                    # Video / Image Detection Dashboard
```

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 Group 03 — University of Jaffna

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---
