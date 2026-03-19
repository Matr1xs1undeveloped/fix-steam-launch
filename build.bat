@echo off
echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.
echo To build the executable, run:
echo   pyinstaller steam_cache_cleaner.spec
echo.
pause

