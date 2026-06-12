@echo off
setlocal

echo [validate_release] Step 1/4 - Setting deterministic environment...
call scripts\set_env_deterministic.bat
if errorlevel 1 exit /b 1

echo [validate_release] Step 2/4 - Static validation...
call scripts\validate_static.bat
if errorlevel 1 exit /b 1

echo [validate_release] Step 3/4 - Running full pipeline...
call scripts\run_pipeline.bat
if errorlevel 1 exit /b 1

echo [validate_release] Step 4/4 - Running test suite...
call scripts\run_tests.bat
if errorlevel 1 exit /b 1

echo [validate_release] Release validation completed successfully.

endlocal