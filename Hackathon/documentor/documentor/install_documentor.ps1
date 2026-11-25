$ErrorActionPreference = "Stop"
Set-Location "C:\Users\JohnDon\Desktop\Hackathon\documentor\documentor"

if (-Not (Test-Path ".venv")) {
    python -m venv .venv
}

& ".\.venv\Scripts\Activate.ps1"

$PyPI = "https" + "://" + "pypi.org" + "/simple"

python -m pip install --upgrade pip -i $PyPI
pip install -r requirements.txt -i $PyPI

pytest -q

Write-Host ""
Write-Host "Installation and tests finished."
Write-Host "Start the app with:"
Write-Host "  uvicorn app.main:app --reload"