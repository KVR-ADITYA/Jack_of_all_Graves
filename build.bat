@echo off
title Jack of All Graves - Build
echo ============================================
echo   Jack of All Graves - Building .exe
echo ============================================
echo.
echo This bundles Python + PyTorch + the RL model into a standalone app.
echo Expect 5-15 minutes and a ~400-600 MB output folder.
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Install Python 3.10+ and try again.
    pause & exit /b 1
)

where pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo Starting build...
echo.
pyinstaller JackOfAllGraves.spec --clean --noconfirm

if %errorlevel% == 0 (
    echo.
    echo ============================================
    echo   BUILD COMPLETE
    echo ============================================
    echo.
    echo Your app is at:  dist\JackOfAllGraves\
    echo Run it with:     dist\JackOfAllGraves\JackOfAllGraves.exe
    echo.
    echo To distribute: zip the entire dist\JackOfAllGraves\ folder
    echo and share it. No Python install needed on the target machine.
    echo.
) else (
    echo.
    echo BUILD FAILED. Check errors above.
    echo Common fixes:
    echo   - Run: pip install -r requirements.txt
    echo   - Make sure jack\rl\checkpoints\bingo_agent_final.zip exists
    echo.
)
pause
