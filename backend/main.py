import base64
import time
import tempfile
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from detector import Detector

detector: Optional[Detector] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global detector
    print("🚀 Starting Classroom Detector API...")
    detector = Detector()
    print("✅ API Ready!")
    yield

app = FastAPI(
    title="🎓 Smart Classroom Edge AI API",
    description="YOLOv8 Classroom Occupancy Detection with Automated AC Control",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static dashboard ──────────────────────────────────────────────────
dashboard_dir = Path(__file__).parent.parent / "dashboard"
if dashboard_dir.exists():
    app.mount("/dashboard", StaticFiles(directory=str(dashboard_dir)), name="dashboard")

# Temp dir for video processing
TEMP_DIR = Path(tempfile.gettempdir()) / "classroom_detector"
TEMP_DIR.mkdir(exist_ok=True)

# ── Occupancy Logic ───────────────────────────────────────────────────
def classify_occupancy(person_count: int, low_max: int = 2, med_max: int = 9) -> str:
    if person_count <= low_max:
        return "LOW"
    elif person_count <= med_max:
        return "MEDIUM"
    return "HIGH"

def get_ac_action(occupancy: str, med_temp: int = 24, high_temp: int = 20) -> dict:
    if occupancy == "LOW":
        return {"state": "OFF", "temp": None, "fan": "OFF"}
    elif occupancy == "MEDIUM":
        return {"state": "ON", "temp": med_temp, "fan": "Low"}
    else:
        return {"state": "ON", "temp": high_temp, "fan": "High"}

# ── Schemas ───────────────────────────────────────────────────────────
class FrameRequest(BaseModel):
    frame_b64: str
    conf: float = 0.25
    low_max: int = 2
    med_max: int = 9
    med_temp: int = 24
    high_temp: int = 20

class SettingsRequest(BaseModel):
    conf: Optional[float] = None
    iou: Optional[float] = None
    img_size: Optional[int] = None

# ── Root → Dashboard redirect ─────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to the AC dashboard."""
    return RedirectResponse(url="/dashboard/ac_dashboard.html")

# ── Health ────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "ok",
        "timestamp": time.time(),
        "model_loaded": detector is not None,
        "classes": list(detector.classes.values()) if detector else [],
    }

# ── Frame Detection (with occupancy + AC action) ──────────────────────
@app.post("/detect/frame", tags=["Detection"])
async def detect_frame(req: FrameRequest):
    if detector is None:
        raise HTTPException(503, "Model not loaded")

    result = detector.detect_image(base64.b64decode(req.frame_b64), conf=req.conf)

    person_count = sum(
        1 for d in result["detections"]
        if d["class_name"].lower() in ["person", "janitor"]
    )
    occupancy = classify_occupancy(person_count, req.low_max, req.med_max)
    ac = get_ac_action(occupancy, req.med_temp, req.high_temp)

    return JSONResponse({
        "success"       : True,
        "count"         : result["count"],
        "person_count"  : person_count,
        "detections"    : result["detections"],
        "annotated_b64" : result["annotated_b64"],
        "occupancy"     : occupancy,
        "ac_state"      : ac["state"],
        "ac_temp"       : ac["temp"],
        "ac_fan"        : ac["fan"],
    })

# ── Image Detection ───────────────────────────────────────────────────
@app.post("/detect/image", tags=["Detection"])
async def detect_image(
    file: UploadFile = File(...),
    conf: float = Query(0.25, ge=0.01, le=1.0),
    iou: float = Query(0.45, ge=0.01, le=1.0),
):
    if detector is None:
        raise HTTPException(503, "Model not loaded")
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, f"Expected image, got {file.content_type}")

    image_bytes = await file.read()
    result = detector.detect_image(image_bytes, conf=conf, iou=iou)
    return JSONResponse({
        "success"       : True,
        "filename"      : file.filename,
        "count"         : result["count"],
        "detections"    : result["detections"],
        "annotated_b64" : result["annotated_b64"],
        "image_size"    : result["image_size"],
    })

# ── Video Detection ───────────────────────────────────────────────────
@app.post("/detect/video", tags=["Detection"])
async def detect_video(
    file: UploadFile = File(...),
    conf: float = Query(0.25),
    iou: float = Query(0.45),
    skip: int = Query(2, ge=1, le=10),
):
    import cv2
    import numpy as np

    if detector is None:
        raise HTTPException(503, "Model not loaded")

    video_bytes = await file.read()
    suffix   = Path(file.filename).suffix or ".mp4"
    in_path  = TEMP_DIR / f"input_{int(time.time())}{suffix}"
    out_path = TEMP_DIR / f"output_{int(time.time())}.mp4"
    in_path.write_bytes(video_bytes)

    cap = cv2.VideoCapture(str(in_path))
    if not cap.isOpened():
        in_path.unlink(missing_ok=True)
        raise HTTPException(400, "Could not open video")

    fps    = cap.get(cv2.CAP_PROP_FPS) or 25
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(out_path), fourcc, fps, (width, height))

    frame_stats = []
    frame_idx   = 0
    last_result = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % skip == 0:
            _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            result = detector.detect_image(buf.tobytes(), conf=conf, iou=iou)
            last_result = result
            ann_bytes = base64.b64decode(result["annotated_b64"])
            ann_arr   = np.frombuffer(ann_bytes, np.uint8)
            ann_frame = cv2.imdecode(ann_arr, cv2.IMREAD_COLOR)
            if ann_frame is not None:
                writer.write(ann_frame)
            person_count = sum(
                1 for d in result["detections"]
                if d["class_name"].lower() in ["person", "janitor"]
            )
            frame_stats.append({
                "frame"      : frame_idx,
                "count"      : result["count"],
                "person_count": person_count,
                "occupancy"  : classify_occupancy(person_count),
                "detections" : [{"class": d["class_name"], "conf": d["confidence"]} for d in result["detections"]],
            })
        else:
            if last_result:
                ann_bytes = base64.b64decode(last_result["annotated_b64"])
                ann_arr   = np.frombuffer(ann_bytes, np.uint8)
                ann_frame = cv2.imdecode(ann_arr, cv2.IMREAD_COLOR)
                if ann_frame is not None:
                    writer.write(cv2.resize(ann_frame, (width, height)))
            else:
                writer.write(frame)
        frame_idx += 1

    cap.release()
    writer.release()
    in_path.unlink(missing_ok=True)

    class_counts = {}
    total_det = 0
    for fs in frame_stats:
        total_det += fs["count"]
        for d in fs["detections"]:
            class_counts[d["class"]] = class_counts.get(d["class"], 0) + 1

    video_b64 = ""
    if out_path.exists() and out_path.stat().st_size > 0:
        video_b64 = base64.b64encode(out_path.read_bytes()).decode("utf-8")
        out_path.unlink(missing_ok=True)

    return JSONResponse({
        "success"              : True,
        "filename"             : file.filename,
        "total_frames"         : total,
        "processed_frames"     : len(frame_stats),
        "total_detections"     : total_det,
        "class_summary"        : class_counts,
        "fps"                  : fps,
        "resolution"           : {"width": width, "height": height},
        "frame_stats"          : frame_stats,
        "annotated_video_b64"  : video_b64,
    })

# ── Classes / Stats / Settings ────────────────────────────────────────
@app.get("/classes", tags=["Info"])
async def get_classes():
    if detector is None:
        raise HTTPException(503, "Model not loaded")
    return {
        "classes"    : list(detector.classes.values()),
        "num_classes": len(detector.classes),
        "class_map"  : detector.classes,
    }

@app.get("/stats", tags=["Stats"])
async def get_stats():
    if detector is None:
        raise HTTPException(503, "Model not loaded")
    return detector.get_stats()

@app.post("/stats/reset", tags=["Stats"])
async def reset_stats():
    if detector is None:
        raise HTTPException(503, "Model not loaded")
    detector.reset_stats()
    return {"success": True}

@app.get("/settings", tags=["Settings"])
async def get_settings():
    if detector is None:
        raise HTTPException(503, "Model not loaded")
    return {
        "conf"    : detector.conf_threshold,
        "iou"     : detector.iou_threshold,
        "img_size": detector.img_size,
    }

@app.post("/settings", tags=["Settings"])
async def update_settings(req: SettingsRequest):
    if detector is None:
        raise HTTPException(503, "Model not loaded")
    if req.conf is not None:
        detector.conf_threshold = req.conf
    if req.iou is not None:
        detector.iou_threshold = req.iou
    if req.img_size is not None:
        detector.img_size = req.img_size
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
