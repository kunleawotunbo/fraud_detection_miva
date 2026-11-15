@echo off
title Mobile Money Fraud Detection - Streamlit Console
echo =======================================================
echo  Mobile Money Fraud Surveillance Streamlit Dashboard
echo  Dashboard: http://localhost:8501
echo =======================================================
set PYTHONPATH=.
.\venv\Scripts\python.exe -m streamlit run app.py
pause

