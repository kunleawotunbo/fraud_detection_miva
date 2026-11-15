Write-Host "`n=======================================================" -ForegroundColor Cyan
Write-Host " 📊 Mobile Money Fraud Surveillance Streamlit Dashboard" -ForegroundColor Cyan
Write-Host " Console URL: http://localhost:8501" -ForegroundColor Green
Write-Host "=======================================================`n" -ForegroundColor Cyan

$env:PYTHONPATH = "."
& ".\venv\Scripts\python.exe" -m streamlit run app.py

