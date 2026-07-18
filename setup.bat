@echo off
setlocal

cd /d "%~dp0"

echo Current directory: 
cd
echo.

echo Creating the Python environment...
py -m venv .venv

if errorlevel 1 (
    echo.
    echo Could not create the environment.
    echo Confirm that Python is installed and that the "py" command works.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

echo.
echo Installing required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Package installation failed.
    pause 
    exit /b 1
)

echo.
echo Setup complete.
echo You may now use run_estimator.bat.
pause