# PowerShell Launcher for Hostel Booking and Management System
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   HOSTEL BOOKING AND MANAGEMENT SYSTEM" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting server at http://localhost:8080 ..." -ForegroundColor Green
Start-Process "http://localhost:8080/index.html"
python server.py
