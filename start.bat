@echo off
start "Backend" cmd /k ".venv\Scripts\activate && python -m uvicorn app.main:app --reload --port 8000"
timeout /t 3 /nobreak > NUL
start "Frontend" cmd /k ".venv\Scripts\activate && python -m streamlit run streamlit_app.py"