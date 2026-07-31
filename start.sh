#!/bin/bash
# ════════════════════════════════════════════════════════
#  Smart Classroom Edge AI System — Docker Start Script
#  For Linux / macOS / WSL
# ════════════════════════════════════════════════════════

set -e

echo ""
echo " ========================================"
echo "   Smart Classroom Edge AI System"
echo "   University of Jaffna - Group 03"
echo " ========================================"
echo ""

# Check Docker
if ! docker info >/dev/null 2>&1; then
  echo " [ERROR] Docker is not running!"
  echo " Please start Docker and try again."
  exit 1
fi

echo " [1/3] Building Docker image..."
docker compose build

echo ""
echo " [2/3] Starting container..."
docker compose up -d

echo ""
echo " [3/3] Waiting for server to start (30s)..."
sleep 10

# Health check loop
for i in {1..6}; do
  if curl -s http://localhost:8000/health >/dev/null 2>&1; then
    echo " ✅ Server is ready!"
    break
  fi
  echo "   Waiting... ($i/6)"
  sleep 5
done

echo ""
echo " ========================================"
echo "  System is ready!"
echo ""
echo "  AC Dashboard (Smart Classroom):"
echo "  http://localhost:8000/dashboard/ac_dashboard.html"
echo ""
echo "  API Documentation:"
echo "  http://localhost:8000/docs"
echo " ========================================"
echo ""

# Try to open browser
if command -v xdg-open >/dev/null 2>&1; then
  xdg-open http://localhost:8000/dashboard/ac_dashboard.html
elif command -v open >/dev/null 2>&1; then
  open http://localhost:8000/dashboard/ac_dashboard.html
fi

echo " Press CTRL+C to stop..."
echo ""

# Show logs
docker compose logs -f
