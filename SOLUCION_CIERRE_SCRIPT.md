# 🔧 Solución: Script se Cierra Como Administrador

**Copyright © 2026 Rafael Llibre. Todos los derechos reservados.**

## ❌ Problema

Cuando ejecutas `instalar_windows.bat` como Administrador, el script se cierra inmediatamente sin mostrar errores.

## 🔍 Causas Comunes

### 1. Variables de Entorno con Administrador
Cuando ejecutas como administrador, el contexto de las variables de entorno cambia y puede que Python no se detecte correctamente en el PATH del administrador, aunque esté instalado para el usuario normal.

### 2. Expansión de Variables Diferida
Windows Batch tiene problemas con variables cuando se usa `%variable%` en lugar de `!variable!` dentro de bloques IF o FOR.

### 3. Errores Silenciosos
Si hay un error de sintaxis o lógica, el script se cierra sin mostrar nada.

---

## ✅ Soluciones Implementadas

### 📝 Cambio 1: Modo CHILD para Captura de Errores

```batch
if "%1"=="CHILD" (
    shift
    goto MAIN
)

REM Ejecutar en modo con captura de errores
cmd /k "%~f0 CHILD %*"
exit /b

:MAIN
```

**Qué hace:** Ejecuta el script en un cmd persistente que NO se cierra al terminar.

### 📝 Cambio 2: EnableDelayedExpansion

```batch
setlocal EnableDelayedExpansion
```

**Qué hace:** Permite usar `!variable!` en lugar de `%variable%` para expansión correcta dentro de bloques.

### 📝 Cambio 3: Verificación de Administrador

```batch
net session >nul 2>&1
if %errorlevel% == 0 (
    echo ✓ Ejecutando como Administrador
) else (
    echo ⚠ No se está ejecutando como Administrador
)
```

**Qué hace:** Informa al usuario si tiene permisos de administrador.

### 📝 Cambio 4: Pausas en Puntos Críticos

```batch
if !DOWNLOAD_RESULT! neq 0 (
    echo.
    echo ✗ ERROR: No se pudo descargar Python
    echo.
    pause
    exit /b 1
)
```

**Qué hace:** Pausa el script cuando hay error para que veas el mensaje.

### 📝 Cambio 5: Uso de Variables con !

```batch
REM Antes (malo):
if %errorlevel% neq 0

REM Después (bueno):
if !errorlevel! neq 0
```

**Qué hace:** Evalúa correctamente las variables dentro de bloques IF/FOR.

### 📝 Cambio 6: Endlocal al Final

```batch
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul
endlocal
exit /b 0
```

**Qué hace:** Cierra correctamente el entorno local de variables.

---

## 🎯 Cómo Usar Ahora

### Opción 1: Normal (Sin Administrador) - RECOMENDADO

```
1. Haz doble clic en instalar_windows.bat
2. El script se abre en una ventana persistente
3. Si necesita instalar Python, te avisará
```

**Ventajas:**
- ✅ Funciona la mayoría de las veces
- ✅ Instala Python para tu usuario
- ✅ Menos problemas con permisos

### Opción 2: Como Administrador (Si es necesario)

```
1. Clic derecho en instalar_windows.bat
2. "Ejecutar como administrador"
3. Ahora NO se cierra automáticamente
4. Verás mensajes de error si algo falla
```

**Cuándo usar:**
- ⚠️ Solo si la instalación normal falla
- ⚠️ Si necesitas instalar para todos los usuarios
- ⚠️ Si hay problemas de permisos

---

## 🐛 Si Aún Tienes Problemas

### Problema: "Python no se detecta"

**Solución:**

1. Abre CMD **normal** (no como administrador)
2. Ejecuta: `python --version`
3. Si funciona aquí pero no en el script:

```batch
REM El problema es el PATH del administrador
REM Solución: Instala Python manualmente con "Add to PATH"
```

### Problema: "Error al descargar Python"

**Solución:**

```
1. Verifica conexión a internet
2. Desactiva temporalmente el antivirus/firewall
3. O descarga Python manualmente:
   https://www.python.org/downloads/
4. Durante instalación, MARCA "Add Python to PATH"
5. Ejecuta el script de nuevo
```

### Problema: "El script sigue cerrándose"

**Solución Alternativa - Ejecutar desde CMD:**

```
1. Presiona Win + R
2. Escribe: cmd
3. Presiona Enter
4. Arrastra instalar_windows.bat a la ventana CMD
5. Presiona Enter
6. Ahora verás todos los errores
```

### Problema: "Instalación de librerías falla"

**Solución:**

```batch
REM Ejecuta manualmente:
python -m pip install --upgrade pip
python -m pip install PyQt6 pandas matplotlib openpyxl
```

---

## 📊 Comparación: Normal vs Administrador

| Aspecto | Ejecución Normal | Como Administrador |
|---------|------------------|-------------------|
| **PATH** | Usuario actual | Sistema completo |
| **Permisos** | Usuario | Máximos |
| **Problemas** | Pocos | Más frecuentes |
| **Recomendado** | ✅ Sí | ⚠️ Solo si necesario |

---

## 🎓 Explicación Técnica

### ¿Por qué EnableDelayedExpansion?

Windows Batch evalúa variables **antes** de ejecutar un bloque completo. Esto causa problemas:

```batch
REM Sin EnableDelayedExpansion:
set VAR=1
if %VAR%==1 (
    set VAR=2
    if %VAR%==2 echo Nunca se ejecuta  REM %VAR% sigue siendo 1
)

REM Con EnableDelayedExpansion:
set VAR=1
if !VAR!==1 (
    set VAR=2
    if !VAR!==2 echo Ahora SÍ funciona  REM !VAR! se evalúa en tiempo real
)
```

### ¿Por qué cmd /k?

```batch
cmd /k  = Ejecuta comando y MANTIENE la ventana abierta
cmd /c  = Ejecuta comando y CIERRA la ventana
```

El script usa `cmd /k` para que puedas ver errores antes de que se cierre.

---

## 🔄 Actualización Automática

Si descargas una versión nueva de `instalar_windows.bat`, automáticamente tendrá todas estas mejoras.

---

## 📞 Soporte

Si el problema persiste:

1. **Captura de pantalla** del error (ahora se quedará visible)
2. **Copia el mensaje** de error
3. **Verifica**:
   - ¿Tienes internet?
   - ¿Antivirus activo?
   - ¿Python ya instalado? (`python --version` en CMD)

---

## ✅ Cambios Realizados en instalar_windows.bat

**Versión**: 3.0.1  
**Fecha**: Enero 8, 2026  
**Autor**: Rafael Llibre

### Mejoras:

1. ✅ EnableDelayedExpansion para variables
2. ✅ Modo CHILD para captura de errores
3. ✅ Pausas en todos los puntos de error
4. ✅ Verificación de permisos de administrador
5. ✅ Manejo mejorado de errorlevel
6. ✅ Uso de !variable! en lugar de %variable%
7. ✅ Endlocal al final
8. ✅ Mensajes de error más descriptivos
9. ✅ Verificación de archivo descargado
10. ✅ Uso de start /wait para instalación

---

**El script ya NO debería cerrarse al ejecutarlo como administrador.**
