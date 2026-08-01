import cv2
import numpy as np
import base64
import time
from pathlib import Path
from ultralytics import YOLO
from PIL import Image
import io

MODEL_PATH = Path(__file__).parent / "models" / "best.pt"

class Detector:
    def __init__(self):
        print(f"🔄 Loading model from {MODEL_PATH}...")
        self.model = YOLO(str(MODEL_PATH))
        self.classes = self.model.names  # dict: {0: 'person', 1: 'chair', ...}
        self.conf_threshold = 0.25
        self.iou_threshold  = 0.45
        self.img_size       = 640
        self.detection_history = []   # list of detection summaries
        self.total_detections  = 0
        self.class_counts      = {v: 0 for v in self.classes.values()}
        print(f"✅ Model loaded! Classes: {list(self.classes.values())}")

    # ------------------------------------------------------------------
    def _to_cv2(self, image_bytes: bytes) -> np.ndarray:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img   = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img

    def _img_to_base64(self, img: np.ndarray) -> str:
        _, buffer = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 90])
        return base64.b64encode(buffer).decode("utf-8")

    # ------------------------------------------------------------------
    def detect_image(self, image_bytes: bytes, conf: float = None, iou: float = None):
        conf = conf or self.conf_threshold
        iou  = iou  or self.iou_threshold

        img = self._to_cv2(image_bytes)
        h, w = img.shape[:2]

        results = self.model.predict(
            source  = img,
            conf    = conf,
            iou     = iou,
            imgsz   = self.img_size,
            verbose = False,
        )[0]

        detections = []
        annotated  = img.copy()

        if results.boxes is not None and len(results.boxes) > 0:
            for box in results.boxes:
                x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].cpu().numpy()]
                cls_id   = int(box.cls[0].cpu().numpy())
                conf_val = float(box.conf[0].cpu().numpy())
                cls_name = self.classes.get(cls_id, str(cls_id))

                detections.append({
                    "class_id"  : cls_id,
                    "class_name": cls_name,
                    "confidence": round(conf_val, 4),
                    "bbox"      : {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                    "bbox_norm" : {
                        "x1": round(x1/w, 4), "y1": round(y1/h, 4),
                        "x2": round(x2/w, 4), "y2": round(y2/h, 4)
                    },
                })

                # Draw bbox
                color = self._class_color(cls_id)
                cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
                label = f"{cls_name} {conf_val:.2f}"
                (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
                cv2.rectangle(annotated, (x1, y1-th-8), (x1+tw+4, y1), color, -1)
                cv2.putText(annotated, label, (x1+2, y1-4),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,255,255), 1)

                # Update stats
                self.class_counts[cls_name] = self.class_counts.get(cls_name, 0) + 1

        self.total_detections += len(detections)

        # Save to history (keep last 100)
        entry = {
            "timestamp"  : time.time(),
            "count"      : len(detections),
            "classes"    : [d["class_name"] for d in detections],
        }
        self.detection_history.append(entry)
        if len(self.detection_history) > 100:
            self.detection_history.pop(0)

        return {
            "detections"    : detections,
            "count"         : len(detections),
            "annotated_b64" : self._img_to_base64(annotated),
            "image_size"    : {"width": w, "height": h},
        }

    # ------------------------------------------------------------------
    def detect_frame(self, frame_b64: str, conf: float = None):
        """Detect from base64 encoded frame (for WebSocket streaming)."""
        image_bytes = base64.b64decode(frame_b64)
        return self.detect_image(image_bytes, conf=conf)

    # ------------------------------------------------------------------
    def get_stats(self):
        recent = self.detection_history[-20:] if self.detection_history else []
        avg_per_frame = (
            sum(e["count"] for e in recent) / len(recent)
            if recent else 0
        )
        return {
            "total_detections"  : self.total_detections,
            "total_frames"      : len(self.detection_history),
            "avg_per_frame"     : round(avg_per_frame, 2),
            "class_counts"      : self.class_counts,
            "recent_history"    : recent[-10:],
            "model_path"        : str(MODEL_PATH),
            "classes"           : list(self.classes.values()),
            "num_classes"       : len(self.classes),
        }

    # ------------------------------------------------------------------
    def reset_stats(self):
        self.detection_history = []
        self.total_detections  = 0
        self.class_counts      = {v: 0 for v in self.classes.values()}

    # ------------------------------------------------------------------
    @staticmethod
    def _class_color(cls_id: int):
        palette = [
            (255,  56,  56), (255, 157,  36), ( 43, 189, 255),
            (255,  80, 120), (100, 255, 100), (200,  60, 255),
            ( 60, 180, 255), (255, 200,  60), ( 80, 255, 200),
            (255, 120,  60),
        ]
        return palette[cls_id % len(palette)]
