@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul 2>&1
color 0A
title Instalador Automático - Sistema de Gestión de Casos

REM ===================================================================
REM Sistema de Gestión de Casos Judiciales
REM Copyright © 2026 Rafael Llibre
REM Todos los derechos reservados.
REM ===================================================================

REM Capturar errores y evitar cierre automático
if "%1"=="CHILD" (
    shift
    goto MAIN
)

REM Ejecutar en modo con captura de errores
cmd /k "%~f0 CHILD %*"
exit /b

:MAIN

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║  INSTALADOR AUTOMÁTICO - SISTEMA DE GESTIÓN DE CASOS         ║
echo ║  Versión 3.0 - Enero 2026                                     ║
echo ║  Copyright © 2026 Rafael Llibre                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Verificar si se está ejecutando como administrador
net session >nul 2>&1
if %errorlevel% == 0 (
    echo ✓ Ejecutando como Administrador
) else (
    echo ⚠ No se está ejecutando como Administrador
    echo   Esto puede causar problemas al instalar Python
    echo.
)

echo Presiona cualquier tecla para continuar...
pause >nul
echo.

REM ============================================================
REM PASO 1: Verificar Python
REM ============================================================

echo [1/6] Verificando instalación de Python...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
set PYTHON_CHECK=%errorlevel%

if !PYTHON_CHECK! neq 0 (
    echo ⚠ Python no está instalado
    echo.
    goto INSTALL_PYTHON
)

REM Obtener versión de Python con manejo de errores
set "PYTHON_VERSION="
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%i"

if "!PYTHON_VERSION!"=="" (
    echo ⚠ No se pudo detectar la versión de Python
    echo.
    goto INSTALL_PYTHON
)

echo Versión detectada: !PYTHON_VERSION!
echo.

REM Extraer versión mayor y menor (ej: 3.12.1 -> 3.12)
for /f "tokens=1,2 delims=." %%a in ("!PYTHON_VERSION!") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

REM Verificar si la versión es 3.8 o superior
if !PYTHON_MAJOR! LSS 3 (
    echo ⚠ Python !PYTHON_VERSION! es demasiado antiguo
    echo Se requiere Python 3.8 o superior
    echo.
    goto INSTALL_PYTHON
)

if !PYTHON_MAJOR! EQU 3 (
    if !PYTHON_MINOR! LSS 8 (
        echo ⚠ Python !PYTHON_VERSION! es demasiado antiguo
        echo Se requiere Python 3.8 o superior
        echo.
        goto INSTALL_PYTHON
    )
)

echo ✓ Python !PYTHON_VERSION! detectado (versión correcta)
echo.
goto CHECK_PIP

REM ============================================================
REM Instalar Python automáticamente
REM ============================================================

:INSTALL_PYTHON
echo Descargando e instalando Python 3.12...
echo Esto puede tomar varios minutos...
echo.

REM Descargar instalador de Python 3.12
set PYTHON_INSTALLER=python-3.12.1-amd64.exe
set PYTHON_URL=https://www.python.org/ftp/python/3.12.1/%PYTHON_INSTALLER%

echo Descargando Python desde python.org...
echo URL: %PYTHON_URL%
echo.

REM Usar PowerShell para descargar con manejo de errores
echo Intentando descargar...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; try { Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%TEMP%\%PYTHON_INSTALLER%' -ErrorAction Stop; exit 0 } catch { Write-Host 'Error: ' $_.Exception.Message; exit 1 }}"

set DOWNLOAD_RESULT=!errorlevel!

if !DOWNLOAD_RESULT! neq 0 (
    echo.
    echo ✗ ERROR: No se pudo descargar Python
    echo.
    echo Posibles causas:
    echo   - Sin conexión a internet
    echo   - Firewall bloqueando la descarga
    echo   - Antivirus bloqueando PowerShell
    echo.
    echo SOLUCIÓN:
    echo 1. Verifica tu conexión a internet
    echo 2. Desactiva temporalmente el antivirus
    echo 3. O descarga e instala Python manualmente:
    echo    URL: https://www.python.org/downloads/
    echo    Durante instalación, MARCA "Add Python to PATH"
    echo 4. Ejecuta este script nuevamente
    echo.
    pause
    exit /b 1
)

echo ✓ Python descargado correctamente
echo.

REM Verificar que el archivo existe
if not exist "%TEMP%\%PYTHON_INSTALLER%" (
    echo ✗ ERROR: El archivo descargado no se encontró
    echo.
    pause
    exit /b 1
)

REM Instalar Python silenciosamente
echo Instalando Python (esto puede tomar 2-5 minutos)...
echo Por favor, espera...
echo.
echo IMPORTANTE: NO cierres esta ventana
echo.

start /wait "" "%TEMP%\%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

set INSTALL_RESULT=!errorlevel!

if !INSTALL_RESULT! neq 0 (
    echo.
    echo ⚠ La instalación automática puede haber fallado
    echo   Error code: !INSTALL_RESULT!
    echo.
    echo Intenta instalar manualmente:
    echo 1. Busca el archivo: %TEMP%\%PYTHON_INSTALLER%
    echo 2. Haz doble clic
    echo 3. MARCA "Add Python to PATH"
    echo 4. Completa la instalación
    echo 5. Ejecuta este script nuevamente
    echo.
    pause
    exit /b 1
)

echo ✓ Python instalado correctamente
echo.

REM Limpiar archivo temporal
del "%TEMP%\%PYTHON_INSTALLER%" >nul 2>&1

echo IMPORTANTE: Cerrando y reiniciando el script...
echo Python fue instalado. El script debe ejecutarse de nuevo para
echo que Windows reconozca el nuevo PATH.
echo.
echo Por favor, ejecuta 'instalar_windows.bat' nuevamente.
echo.
pause
exit /b 0

:CHECK_PIP

REM ============================================================
REM PASO 2: Verificar pip
REM ============================================================

echo [2/6] Verificando pip (gestor de paquetes)...
echo.

pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ ERROR: pip no está instalado
    echo Intentando instalar pip...
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo ✗ No se pudo instalar pip automáticamente
        echo Por favor, reinstala Python con "Add Python to PATH"
        pause
        exit /b 1
    )
)

echo ✓ pip instalado correctamente
echo.

REM ============================================================
REM PASO 3: Actualizar pip
REM ============================================================

echo [3/6] Actualizando pip a la última versión...
echo.

python -m pip install --upgrade pip --quiet
if %errorlevel% neq 0 (
    echo ⚠ Advertencia: No se pudo actualizar pip (continuando...)
) else (
    echo ✓ pip actualizado
)
echo.

REM ============================================================
REM PASO 4: Instalar dependencias
REM ============================================================

echo [4/6] Instalando librerías necesarias...
echo.
echo Esto puede tomar 2-10 minutos dependiendo de tu conexión...
echo.

if exist requirements.txt (
    echo Instalando desde requirements.txt...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo ✗ ERROR: No se pudieron instalar las dependencias
        echo.
        echo Intentando instalación individual...
        echo.
        goto INSTALL_INDIVIDUAL
    )
    echo.
    echo ✓ Todas las librerías instaladas desde requirements.txt
    goto VERIFY_INSTALL
) else (
    echo ⚠ Advertencia: requirements.txt no encontrado
    echo Instalando librerías individualmente...
    echo.
    goto INSTALL_INDIVIDUAL
)

:INSTALL_INDIVIDUAL
echo Instalando PyQt6...
pip install PyQt6
if %errorlevel% neq 0 goto INSTALL_ERROR

echo Instalando pandas...
pip install pandas
if %errorlevel% neq 0 goto INSTALL_ERROR

echo Instalando matplotlib...
pip install matplotlib
if %errorlevel% neq 0 goto INSTALL_ERROR

echo Instalando openpyxl...
pip install openpyxl
if %errorlevel% neq 0 goto INSTALL_ERROR

echo.
echo ✓ Todas las librerías instaladas correctamente
goto VERIFY_INSTALL

:INSTALL_ERROR
echo.
echo ✗ ERROR: No se pudo instalar alguna librería
echo.
echo Posibles causas:
echo - Sin conexión a internet
echo - Firewall bloqueando pip
echo - Permisos insuficientes
echo.
echo Intenta ejecutar este script como Administrador
pause
exit /b 1

:VERIFY_INSTALL

REM ============================================================
REM PASO 5: Verificar instalación
REM ============================================================

echo.
echo [5/6] Verificando instalación...
echo.

python -c "import PyQt6" 2>nul
if %errorlevel% neq 0 (
    echo ✗ ERROR: PyQt6 no se instaló correctamente
    goto INSTALL_ERROR
)
echo ✓ PyQt6 verificado

python -c "import pandas" 2>nul
if %errorlevel% neq 0 (
    echo ✗ ERROR: pandas no se instaló correctamente
    goto INSTALL_ERROR
)
echo ✓ pandas verificado

python -c "import matplotlib" 2>nul
if %errorlevel% neq 0 (
    echo ✗ ERROR: matplotlib no se instaló correctamente
    goto INSTALL_ERROR
)
echo ✓ matplotlib verificado

python -c "import openpyxl" 2>nul
if %errorlevel% neq 0 (
    echo ✗ ERROR: openpyxl no se instaló correctamente
    goto INSTALL_ERROR
)
echo ✓ openpyxl verificado

REM ============================================================
REM PASO 6: Crear carpetas necesarias
REM ============================================================

echo.
echo Creando estructura de carpetas...
echo.

if not exist backups mkdir backups
if %errorlevel% equ 0 (
    echo ✓ Carpeta 'backups' creada
) else (
    echo ⚠ Carpeta 'backups' ya existe o no se pudo crear
)

if not exist documentos mkdir documentos
if %errorlevel% equ 0 (
    echo ✓ Carpeta 'documentos' creada
) else (
    echo ⚠ Carpeta 'documentos' ya existe o no se pudo crear
)

REM ============================================================
REM PASO 7: Crear script de ejecución
REM ============================================================

echo.
echo Creando acceso directo de ejecución...
echo.

(
echo @echo off
echo cd /d "%%~dp0"
echo python main.py
echo pause
) > ejecutar.bat

if exist ejecutar.bat (
    echo ✓ Archivo 'ejecutar.bat' creado
    echo   Puedes usar este archivo para abrir el programa fácilmente
) else (
    echo ⚠ No se pudo crear 'ejecutar.bat'
)

REM ============================================================
REM INSTALACIÓN COMPLETADA
REM ============================================================

echo.
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║  ✓ INSTALACIÓN COMPLETADA EXITOSAMENTE                        ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo Resumen de la instalación:
echo.
echo   ✓ Python %PYTHON_VERSION% detectado
echo   ✓ pip instalado y actualizado
echo   ✓ PyQt6 instalado (interfaz gráfica)
echo   ✓ pandas instalado (manejo de datos)
echo   ✓ matplotlib instalado (gráficos)
echo   ✓ openpyxl instalado (exportación Excel)
echo   ✓ Carpetas de respaldo y documentos creadas
echo   ✓ Script de ejecución creado
echo.
echo ═══════════════════════════════════════════════════════════════
echo  CÓMO EJECUTAR EL PROGRAMA:
echo ═══════════════════════════════════════════════════════════════
echo.
echo  Opción 1: Haz doble clic en 'ejecutar.bat'
echo  Opción 2: Ejecuta 'python main.py' en esta carpeta
echo.
echo ═══════════════════════════════════════════════════════════════
echo  DOCUMENTACIÓN DISPONIBLE:
echo ═══════════════════════════════════════════════════════════════
echo.
echo  • MANUAL_COMPLETO.md     - Manual detallado de usuario
echo  • GUIA_USUARIO.md        - Guía de funciones
echo  • CATEGORIAS.md          - Lista de categorías de casos
echo  • INSTALACION_WINDOWS.md - Esta guía de instalación
echo.
echo ═══════════════════════════════════════════════════════════════

REM ============================================================
REM OPCIÓN: Ejecutar el programa ahora
REM ============================================================

echo.
set /p EJECUTAR="¿Deseas ejecutar el programa ahora? (S/N): "

if /i "!EJECUTAR!"=="S" (
    echo.
    echo Iniciando el sistema...
    echo.
    python main.py
    if !errorlevel! neq 0 (
        echo.
        echo ✗ Error al ejecutar el programa
        echo Verifica que el archivo 'main.py' existe en esta carpeta
        echo.
        pause
        endlocal
        exit /b 1
    )
) else (
    echo.
    echo Para ejecutar el programa más tarde:
    echo - Haz doble clic en 'ejecutar.bat'
    echo - O ejecuta 'python main.py' en esta carpeta
    echo.
)

echo.
echo Presiona cualquier tecla para cerrar...
pause >nul
endlocal
exit /b 0
