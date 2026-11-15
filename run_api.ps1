Write-Host "`n=======================================================" -ForegroundColor Cyan
Write-Host " 🛡️  Mobile Money Fraud Surveillance REST API Gateway" -ForegroundColor Cyan
Write-Host " Swagger UI: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host " Health Check: http://127.0.0.1:8000/health" -ForegroundColor Green
Write-Host "=======================================================`n" -ForegroundColor Cyan

$env:PYTHONPATH = "."
& ".\venv\Scripts\python.exe" api.py

