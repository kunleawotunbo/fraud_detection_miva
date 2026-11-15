@echo off
title Mobile Money Fraud Detection - FastAPI Gateway
echo =======================================================
echo  Mobile Money Fraud Surveillance REST API Gateway
echo  Swagger UI: http://127.0.0.1:8000/docs
echo  Health:     http://127.0.0.1:8000/health
echo =======================================================
set PYTHONPATH=.
.\venv\Scripts\python.exe api.py
pause

