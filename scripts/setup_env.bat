@echo off
setlocal

echo [setup_env] Creating virtual environment...
python -m venv .venv
if errorlevel 1 exit /b 1

echo [setup_env] Upgrading pip...
.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 exit /b 1

echo [setup_env] Installing dependencies...
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

echo [setup_env] Creating data\raw directory...
if not exist data\raw mkdir data\raw

echo [setup_env] Done.
echo Next step:
echo   .venv\Scripts\activate
echo   Place the raw dataset at: data\raw\three_months.csv

endlocal