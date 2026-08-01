# ════════════════════════════════════════════════════════════════════
#  Smart Classroom Edge AI System — Dockerfile
#  Runs the FastAPI backend + serves the dashboard on port 8000
# ════════════════════════════════════════════════════════════════════

FROM python:3.11-slim

LABEL maintainer="Group 03 — University of Jaffna"
LABEL description="Smart Classroom Edge AI System"
LABEL version="1.0.0"

# System deps for OpenCV headless + libGL stub
RUN apt-get update && apt-get install -y --no-install-recommends \
        libglib2.0-0 \
        libgomp1 \
        libgl1 \
        libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt /app/backend/requirements.txt

# Install step-by-step:
# 1. Install ultralytics (pulls in opencv-python as dep)
# 2. Uninstall opencv-python (has GUI/libxcb deps)
# 3. Install opencv-python-headless (no display needed)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
        "fastapi" \
        "uvicorn[standard]" \
        "ultralytics" \
        "python-multipart" \
        "pillow" \
        "numpy" \
        "aiofiles" \
    && pip uninstall -y opencv-python || true \
    && pip install --no-cache-dir "opencv-python-headless"

# Copy backend source code
COPY backend/ /app/backend/

# Copy dashboard
COPY dashboard/ /app/dashboard/

# Verify model files
RUN ls -lh /app/backend/models/ || echo "WARNING: No model files found!"

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

WORKDIR /app/backend
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
