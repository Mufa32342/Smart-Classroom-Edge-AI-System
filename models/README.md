# Models

This folder contains the trained YOLO model weights.

## Files

| File | Size | Description |
|------|------|-------------|
| `best.pt` | ~21 MB | YOLO PyTorch model — **included** |
| `best.onnx` | ~43 MB | YOLO ONNX export — **NOT included** (exceeds GitHub 25 MB upload limit) |

## How to export `best.onnx`

`best.onnx` was excluded from this repository because it exceeds GitHub's 25 MB file upload limit.

To regenerate it after training, run:

```python
from ultralytics import YOLO
model = YOLO("best.pt")
model.export(format="onnx")
```

This will produce a `best.onnx` file in the same directory. Copy it here for use by the backend API.
