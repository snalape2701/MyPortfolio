@echo off
title Premium Glassmorphism Portfolio & API launcher
color 0b

echo =====================================================================
echo    SAHIL TALAPE ^| LUXURY GLASSMORPHISM PORTFOLIO ^& BACKEND
echo =====================================================================
echo.
echo  [1] Starting the Frontend:
echo      To view your gorgeous personal portfolio, simply open the
echo      following file in your favorite web browser:
echo      n:\MyPortfolio\frontend\public\index.html
echo.
echo  [2] Starting the FastAPI Backend Placeholder:
echo      Checking local Python installation...
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  [!] WARNING: Python is not detected in your system's PATH.
    echo      To enable the contact form, please install Python 3.10+
    echo      and start FastAPI as detailed in n:\MyPortfolio\README.md.
    echo.
    pause
    exit /b
)

cd backend
if not exist "venv" (
    echo  [-] Creating virtual environment (venv)...
    python -m venv venv
)

echo  [-] Activating virtual environment...
call venv\Scripts\activate  

echo  [-] Checking / Installing requirements...
pip install -r requirements.txt

echo.
echo  [+] SUCCESS: Launching FastAPI local server on port 8000!
echo      API documentation available at: http://127.0.0.1:8000/docs
echo      submissions will log directly to backend\app\submissions.json
echo.
echo =====================================================================
echo.
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
pause
