@echo off
setlocal

echo [run_ui] Starting Streamlit UI...
streamlit run src/ui/streamlit_app.py
if errorlevel 1 exit /b 1

endlocal