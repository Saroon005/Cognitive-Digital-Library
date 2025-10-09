@echo off
REM Start Backend Server Script
cd /d "%~dp0"
echo Starting Cognitive Digital Library Backend...
echo.
call venv\Scripts\activate.bat
python main.py
