@echo off
setlocal enabledelayedexpansion

REM Build standalone Windows executable with PyInstaller.
set PROJECT_DIR=%~dp0
cd /d %PROJECT_DIR%
set ICON=assets\icon.ico

if not exist .venv (
    py -3 -m venv .venv || python -m venv .venv
)

call .venv\Scripts\activate.bat

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

REM Clean previous build artifacts
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

set ICON_FLAG=
if exist "%ICON%" (
  set ICON_FLAG=--icon "%ICON%"
)

pyinstaller ^
  --noconfirm ^
  --windowed ^
  --name FiscaliaCases ^
  --hidden-import PyQt6.sip ^
  --add-data "cases.db;." ^
  %ICON_FLAG% ^
  main.py

echo.
echo Build finalizado. Encuentra el ejecutable en dist\FiscaliaCases.
endlocal
