@echo off
echo ========================================================
echo   Khoi dong Backend Tu Vi & Than So Hoc (Uvicorn)
echo ========================================================
uvicorn main:app --reload --reload-exclude "test_*.py" --reload-exclude "_*.py" --reload-exclude "check_*.py" --reload-exclude "get_*.py"
