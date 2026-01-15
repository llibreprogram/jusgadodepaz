#!/usr/bin/env python3
"""
Script para crear un instalador autoextraible de Windows.
Genera un solo archivo .bat que contiene todo el sistema embebido.
"""

import os
import base64
import sys
from pathlib import Path

# Archivos a incluir en el instalador
FILES_TO_INCLUDE = [
    'main.py',
    'requirements.txt',
    # Controllers
    'controllers/case_controller.py',
    'controllers/fiscal_history_controller.py',
    # Database
    'database/db.py',
    'database/documents_db.py',
    # Models
    'models/case.py',
    'models/fiscal_history.py',
    # Views
    'views/main_window.py',
    'views/fiscal_history_dialog.py',
    'views/fiscal_stats_dialog.py',
    # Services
    'services/document_service.py',
    # Utils
    'utils/backup_manager.py',
    'utils/export_service.py',
    'utils/graph_utils.py',
    'utils/import_service.py',
    'utils/notification_manager.py',
    'utils/responsive_utils.py',  # NUEVO: Sistema de diseño responsivo
]

# Directorios a crear
DIRS_TO_CREATE = [
    'controllers',
    'database',
    'models',
    'views',
    'services',
    'utils',
    'backups',
    'documentos',
    'documents',
    'exports',
]

def encode_file(filepath):
    """Codifica un archivo en base64"""
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
            return base64.b64encode(content).decode('ascii')
    except Exception as e:
        print(f"Error al codificar {filepath}: {e}")
        return None

def generate_installer():
    """Genera el instalador autoextraible"""
    
    print("=" * 70)
    print("GENERADOR DE INSTALADOR AUTOEXTRAIBLE")
    print("Sistema de Gestion de Casos - Version 3.0")
    print("=" * 70)
    print()
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('main.py'):
        print("ERROR: Este script debe ejecutarse desde la raiz del proyecto")
        print("Debe existir el archivo main.py en el directorio actual")
        sys.exit(1)
    
    # Codificar archivos
    print("[1/3] Codificando archivos del sistema...")
    encoded_files = {}
    
    for filepath in FILES_TO_INCLUDE:
        if os.path.exists(filepath):
            print(f"  • Codificando {filepath}...")
            encoded = encode_file(filepath)
            if encoded:
                encoded_files[filepath] = encoded
        else:
            print(f"  [!] Advertencia: {filepath} no encontrado, se omitira")
    
    print(f"\n[OK] {len(encoded_files)} archivos codificados correctamente\n")
    
    # Crear el script BAT
    print("[2/3] Generando instalador autoextraible...")
    
    bat_content = '''@echo off
setlocal EnableDelayedExpansion

REM Mantener ventana abierta siempre
REM No usar chcp para evitar problemas

:MAIN
color 0A
echo [DEBUG] Script iniciado correctamente
title Instalador Unico - Sistema de Gestion de Casos

REM ===================================================================
REM Sistema de Gestion de Casos Judiciales
REM Copyright (C) 2026 Rafael Llibre
REM Todos los derechos reservados.
REM ===================================================================

echo.
echo [DEBUG] Mostrando banner...
echo ================================================================
echo   INSTALADOR UNICO - SISTEMA DE GESTION DE CASOS
echo   Version 3.0 - Enero 2026
echo   Instalador autoextraible - Todo incluido
echo   Copyright (C) 2026 Rafael Llibre
echo ================================================================
echo.
echo [DEBUG] Banner mostrado correctamente

REM Preguntar ubicacion de instalacion
echo [DEBUG] Preguntando ubicacion...
echo Donde deseas instalar el sistema?
echo.
echo Opciones:
echo   1. Mis Documentos (Recomendado)
echo   2. C:\\SistemaGestionCasos
echo   3. Ubicacion personalizada
echo.
echo [DEBUG] Esperando seleccion del usuario...
set /p INSTALL_OPTION="Elige una opcion (1-3): "

echo [DEBUG] Opcion seleccionada: !INSTALL_OPTION!

if "!INSTALL_OPTION!"=="1" (
    echo [DEBUG] Opcion 1 - Mis Documentos
    set "INSTALL_DIR=%USERPROFILE%\\Documents\\SistemaGestionCasos"
) else if "!INSTALL_OPTION!"=="2" (
    echo [DEBUG] Opcion 2 - C:\\SistemaGestionCasos
    set "INSTALL_DIR=C:\\SistemaGestionCasos"
) else if "!INSTALL_OPTION!"=="3" (
    echo [DEBUG] Opcion 3 - Ubicacion personalizada
    set /p INSTALL_DIR="Ingresa la ruta completa: "
) else (
    echo [DEBUG] Opcion invalida, usando predeterminado
    echo Opcion invalida. Usando Documentos por defecto...
    set "INSTALL_DIR=%USERPROFILE%\\Documents\\SistemaGestionCasos"
)

echo.
echo [DEBUG] Directorio seleccionado: !INSTALL_DIR!
echo Se instalara en: !INSTALL_DIR!
echo.
set /p CONFIRMAR="Continuar? (S/N): "

echo [DEBUG] Respuesta: !CONFIRMAR!

if /i not "!CONFIRMAR!"=="S" (
    echo Instalacion cancelada.
    echo.
    echo [DEBUG] Usuario cancelo la instalacion
    pause
    endlocal
    exit /b 0
)

REM ============================================================
REM PASO 1: Crear directorio de instalacion
REM ============================================================

echo.
echo [1/7] Creando directorio de instalacion...
echo.

if not exist "!INSTALL_DIR!" (
    mkdir "!INSTALL_DIR!"
    if !errorlevel! neq 0 (
        echo ✗ ERROR: No se pudo crear el directorio
        echo Intenta ejecutar como Administrador
        echo.
        pause
        endlocal
        exit /b 1
    )
    echo [OK] Directorio creado: !INSTALL_DIR!
) else (
    echo [!] El directorio ya existe
    set /p SOBRESCRIBIR="Sobrescribir archivos existentes? (S/N): "
    if /i not "!SOBRESCRIBIR!"=="S" (
        echo Instalacion cancelada.
        echo.
        pause
        endlocal
        exit /b 0
    )
)

cd /d "!INSTALL_DIR!"
if !errorlevel! neq 0 (
    echo ✗ ERROR: No se pudo acceder al directorio
    echo.
    pause
    endlocal
    exit /b 1
)

REM ============================================================
REM PASO 2: Extraer archivos del sistema
REM ============================================================

echo.
echo [2/7] Extrayendo archivos del sistema...
echo.

'''

    # Agregar creacion de directorios
    bat_content += 'REM Crear estructura de directorios\n'
    for dir_name in DIRS_TO_CREATE:
        bat_content += f'if not exist "{dir_name}" mkdir "{dir_name}"\n'
    
    bat_content += '\necho [OK] Estructura de directorios creada\necho.\n\n'
    
    # Agregar extraccion de archivos
    bat_content += 'REM Extraer archivos codificados\n'
    bat_content += 'echo Extrayendo archivos Python...\n\n'
    
    for filepath, encoded_content in encoded_files.items():
        # Dividir el contenido en lineas de 8000 caracteres para evitar limites de cmd
        chunk_size = 8000
        chunks = [encoded_content[i:i+chunk_size] for i in range(0, len(encoded_content), chunk_size)]
        
        bat_content += f'REM Extraer {filepath}\n'
        bat_content += f'echo   • {filepath}\n'
        bat_content += f'set "TEMP_FILE=%TEMP%\\{filepath.replace("/", "_").replace("\\", "_")}.b64"\n'
        bat_content += 'if exist "%TEMP_FILE%" del "%TEMP_FILE%"\n'
        
        for chunk in chunks:
            bat_content += f'echo {chunk}>>"%TEMP_FILE%"\n'
        
        # Decodificar usando PowerShell
        # Usar comillas dobles escapadas para evitar problemas de parsing en cmd.exe
        output_path = filepath.replace("/", "\\")
        bat_content += f'powershell -Command "$content = [System.Convert]::FromBase64String((Get-Content \\"%TEMP_FILE%\\" -Raw)); [System.IO.File]::WriteAllBytes(\\"{output_path}\\", $content)"\n'
        bat_content += 'del "%TEMP_FILE%"\n\n'
    
    bat_content += 'echo.\necho [OK] Todos los archivos extraidos correctamente\necho.\n\n'
    
    # Agregar instalacion de Python
    bat_content += '''
REM ============================================================
REM PASO 3: Verificar/Instalar Python
REM ============================================================

echo [3/7] Verificando Python...
echo.

python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [!] Python no esta instalado
    echo Descargando Python 3.12...
    echo.
    
    set PYTHON_INSTALLER=python-3.12.1-amd64.exe
    set PYTHON_URL=https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe
    
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '!PYTHON_URL!' -OutFile '%TEMP%\\!PYTHON_INSTALLER!'"
    
    if !errorlevel! neq 0 (
        echo ✗ No se pudo descargar Python
        echo Por favor, instala Python manualmente desde python.org
        echo.
        pause
        endlocal
        exit /b 1
    )
    
    echo [OK] Python descargado
    echo Instalando Python...
    echo.
    
    "%TEMP%\\!PYTHON_INSTALLER!" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del "%TEMP%\\!PYTHON_INSTALLER!"
    
    echo [OK] Python instalado
    echo.
    echo IMPORTANTE: Cierra esta ventana y ejecuta el archivo nuevamente
    echo para que Windows reconozca Python.
    echo.
    echo Busca el archivo: !INSTALL_DIR!\\ejecutar.bat
    echo.
    pause
    endlocal
    exit /b 0
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python !PYTHON_VERSION! detectado
echo.

REM ============================================================
REM PASO 4: Instalar dependencias
REM ============================================================

echo [4/7] Instalando librerias necesarias...
echo.
echo Esto puede tomar 5-10 minutos...
echo.

if exist requirements.txt (
    pip install -r requirements.txt --quiet
) else (
    pip install PyQt6 pandas matplotlib openpyxl --quiet
)

if !errorlevel! neq 0 (
    echo ✗ Error instalando librerias
    echo.
    pause
    endlocal
    exit /b 1
)

echo [OK] Librerias instaladas
echo.

REM ============================================================
REM PASO 5: Verificar instalacion
REM ============================================================

echo [5/7] Verificando instalacion...
echo.

python -c "import PyQt6" 2>nul
if !errorlevel! neq 0 (
    echo ✗ PyQt6 no se instalo correctamente
    echo.
    pause
    endlocal
    exit /b 1
)
echo [OK] PyQt6

python -c "import pandas" 2>nul
if !errorlevel! neq 0 (
    echo ✗ pandas no se instalo correctamente
    echo.
    pause
    endlocal
    exit /b 1
)
echo [OK] pandas

python -c "import matplotlib" 2>nul
if !errorlevel! neq 0 (
    echo ✗ matplotlib no se instalo correctamente
    echo.
    pause
    endlocal
    exit /b 1
)
echo [OK] matplotlib

python -c "import openpyxl" 2>nul
if !errorlevel! neq 0 (
    echo ✗ openpyxl no se instalo correctamente
    echo.
    pause
    endlocal
    exit /b 1
)
echo [OK] openpyxl
echo.

REM ============================================================
REM PASO 6: Crear acceso directo
REM ============================================================

echo [6/7] Creando acceso directo...
echo.

(
echo @echo off
echo cd /d "%%~dp0"
echo python main.py
echo if %%errorlevel%% neq 0 pause
) > ejecutar.bat

echo [OK] Archivo ejecutar.bat creado
echo.

REM ============================================================
REM PASO 7: Crear acceso directo en escritorio
REM ============================================================

echo [7/7] Crear acceso directo en el escritorio?
set /p CREATE_SHORTCUT="(S/N): "

if /i "!CREATE_SHORTCUT!"=="S" (
    set "SCRIPT=%TEMP%\\create_shortcut.vbs"
    (
        echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
        echo sLinkFile = oWS.SpecialFolders^("Desktop"^) ^& "\\Sistema Gestion Casos.lnk"
        echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
        echo oLink.TargetPath = "!INSTALL_DIR!\\ejecutar.bat"
        echo oLink.WorkingDirectory = "!INSTALL_DIR!"
        echo oLink.Description = "Sistema de Gestion de Casos Judiciales"
        echo oLink.Save
    ) > "!SCRIPT!"
    cscript //nologo "!SCRIPT!"
    del "!SCRIPT!"
    echo [OK] Acceso directo creado en el escritorio
)

REM ============================================================
REM INSTALACION COMPLETADA
REM ============================================================

echo.
echo.
echo =================================================================
echo |  [OK] INSTALACION COMPLETADA EXITOSAMENTE                        |
echo =================================================================
echo.
echo Ubicacion: !INSTALL_DIR!
echo.
echo ===============================================================
echo  COMO EJECUTAR:
echo ===============================================================
echo.
echo  • Doble clic en: ejecutar.bat
echo  • O acceso directo en el escritorio
echo.
echo ===============================================================

set /p EJECUTAR_AHORA="Ejecutar el programa ahora? (S/N): "

if /i "!EJECUTAR_AHORA!"=="S" (
    echo.
    echo Iniciando sistema...
    python main.py
)

echo.
pause
endlocal
exit /b 0
'''
    
    # Guardar el instalador
    output_file = 'InstaladorUnico_SistemaGestionCasos.bat'
    
    print(f"  • Escribiendo {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(bat_content)
    
    file_size = os.path.getsize(output_file) / 1024 / 1024
    print(f"\n[OK] Instalador generado: {output_file}")
    print(f"  Tamano: {file_size:.2f} MB\n")
    
    # Instrucciones
    print("[3/3] Instrucciones de uso:")
    print("=" * 70)
    print()
    print(f"[OK] Instalador creado: {output_file}")
    print()
    print("COMO USAR:")
    print("  1. Copia el archivo a una USB o envialo por correo")
    print("  2. En Windows, haz doble clic en el archivo")
    print("  3. Sigue las instrucciones en pantalla")
    print("  4. El instalador:")
    print("     • Preguntara donde instalarlo")
    print("     • Extraera todos los archivos")
    print("     • Instalara Python si no existe")
    print("     • Instalara todas las librerias")
    print("     • Creara acceso directo")
    print("     • Ejecutara el programa")
    print()
    print("VENTAJAS:")
    print("  [OK] Un solo archivo para distribuir")
    print("  [OK] Instalacion 100% automatica")
    print("  [OK] No requiere archivos adicionales")
    print("  [OK] Facil de enviar por correo o USB")
    print()
    print("=" * 70)
    print("\n[OK] PROCESO COMPLETADO\n")

if __name__ == '__main__':
    try:
        generate_installer()
    except KeyboardInterrupt:
        print("\n\nProceso cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
