# Models

This folder contains the trained YOLO model weights used by the backend API.

## Files

| File | Size | Description |
|------|------|-------------|
| `best.pt` | ~21 MB | YOLO PyTorch model — **included** |
| `best.onnx` | ~43 MB | YOLO ONNX export — **NOT included** (exceeds GitHub 25 MB upload limit) |

## How to get `best.onnx`

`best.onnx` was excluded from this repository because it exceeds GitHub's 25 MB file upload limit.

To generate it locally, run the following from the Data Scientists branch notebooks:

```python
from ultralytics import YOLO
model = YOLO("best.pt")
model.export(format="onnx")
```

Or request the file directly from the Data Scientists team.
