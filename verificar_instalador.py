#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador del Instalador BAT
Valida que el instalador esté correctamente generado sin ejecutarlo en Windows
"""

import re
import base64
import os
from pathlib import Path

def verificar_sintaxis_bat(bat_file):
    """Verifica la sintaxis básica del archivo BAT"""
    print("\n" + "="*70)
    print("🔍 VERIFICANDO SINTAXIS DEL ARCHIVO BAT")
    print("="*70)
    
    with open(bat_file, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    errores = []
    advertencias = []
    
    # Verificar estructura básica
    if not content.startswith('@echo off'):
        errores.append("El archivo debe comenzar con '@echo off'")
    
    if 'setlocal EnableDelayedExpansion' not in content:
        errores.append("Falta 'setlocal EnableDelayedExpansion'")
    
    # Verificar comandos PowerShell
    powershell_cmds = re.findall(r'powershell -Command "(.*?)"', content, re.DOTALL)
    print(f"\n✅ Encontrados {len(powershell_cmds)} comandos PowerShell")
    
    # Verificar que las comillas estén correctamente escapadas
    comillas_incorrectas = 0
    for i, cmd in enumerate(powershell_cmds, 1):
        if "'" in cmd and '\\"' not in cmd:
            advertencias.append(f"Comando PowerShell #{i} podría tener problemas con comillas simples")
            comillas_incorrectas += 1
    
    if comillas_incorrectas == 0:
        print("✅ Todas las comillas en comandos PowerShell están correctamente escapadas")
    else:
        print(f"⚠️  {comillas_incorrectas} comandos PowerShell con posibles problemas de comillas")
    
    # Verificar uso de variables con delayed expansion
    if_blocks = re.findall(r'if\s+.*?\(', content, re.IGNORECASE)
    variables_correctas = content.count('!errorlevel!') + content.count('!INSTALL_')
    
    print(f"✅ Uso de variables con delayed expansion: {variables_correctas} instancias")
    
    # Verificar estructura de IF/ELSE
    open_parens = content.count('(')
    close_parens = content.count(')')
    if open_parens != close_parens:
        errores.append(f"Paréntesis desbalanceados: {open_parens} abiertos vs {close_parens} cerrados")
    else:
        print(f"✅ Paréntesis balanceados: {open_parens} pares")
    
    return errores, advertencias, len(powershell_cmds)

def verificar_base64(bat_file):
    """Verifica que el contenido Base64 sea válido"""
    print("\n" + "="*70)
    print("🔍 VERIFICANDO CODIFICACIÓN BASE64")
    print("="*70)
    
    with open(bat_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraer bloques de Base64
    base64_pattern = r'echo ([A-Za-z0-9+/=]+)>>'
    base64_chunks = re.findall(base64_pattern, content)
    
    print(f"\n📦 Encontrados {len(base64_chunks)} chunks de Base64")
    
    errores = []
    archivos_encontrados = 0
    
    # Agrupar chunks por archivo
    temp_file_pattern = r'set "TEMP_FILE=%TEMP%\\([^"]+)"'
    temp_files = re.findall(temp_file_pattern, content)
    
    print(f"📄 Archivos a extraer: {len(temp_files)}")
    
    for i, temp_file in enumerate(temp_files, 1):
        # Extraer el nombre original
        nombre_archivo = temp_file.replace('.b64', '').replace('_', '/')
        
        # Buscar los chunks correspondientes
        pattern = f'set "TEMP_FILE=%TEMP%\\\\{re.escape(temp_file)}".*?(?=set "TEMP_FILE=|REM Extraer|echo\\.)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            file_section = match.group(0)
            file_chunks = re.findall(r'echo ([A-Za-z0-9+/=]+)>>', file_section)
            
            if file_chunks:
                # Concatenar todos los chunks
                full_base64 = ''.join(file_chunks)
                
                # Intentar decodificar
                try:
                    decoded = base64.b64decode(full_base64)
                    print(f"  ✅ {nombre_archivo:40} - {len(decoded):,} bytes")
                    archivos_encontrados += 1
                except Exception as e:
                    errores.append(f"Error decodificando {nombre_archivo}: {str(e)}")
                    print(f"  ❌ {nombre_archivo:40} - ERROR")
    
    return errores, archivos_encontrados

def verificar_comandos_powershell(bat_file):
    """Verifica que los comandos PowerShell estén bien formados"""
    print("\n" + "="*70)
    print("🔍 VERIFICANDO COMANDOS POWERSHELL")
    print("="*70)
    
    with open(bat_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraer todos los comandos PowerShell (capturando contenido con comillas escapadas)
    powershell_pattern = r'powershell -Command "([^"]*(?:\\.[^"]*)*)"'
    comandos = re.findall(powershell_pattern, content)
    
    errores = []
    advertencias = []
    
    for i, cmd in enumerate(comandos, 1):
        print(f"\n📋 Comando #{i}:")
        
        # Verificar estructura básica para Base64
        if 'FromBase64String' in cmd:
            # Debe tener Get-Content con ruta
            if '\\"' not in cmd:
                errores.append(f"Comando #{i}: Faltan comillas escapadas")
                print(f"  ❌ Comillas no escapadas")
            else:
                print(f"  ✅ Comillas correctamente escapadas")
            
            # Debe tener WriteAllBytes
            if 'WriteAllBytes' not in cmd:
                errores.append(f"Comando #{i}: Falta WriteAllBytes")
                print(f"  ❌ Falta WriteAllBytes")
            else:
                print(f"  ✅ WriteAllBytes presente")
            
            # Extraer ruta de salida
            output_match = re.search(r'WriteAllBytes\(\\"([^"]+)\\"', cmd)
            if output_match:
                output_path = output_match.group(1)
                print(f"  📁 Salida: {output_path}")
            
        elif 'Invoke-WebRequest' in cmd:
            print(f"  🌐 Descarga de archivo")
            if '!PYTHON_URL!' in cmd:
                print(f"  ✅ Variable de URL presente")
        else:
            advertencias.append(f"Comando #{i}: Tipo desconocido")
            print(f"  ⚠️  Tipo de comando no reconocido")
    
    return errores, advertencias

def verificar_estructura_archivos(bat_file):
    """Verifica que se generen todos los archivos y directorios necesarios"""
    print("\n" + "="*70)
    print("🔍 VERIFICANDO ESTRUCTURA DE ARCHIVOS")
    print("="*70)
    
    with open(bat_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar creación de directorios
    mkdir_pattern = r'if not exist "([^"]+)" mkdir'
    directorios = re.findall(mkdir_pattern, content)
    
    print(f"\n📁 Directorios a crear: {len(directorios)}")
    for dir_name in sorted(set(directorios)):
        print(f"  • {dir_name}")
    
    # Buscar archivos a extraer
    extract_pattern = r'echo\s+•\s+(.+)'
    archivos = re.findall(extract_pattern, content)
    
    print(f"\n📄 Archivos a extraer: {len(archivos)}")
    for archivo in archivos:
        print(f"  • {archivo}")
    
    return len(directorios), len(archivos)

def simular_extraccion(bat_file, output_dir='test_extraction'):
    """Simula la extracción de archivos para verificar que funcionen"""
    print("\n" + "="*70)
    print("🧪 SIMULANDO EXTRACCIÓN DE ARCHIVOS")
    print("="*70)
    
    # Crear directorio temporal
    output_path = Path(output_dir)
    if output_path.exists():
        import shutil
        shutil.rmtree(output_path)
    output_path.mkdir()
    
    with open(bat_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraer información de archivos
    temp_file_pattern = r'set "TEMP_FILE=%TEMP%\\([^"]+)"'
    temp_files = re.findall(temp_file_pattern, content)
    
    exitos = 0
    errores = []
    
    for temp_file in temp_files:
        nombre_archivo = temp_file.replace('.b64', '').replace('_', '/')
        
        # Buscar los chunks correspondientes
        pattern = f'set "TEMP_FILE=%TEMP%\\\\{re.escape(temp_file)}".*?(?=set "TEMP_FILE=|REM Extraer|echo\\.)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            file_section = match.group(0)
            file_chunks = re.findall(r'echo ([A-Za-z0-9+/=]+)>>', file_section)
            
            if file_chunks:
                full_base64 = ''.join(file_chunks)
                
                try:
                    decoded = base64.b64decode(full_base64)
                    
                    # Crear archivo
                    file_path = output_path / nombre_archivo.replace('\\', '/')
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    file_path.write_bytes(decoded)
                    
                    print(f"  ✅ {nombre_archivo:40} - {len(decoded):,} bytes")
                    exitos += 1
                    
                except Exception as e:
                    errores.append(f"{nombre_archivo}: {str(e)}")
                    print(f"  ❌ {nombre_archivo:40} - ERROR: {str(e)}")
    
    print(f"\n📊 Resultado: {exitos}/{len(temp_files)} archivos extraídos correctamente")
    
    if exitos == len(temp_files):
        print(f"✅ Todos los archivos se extrajeron exitosamente en: {output_path.absolute()}")
    
    return exitos, errores

def main():
    bat_file = 'InstaladorUnico_SistemaGestionCasos.bat'
    
    if not os.path.exists(bat_file):
        print(f"❌ Error: No se encontró el archivo {bat_file}")
        return
    
    print("\n" + "="*70)
    print("🔧 VERIFICADOR DE INSTALADOR BAT")
    print("Sistema de Gestión de Casos")
    print("="*70)
    
    file_size = os.path.getsize(bat_file) / 1024
    print(f"\n📁 Archivo: {bat_file}")
    print(f"📏 Tamaño: {file_size:.2f} KB")
    
    # 1. Verificar sintaxis
    errores_sintaxis, advertencias_sintaxis, num_powershell = verificar_sintaxis_bat(bat_file)
    
    # 2. Verificar Base64
    errores_base64, num_archivos = verificar_base64(bat_file)
    
    # 3. Verificar comandos PowerShell
    errores_ps, advertencias_ps = verificar_comandos_powershell(bat_file)
    
    # 4. Verificar estructura
    num_dirs, num_files = verificar_estructura_archivos(bat_file)
    
    # 5. Simular extracción
    print("\n" + "="*70)
    respuesta = input("¿Deseas simular la extracción de archivos? (S/n): ").strip().lower()
    if respuesta in ['s', 'si', 'yes', '']:
        exitos, errores_ext = simular_extraccion(bat_file)
    else:
        exitos = 0
        errores_ext = []
    
    # Resumen final
    print("\n" + "="*70)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("="*70)
    
    total_errores = len(errores_sintaxis) + len(errores_base64) + len(errores_ps) + len(errores_ext)
    total_advertencias = len(advertencias_sintaxis) + len(advertencias_ps)
    
    print(f"\n✅ Comandos PowerShell: {num_powershell}")
    print(f"✅ Archivos codificados: {num_archivos}")
    print(f"✅ Directorios a crear: {num_dirs}")
    print(f"✅ Archivos a extraer: {num_files}")
    
    if exitos > 0:
        print(f"✅ Archivos extraídos exitosamente: {exitos}/{num_archivos}")
    
    if total_errores == 0:
        print("\n" + "🎉 " * 10)
        print("✅ ¡VERIFICACIÓN EXITOSA! El instalador está correctamente generado.")
        print("🎉 " * 10)
        print("\n💡 El instalador debería funcionar correctamente en Windows.")
    else:
        print(f"\n❌ Se encontraron {total_errores} errores:")
        for error in errores_sintaxis + errores_base64 + errores_ps + errores_ext:
            print(f"  • {error}")
    
    if total_advertencias > 0:
        print(f"\n⚠️  Advertencias ({total_advertencias}):")
        for adv in advertencias_sintaxis + advertencias_ps:
            print(f"  • {adv}")
    
    print("\n" + "="*70)

if __name__ == '__main__':
    main()
