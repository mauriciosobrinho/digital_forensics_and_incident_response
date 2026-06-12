@echo off
setlocal

echo [run_tests] Reminder: full pytest expects HUMAN_DECISION_SCENARIO=approve.
echo [run_tests] Running test suite...
pytest -v
if errorlevel 1 exit /b 1

endlocal