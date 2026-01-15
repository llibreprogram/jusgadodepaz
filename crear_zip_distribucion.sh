#!/bin/bash
# Script para crear ZIP protegido del Instalador Único
# Copyright © 2026 Rafael Llibre

PASSWORD="jusgadodepaz2026"
ARCHIVO="InstaladorUnico_SistemaGestionCasos.bat"
ZIP_SALIDA="InstaladorUnico_SistemaGestionCasos_Protegido.zip"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     CREADOR DE ZIP PROTEGIDO PARA DISTRIBUCIÓN               ║"
echo "║     Sistema de Gestión de Casos v3.0                         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Verificar que existe el archivo
if [ ! -f "$ARCHIVO" ]; then
    echo "❌ Error: No se encontró $ARCHIVO"
    echo "   Ejecuta primero: python3 crear_instalador_unico.py"
    exit 1
fi

echo "📦 Archivo a comprimir: $ARCHIVO"
echo "🔐 Contraseña: $PASSWORD"
echo "📁 ZIP de salida: $ZIP_SALIDA"
echo ""

# Intentar con 7z primero
if command -v 7z &> /dev/null; then
    echo "🔧 Usando 7-Zip..."
    7z a -p"$PASSWORD" -tzip -mem=AES256 "$ZIP_SALIDA" "$ARCHIVO" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✅ ZIP creado exitosamente con 7-Zip"
    else
        echo "❌ Error al crear ZIP con 7-Zip"
        exit 1
    fi

# Si no hay 7z, intentar con zip
elif command -v zip &> /dev/null; then
    echo "🔧 Usando zip..."
    zip -P "$PASSWORD" "$ZIP_SALIDA" "$ARCHIVO" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✅ ZIP creado exitosamente con zip"
    else
        echo "❌ Error al crear ZIP con zip"
        exit 1
    fi

else
    echo "❌ Error: No se encontró 7z ni zip"
    echo ""
    echo "Instala una de estas herramientas:"
    echo "  • Ubuntu/Debian: sudo apt install p7zip-full"
    echo "  • Ubuntu/Debian: sudo apt install zip"
    echo "  • Fedora: sudo dnf install p7zip"
    echo "  • Arch: sudo pacman -S p7zip"
    exit 1
fi

# Mostrar información del archivo creado
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ ARCHIVO LISTO PARA DISTRIBUCIÓN"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📁 Archivo: $ZIP_SALIDA"

if [ -f "$ZIP_SALIDA" ]; then
    TAMANIO=$(du -h "$ZIP_SALIDA" | cut -f1)
    echo "📏 Tamaño: $TAMANIO"
fi

echo "🔐 Contraseña: $PASSWORD"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "📧 CÓMO USAR:"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "1. Adjunta $ZIP_SALIDA a tu email"
echo "2. Incluye en el mensaje:"
echo ""
echo "   ┌─────────────────────────────────────────────────────┐"
echo "   │ Contraseña para extraer: $PASSWORD     │"
echo "   │                                                     │"
echo "   │ Pasos:                                              │"
echo "   │ 1. Extrae el ZIP con la contraseña                  │"
echo "   │ 2. Doble clic en el archivo .bat                    │"
echo "   │ 3. Sigue las instrucciones                          │"
echo "   └─────────────────────────────────────────────────────┘"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ ¡Listo para enviar por Gmail, Outlook, etc!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
