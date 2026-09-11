@echo off
echo ========================================================
echo   Khoi dong Backend Tu Vi ^& Than So Hoc (Uvicorn)
echo ========================================================
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)
uvicorn main:app --reload --reload-exclude "_*.py" --reload-exclude "check_*.py" --reload-exclude "get_*.py" --reload-exclude "test_old_*.py"
