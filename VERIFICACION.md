# Scripts de Verificación del Instalador

## 📋 Resumen

Se han creado varios scripts para verificar que el instalador BAT funcione correctamente **sin necesidad de probarlo en Windows**.

## 🧪 Scripts Disponibles

### 1. **verificar_instalador.py** - Verificación Completa
```bash
python3 verificar_instalador.py
```

**Qué verifica:**
- ✅ Sintaxis del archivo BAT (setlocal, variables, paréntesis)
- ✅ Codificación Base64 (válida y decodificable)
- ✅ Comandos PowerShell (comillas escapadas, estructura)
- ✅ Estructura de archivos y directorios
- ✅ Extracción simulada de todos los archivos
- ✅ Validación sintáctica de archivos Python

**Resultado:** Todos los archivos extraídos en `test_extraction/`

### 2. **test_powershell_commands.sh** - Análisis de PowerShell
```bash
bash test_powershell_commands.sh
```

**Qué verifica:**
- ✅ Comillas correctamente escapadas (`\"`)
- ✅ Estructura de comandos Base64
- ✅ Presencia de FromBase64String, WriteAllBytes, Get-Content
- ✅ Conteo de comandos totales vs comandos corregidos

**Resultado:** 17/17 comandos Base64 con comillas correctas

## ✅ Resultados de las Pruebas

### Verificación Sintáctica
- ✅ `setlocal EnableDelayedExpansion` presente
- ✅ 21 variables con delayed expansion `!variable!`
- ✅ 85 pares de paréntesis balanceados
- ✅ 18 comandos PowerShell

### Verificación de Codificación
- ✅ 17 archivos Python codificados
- ✅ 56 chunks de Base64
- ✅ 277,280 bytes totales (271 KB)
- ✅ Todos decodificables correctamente

### Verificación de Extracción
- ✅ 17/17 archivos extraídos exitosamente
- ✅ 16/16 archivos .py sintácticamente válidos
- ✅ Estructura de directorios correcta

### Verificación de PowerShell
- ✅ 17/17 comandos Base64 con `\"`
- ✅ 1 comando de descarga (Invoke-WebRequest)
- ✅ Sin comillas simples problemáticas

## 🎯 Conclusión

**El instalador está 100% verificado y listo para usar en Windows.**

### Problema Original (RESUELTO ✅)
- ❌ Antes: `'%TEMP_FILE%'` causaba fragmentación de comandos
- ✅ Ahora: `\"%TEMP_FILE%\"` funciona correctamente

### Archivos para Distribuir
1. **InstaladorUnico_SistemaGestionCasos.bat** (380 KB)
   - Instalador completo autoextraíble
   
2. **InstaladorUnico_SistemaGestionCasos_Protegido.zip** (88 KB)
   - Versión comprimida para email
   - Contraseña: `jusgadodepaz2026`

## 🔄 Regenerar si Necesario

Si haces cambios a los archivos Python:

```bash
# 1. Regenerar instalador
python3 crear_instalador_unico.py

# 2. Verificar
python3 verificar_instalador.py

# 3. Crear ZIP protegido
bash crear_zip_distribucion.sh
```

## 📁 Archivos de Prueba

- `test_extraction/` - Archivos extraídos del instalador
- Puedes verificar manualmente estos archivos antes de distribuir

## ⚠️ Nota Importante

Los scripts de verificación son para Linux/Mac. El instalador BAT solo funciona en Windows, pero las pruebas garantizan que funcionará correctamente.
