#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Ejecutable Windows (.exe)
Convierte el sistema en un solo archivo ejecutable para Windows
"""

import os
import sys
import shutil
from pathlib import Path

def verificar_pyinstaller():
    """Verifica si PyInstaller está instalado"""
    try:
        import PyInstaller
        print("✅ PyInstaller ya está instalado")
        return True
    except ImportError:
        print("❌ PyInstaller no está instalado")
        print("\n📦 Instalando PyInstaller...")
        os.system(f"{sys.executable} -m pip install pyinstaller")
        return True

def crear_spec_file():
    """Crea el archivo .spec para PyInstaller"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('views', 'views'),
        ('models', 'models'),
        ('controllers', 'controllers'),
        ('database', 'database'),
        ('services', 'services'),
        ('utils', 'utils'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'matplotlib',
        'pandas',
        'openpyxl',
        'sqlite3',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SistemaGestionCasos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin ventana de consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Puedes agregar un .ico aquí
)
"""
    
    with open('SistemaGestionCasos.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Archivo .spec creado")

def generar_icono():
    """Genera un archivo de icono simple si no existe"""
    # Por ahora solo crear un placeholder
    # En producción podrías convertir una imagen a .ico
    pass

def crear_ejecutable():
    """Crea el ejecutable con PyInstaller"""
    print("\n" + "="*70)
    print("🔨 GENERANDO EJECUTABLE PARA WINDOWS")
    print("="*70)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('main.py'):
        print("❌ Error: No se encontró main.py en el directorio actual")
        return False
    
    print("\n📦 Archivos del proyecto encontrados:")
    for dir_name in ['views', 'models', 'controllers', 'database', 'services', 'utils']:
        if os.path.exists(dir_name):
            print(f"  ✅ {dir_name}/")
    
    # Crear archivo .spec
    print("\n🔧 Creando configuración...")
    crear_spec_file()
    
    # Ejecutar PyInstaller
    print("\n⚙️  Compilando ejecutable (esto puede tomar varios minutos)...")
    print("    Por favor espera...\n")
    
    result = os.system('pyinstaller --clean --noconfirm SistemaGestionCasos.spec')
    
    if result == 0:
        print("\n" + "="*70)
        print("✅ ¡EJECUTABLE CREADO EXITOSAMENTE!")
        print("="*70)
        
        exe_path = Path('dist/SistemaGestionCasos.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\n📁 Archivo: dist/SistemaGestionCasos.exe")
            print(f"📏 Tamaño: {size_mb:.1f} MB")
            print("\n🎯 CÓMO DISTRIBUIR:")
            print("  1. Copia el archivo SistemaGestionCasos.exe")
            print("  2. Distribúyelo por USB, email o nube")
            print("  3. Los usuarios solo hacen doble clic")
            print("  4. No necesitan instalar nada más")
            
            print("\n💡 VENTAJAS:")
            print("  ✅ Un solo archivo")
            print("  ✅ No requiere Python instalado")
            print("  ✅ No requiere permisos de administrador")
            print("  ✅ Funciona en Windows 10/11")
            print("  ✅ Portable (USB, red, etc.)")
        
        return True
    else:
        print("\n❌ Error al crear el ejecutable")
        return False

def crear_version_portable():
    """Crea una carpeta portable con el ejecutable y recursos"""
    print("\n📦 Creando versión portable...")
    
    portable_dir = Path('SistemaGestionCasos_Portable')
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    portable_dir.mkdir()
    
    # Copiar ejecutable
    exe_src = Path('dist/SistemaGestionCasos.exe')
    if exe_src.exists():
        shutil.copy(exe_src, portable_dir / 'SistemaGestionCasos.exe')
    
    # Crear README
    readme = """
SISTEMA DE GESTIÓN DE CASOS JUDICIALES
======================================

INSTRUCCIONES DE USO:
--------------------

1. Haz doble clic en SistemaGestionCasos.exe
2. El sistema se iniciará automáticamente
3. Los datos se guardarán en la carpeta donde está el ejecutable

CARACTERÍSTICAS:
---------------

✓ No requiere instalación
✓ No requiere Python
✓ No requiere conexión a internet
✓ Funciona desde USB
✓ Los datos son 100% locales

RESPALDOS:
---------

Los respaldos automáticos se crean en la carpeta "backups"
Te recomendamos copiar esta carpeta periódicamente.

SOPORTE:
--------

Para cualquier consulta o problema, contacta con el desarrollador.

Copyright © 2026 - Sistema de Gestión de Casos Judiciales
"""
    
    (portable_dir / 'LEEME.txt').write_text(readme, encoding='utf-8')
    
    # Crear carpetas necesarias
    (portable_dir / 'backups').mkdir()
    (portable_dir / 'exports').mkdir()
    (portable_dir / 'documentos').mkdir()
    
    print(f"✅ Versión portable creada en: {portable_dir}/")
    print(f"\n💡 Puedes comprimir esta carpeta en ZIP para distribuir")

def main():
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║   GENERADOR DE EJECUTABLE WINDOWS (.exe)                     ║")
    print("║   Sistema de Gestión de Casos Judiciales                     ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    
    # Verificar PyInstaller
    if not verificar_pyinstaller():
        print("❌ No se pudo instalar PyInstaller")
        return
    
    print("\n⚠️  IMPORTANTE:")
    print("   • Este proceso se debe ejecutar EN WINDOWS")
    print("   • El ejecutable resultante solo funciona en Windows")
    print("   • Si estás en Linux/Mac, necesitas una VM de Windows")
    print()
    
    respuesta = input("¿Continuar? (S/n): ").strip().lower()
    if respuesta and respuesta not in ['s', 'si', 'yes', 'y']:
        print("Cancelado.")
        return
    
    # Crear ejecutable
    if crear_ejecutable():
        # Crear versión portable
        respuesta = input("\n¿Crear versión portable con carpetas? (S/n): ").strip().lower()
        if not respuesta or respuesta in ['s', 'si', 'yes', 'y']:
            crear_version_portable()
        
        print("\n" + "="*70)
        print("✅ PROCESO COMPLETADO")
        print("="*70)
        print("\nARCHIVOS GENERADOS:")
        print("  📁 dist/SistemaGestionCasos.exe - Ejecutable principal")
        if Path('SistemaGestionCasos_Portable').exists():
            print("  📁 SistemaGestionCasos_Portable/ - Versión portable completa")
        print("\n🎉 ¡Listo para distribuir!")

if __name__ == '__main__':
    main()
