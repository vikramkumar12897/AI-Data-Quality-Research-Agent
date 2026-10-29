@echo off
setlocal
python --version || (echo Python 3.12+ is required & pause & exit /b 1)
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist ".env" copy ".env.example" ".env"
echo Setup complete. Add OPENAI_API_KEY to .env and run run_app.bat
pause
