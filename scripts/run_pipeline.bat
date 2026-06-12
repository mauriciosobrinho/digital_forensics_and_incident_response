@echo off
setlocal

if not exist data\raw\three_months.csv (
  echo [run_pipeline] Missing required dataset: data\raw\three_months.csv
  echo Copy the original challenge CSV to data\raw\three_months.csv before running the pipeline.
  exit /b 1
)

echo [run_pipeline] Running full DFIR pipeline...
python -m src.app
if errorlevel 1 exit /b 1

endlocal