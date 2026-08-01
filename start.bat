@echo off
:: ════════════════════════════════════════════════════════
::  Smart Classroom Edge AI System — Docker Start Script
::  For Windows (run this file to start the system)
:: ════════════════════════════════════════════════════════

title Smart Classroom Edge AI System

echo.
echo  ========================================
echo    Smart Classroom Edge AI System
echo    University of Jaffna - Group 03
echo  ========================================
echo.

:: Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Docker is not running!
    echo  Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo  [1/3] Building Docker image...
docker compose build

echo.
echo  [2/3] Starting container...
docker compose up -d

echo.
echo  [3/3] Waiting for server to start...
timeout /t 10 /nobreak >nul

echo.
echo  ========================================
echo   System is ready!
echo.
echo   API + Dashboard:
echo   http://localhost:8000
echo.
echo   AC Dashboard (Smart Classroom):
echo   http://localhost:8000/dashboard/ac_dashboard.html
echo.
echo   API Documentation:
echo   http://localhost:8000/docs
echo  ========================================
echo.

:: Open dashboard in default browser
start http://localhost:8000/dashboard/ac_dashboard.html

echo  Press any key to stop the system...
pause >nul

echo.
echo  Stopping containers...
docker compose down
echo  Done. Goodbye!
pause
