# 📦 Manual del Instalador Único

## Sistema de Gestión de Casos - Versión 3.0

**Copyright © 2026 Rafael Llibre. Todos los derechos reservados.**

---

## 📋 Índice

1. [¿Qué es el Instalador Único?](#qué-es-el-instalador-único)
2. [Ventajas](#ventajas)
3. [Requisitos](#requisitos)
4. [Cómo Obtener el Instalador](#cómo-obtener-el-instalador)
5. [Guía de Instalación Paso a Paso](#guía-de-instalación-paso-a-paso)
6. [Opciones de Instalación](#opciones-de-instalación)
7. [Proceso Completo Explicado](#proceso-completo-explicado)
8. [Solución de Problemas](#solución-de-problemas)
9. [Preguntas Frecuentes](#preguntas-frecuentes)
10. [Desinstalación](#desinstalación)

---

## ¿Qué es el Instalador Único?

`InstaladorUnico_SistemaGestionCasos.bat` es un **instalador autoextraíble** que contiene **TODO** el sistema completo en un solo archivo.

### 📦 Contenido Embebido:

- **17 archivos Python** del sistema completo
- Script de instalación de Python 3.12
- Configuración de dependencias
- Creación automática de estructura
- Todo codificado en Base64

### 🎯 Filosofía:

**"Un solo archivo, una sola ejecución, instalación completa"**

---

## Ventajas

### ✅ Para el Usuario:

| Ventaja | Descripción |
|---------|-------------|
| 🚀 **Un solo archivo** | No necesitas descargar carpetas completas |
| 📧 **Fácil de enviar** | Solo 378 KB - cabe en email, WhatsApp, etc. |
| 🎯 **Instalación guiada** | Interfaz paso a paso muy clara |
| 🔧 **Todo automático** | Instala Python, librerías y configura todo |
| 💾 **Portátil** | Llévalo en USB, guárdalo donde quieras |
| 🔄 **Sin dependencias** | No necesitas nada más |

### ✅ Para el Distribuidor:

| Ventaja | Descripción |
|---------|-------------|
| 📤 **Distribución simple** | Un solo archivo para compartir |
| 🎓 **Usuarios no técnicos** | Cualquiera puede instalarlo |
| 📱 **Múltiples canales** | Email, chat, cloud, USB |
| ✔️ **Verificado** | Todo el código incluido y probado |

---

## Requisitos

### 🖥️ Sistema Operativo:

- **Windows 10** o superior (recomendado)
- **Windows 8.1** (compatible)
- **Windows 7** (puede funcionar, no recomendado)

### 💿 Hardware Mínimo:

- **Procesador**: Dual Core 2.0 GHz o superior
- **RAM**: 4 GB (8 GB recomendado)
- **Disco**: 500 MB libres (para instalación completa)
- **Conexión a Internet**: Necesaria solo si no tienes Python instalado

### ⚠️ Permisos:

- **Permisos de escritura** en la ubicación de instalación
- **Opcional**: Permisos de Administrador (si instala Python)

---

## Cómo Obtener el Instalador

### Opción 1: Descarga Directa

1. Descarga `InstaladorUnico_SistemaGestionCasos.bat`
2. Guárdalo en tu computadora (Descargas, Escritorio, etc.)

### Opción 2: Por Correo Electrónico

1. Recibes el archivo como adjunto
2. Descarga el archivo adjunto

### Opción 3: Desde USB

1. Copia el archivo desde la USB
2. Pégalo en tu computadora

### Opción 4: Cloud (Drive, Dropbox, etc.)

1. Descarga desde el enlace compartido
2. Guarda en tu computadora

---

## Guía de Instalación Paso a Paso

### 📍 Paso 0: Preparación

```
1. Descarga el archivo InstaladorUnico_SistemaGestionCasos.bat
2. Guárdalo en una ubicación que recuerdes
3. Cierra otros programas (opcional pero recomendado)
4. Ten conexión a internet disponible
```

### 🚀 Paso 1: Ejecutar el Instalador

**Método 1 - Doble Clic (Recomendado):**

1. Busca el archivo `InstaladorUnico_SistemaGestionCasos.bat`
2. **Doble clic** sobre él
3. Si aparece advertencia de seguridad:
   - Clic en **"Más información"**
   - Clic en **"Ejecutar de todas formas"**

**Método 2 - Clic Derecho:**

1. Clic derecho sobre el archivo
2. Selecciona **"Abrir"** o **"Ejecutar"**

**Método 3 - Como Administrador (si hay problemas):**

1. Clic derecho sobre el archivo
2. Selecciona **"Ejecutar como administrador"**
3. Clic en **"Sí"** en el UAC (Control de Cuentas de Usuario)

---

### 📂 Paso 2: Elegir Ubicación de Instalación

Verás esta pantalla:

```
╔═══════════════════════════════════════════════════════════════╗
║  INSTALADOR ÚNICO - SISTEMA DE GESTIÓN DE CASOS              ║
║  Versión 3.0 - Enero 2026                                     ║
║  Instalador autoextraíble - Todo incluido                     ║
╚═══════════════════════════════════════════════════════════════╝

¿Dónde deseas instalar el sistema?

Opciones:
  1. Mis Documentos (Recomendado)
  2. C:\SistemaGestionCasos
  3. Ubicación personalizada

Elige una opción (1-3):
```

**Recomendaciones:**

| Opción | Ubicación | Cuándo Usar |
|--------|-----------|-------------|
| **1** | `C:\Users\TuUsuario\Documents\SistemaGestionCasos` | ✅ **Recomendado** para la mayoría |
| **2** | `C:\SistemaGestionCasos` | Si quieres fácil acceso desde la raíz |
| **3** | Tú decides | Si tienes una ubicación específica en mente |

**Ejemplo - Opción 1 (Recomendada):**

```
Elige una opción (1-3): 1
```

Presiona **Enter**

---

### ✅ Paso 3: Confirmar Instalación

```
Se instalará en: C:\Users\TuUsuario\Documents\SistemaGestionCasos

¿Continuar? (S/N):
```

- Escribe **S** (Sí) y presiona **Enter**
- O escribe **N** (No) para cancelar

---

### ⏳ Paso 4: Proceso Automático

A partir de aquí, **TODO es automático**. Solo espera.

#### [1/7] Crear Directorio

```
[1/7] Creando directorio de instalación...

✓ Directorio creado: C:\Users\...\SistemaGestionCasos
```

#### [2/7] Extraer Archivos

```
[2/7] Extrayendo archivos del sistema...

Extrayendo archivos Python...
  • main.py
  • requirements.txt
  • controllers/case_controller.py
  • controllers/fiscal_history_controller.py
  • database/db.py
  • database/documents_db.py
  • models/case.py
  • models/fiscal_history.py
  • views/main_window.py
  • views/fiscal_history_dialog.py
  • views/fiscal_stats_dialog.py
  • services/document_service.py
  • utils/backup_manager.py
  • utils/export_service.py
  • utils/graph_utils.py
  • utils/import_service.py
  • utils/notification_manager.py

✓ Todos los archivos extraídos correctamente
```

⏱️ **Tiempo estimado**: 10-30 segundos

#### [3/7] Verificar/Instalar Python

**Caso A - Python ya instalado:**

```
[3/7] Verificando Python...

✓ Python 3.12.1 detectado
```

⏱️ **Tiempo**: 2 segundos

**Caso B - Python NO instalado:**

```
[3/7] Verificando Python...

⚠ Python no está instalado
Descargando Python 3.12...

Descargando Python desde python.org...
[Barra de progreso]

✓ Python descargado

Instalando Python (esto puede tomar 2-5 minutos)...
[Instalación en progreso]

✓ Python instalado correctamente

IMPORTANTE: Cierra esta ventana y ejecuta el archivo nuevamente
para que Windows reconozca Python.

Busca el archivo: C:\Users\...\SistemaGestionCasos\ejecutar.bat

Presiona cualquier tecla para continuar...
```

⏱️ **Tiempo**: 3-7 minutos

**⚠️ IMPORTANTE**: Si Python se instaló, debes:

1. Cerrar la ventana actual
2. Buscar el instalador de nuevo
3. Ejecutarlo otra vez (ahora reconocerá Python)

#### [4/7] Instalar Dependencias

```
[4/7] Instalando librerías necesarias...

Esto puede tomar 5-10 minutos...

[Instalando PyQt6, pandas, matplotlib, openpyxl...]

✓ Librerías instaladas
```

⏱️ **Tiempo**: 5-10 minutos (varía según conexión)

#### [5/7] Verificar Instalación

```
[5/7] Verificando instalación...

✓ PyQt6
✓ pandas
✓ matplotlib
✓ openpyxl
```

⏱️ **Tiempo**: 5-10 segundos

#### [6/7] Crear Acceso Directo Local

```
[6/7] Creando acceso directo...

✓ Archivo ejecutar.bat creado
```

#### [7/7] Crear Acceso Directo en Escritorio

```
[7/7] ¿Crear acceso directo en el escritorio?
(S/N):
```

- **S** = Sí, crear acceso directo en escritorio (recomendado)
- **N** = No, solo usar el archivo ejecutar.bat

---

### 🎉 Paso 5: Instalación Completada

```
╔═══════════════════════════════════════════════════════════════╗
║  ✓ INSTALACIÓN COMPLETADA EXITOSAMENTE                        ║
╚═══════════════════════════════════════════════════════════════╝

Ubicación: C:\Users\TuUsuario\Documents\SistemaGestionCasos

═══════════════════════════════════════════════════════════════
 CÓMO EJECUTAR:
═══════════════════════════════════════════════════════════════

 • Doble clic en: ejecutar.bat
 • O acceso directo en el escritorio

═══════════════════════════════════════════════════════════════

¿Ejecutar el programa ahora? (S/N):
```

- **S** = Ejecuta el programa inmediatamente
- **N** = Cierra el instalador (puedes ejecutar después)

---

## Opciones de Instalación

### 📍 Ubicaciones Recomendadas

#### Opción 1: Mis Documentos (Recomendada)

**Ruta**: `C:\Users\TuUsuario\Documents\SistemaGestionCasos`

**Ventajas:**
- ✅ Respaldo automático con OneDrive/Google Drive
- ✅ Fácil acceso
- ✅ No requiere permisos de administrador
- ✅ Se incluye en backups de usuario

**Desventajas:**
- ⚠️ Ruta más larga

#### Opción 2: Raíz de C:

**Ruta**: `C:\SistemaGestionCasos`

**Ventajas:**
- ✅ Ruta corta y fácil de recordar
- ✅ Acceso rápido
- ✅ Ideal para servidores

**Desventajas:**
- ⚠️ Puede requerir permisos de administrador
- ⚠️ No se incluye en backup de usuario

#### Opción 3: Personalizada

**Ejemplos:**
- `D:\Trabajo\SistemaGestionCasos`
- `E:\Aplicaciones\Casos`
- `C:\Oficina\Sistema`

**Ventajas:**
- ✅ Ubicación específica para tu flujo de trabajo
- ✅ Puede estar en otro disco

**Desventajas:**
- ⚠️ Debes recordar la ubicación

---

## Proceso Completo Explicado

### 🔍 ¿Qué Hace el Instalador Internamente?

#### Fase 1: Inicialización (0-5 segundos)

```
1. Muestra interfaz de bienvenida
2. Solicita ubicación de instalación
3. Verifica permisos de escritura
4. Confirma con el usuario
```

#### Fase 2: Extracción (10-30 segundos)

```
1. Crea estructura de directorios:
   - controllers/
   - database/
   - models/
   - views/
   - services/
   - utils/
   - backups/
   - documentos/
   - documents/
   - exports/

2. Decodifica archivos Base64:
   - Crea archivos temporales .b64
   - Usa PowerShell para decodificar
   - Escribe archivos Python
   - Elimina archivos temporales

3. Total: 17 archivos Python extraídos
```

#### Fase 3: Python (2 segundos - 7 minutos)

**Si Python está instalado:**
```
1. Ejecuta: python --version
2. Verifica versión >= 3.8
3. Continúa al siguiente paso
```

**Si Python NO está instalado:**
```
1. Detecta ausencia de Python
2. Configura PowerShell con TLS 1.2
3. Descarga Python 3.12.1 (25 MB)
4. Instala silenciosamente con:
   - /quiet (sin interfaz)
   - InstallAllUsers=1 (todos los usuarios)
   - PrependPath=1 (agrega al PATH)
   - Include_test=0 (sin tests)
5. Solicita re-ejecución del instalador
6. Sale del script
```

#### Fase 4: Dependencias (5-10 minutos)

```
1. Verifica que pip funciona: pip --version
2. Instala desde requirements.txt:
   - PyQt6 (interfaz gráfica)
   - pandas (manejo de datos)
   - matplotlib (gráficos)
   - openpyxl (Excel)
3. Modo: --quiet (sin mucha salida)
```

#### Fase 5: Verificación (5-10 segundos)

```
1. Intenta importar cada librería:
   python -c "import PyQt6"
   python -c "import pandas"
   python -c "import matplotlib"
   python -c "import openpyxl"

2. Si falla alguna, muestra error y detiene
```

#### Fase 6: Configuración Final (2-5 segundos)

```
1. Crea ejecutar.bat:
   @echo off
   cd /d "%~dp0"
   python main.py
   if %errorlevel% neq 0 pause

2. (Opcional) Crea acceso directo en escritorio:
   - Usa VBScript para crear .lnk
   - Apunta a ejecutar.bat
   - Nombre: "Sistema Gestion Casos.lnk"
```

#### Fase 7: Finalización (1 segundo)

```
1. Muestra resumen de instalación
2. Ofrece ejecutar el programa
3. Si acepta: ejecuta python main.py
4. Si no: cierra instalador
```

---

## Solución de Problemas

### 🚫 Error: "No se pudo crear el directorio"

**Causa**: Sin permisos de escritura

**Solución**:
```
1. Clic derecho en InstaladorUnico_SistemaGestionCasos.bat
2. Selecciona "Ejecutar como administrador"
3. Clic en "Sí" en el UAC
```

O elige una ubicación diferente (Opción 1: Mis Documentos)

---

### 🚫 Error: "No se pudo descargar Python"

**Causa**: Problemas de conexión o firewall

**Solución 1 - Verificar Conexión**:
```
1. Verifica que tienes internet funcionando
2. Intenta abrir python.org en tu navegador
3. Si funciona, ejecuta el instalador de nuevo
```

**Solución 2 - Firewall/Antivirus**:
```
1. Desactiva temporalmente el antivirus
2. Ejecuta el instalador de nuevo
3. Reactiva el antivirus después
```

**Solución 3 - Instalación Manual de Python**:
```
1. Ve a https://www.python.org/downloads/
2. Descarga Python 3.12 (64-bit)
3. Instala marcando "Add Python to PATH"
4. Ejecuta el instalador de nuevo
```

---

### 🚫 Error: "Python se instaló pero no se reconoce"

**Causa**: Windows no actualizó el PATH

**Solución**:
```
✅ Esto es NORMAL
1. Cierra la ventana del instalador
2. Busca el archivo instalador de nuevo
3. Ejecútalo otra vez
4. Ahora funcionará correctamente
```

---

### 🚫 Error: "No se pueden instalar las dependencias"

**Causa**: Problemas con pip o conexión

**Solución 1 - Verificar pip**:
```
1. Abre CMD (Win + R, escribe "cmd")
2. Ejecuta: python -m pip --version
3. Si falla: python -m ensurepip --upgrade
4. Ejecuta el instalador de nuevo
```

**Solución 2 - Actualizar pip**:
```
1. Abre CMD como Administrador
2. Ejecuta: python -m pip install --upgrade pip
3. Ejecuta el instalador de nuevo
```

**Solución 3 - Proxy/Firewall**:
```
1. Verifica configuración de proxy
2. Desactiva temporalmente firewall
3. Ejecuta el instalador de nuevo
```

---

### 🚫 Error: "Falta alguna librería en la verificación"

**Causa**: Instalación incompleta de dependencias

**Solución**:
```
1. Abre CMD en la carpeta de instalación
2. Ejecuta: pip install PyQt6 pandas matplotlib openpyxl
3. Espera a que termine
4. Ejecuta: python main.py
```

---

### ⚠️ Advertencia de Seguridad de Windows

**Mensaje**: "Windows protegió tu PC"

**Solución**:
```
✅ Esto es normal para archivos .bat
1. Clic en "Más información"
2. Clic en "Ejecutar de todas formas"
3. El instalador es seguro (puedes verificar el código)
```

---

### ⚠️ Antivirus Bloquea el Archivo

**Causa**: Falso positivo común con scripts BAT

**Solución 1 - Excepción Temporal**:
```
1. Abre tu antivirus
2. Agrega excepción para InstaladorUnico_SistemaGestionCasos.bat
3. Ejecuta el instalador
4. Remueve la excepción si deseas
```

**Solución 2 - Desactivar Temporalmente**:
```
1. Desactiva el antivirus por 5 minutos
2. Ejecuta el instalador
3. Reactiva el antivirus
```

---

## Preguntas Frecuentes

### ❓ ¿Necesito Python instalado previamente?

**No**. El instalador lo descarga e instala automáticamente si no lo tienes.

---

### ❓ ¿Necesito conexión a internet?

**Depende**:
- **Sí** si no tienes Python instalado (para descargarlo)
- **Sí** para instalar las librerías (PyQt6, pandas, etc.)
- **No** una vez instalado todo

---

### ❓ ¿Cuánto espacio necesito en disco?

**Mínimo**: 500 MB
- Instalador: 378 KB
- Python 3.12: ~100 MB
- Librerías: ~200 MB
- Sistema: ~5 MB
- Base de datos: ~50 MB (crece con el uso)
- Espacio para documentos y backups: ~100 MB

**Recomendado**: 1 GB libre

---

### ❓ ¿Cuánto tarda la instalación?

**Depende**:

| Escenario | Tiempo |
|-----------|--------|
| Python ya instalado + buena conexión | 5-8 minutos |
| Sin Python + buena conexión | 10-15 minutos |
| Sin Python + conexión lenta | 15-20 minutos |

---

### ❓ ¿Puedo instalar en múltiples computadoras?

**Sí**. El instalador se puede usar en todas las computadoras que quieras.

---

### ❓ ¿Se actualiza automáticamente?

**No**. Para actualizar:
1. Descarga el nuevo instalador
2. Respalda tu base de datos `cases.db`
3. Ejecuta el nuevo instalador en la misma ubicación
4. Restaura `cases.db`

---

### ❓ ¿Qué pasa si cancelo durante la instalación?

**No hay problema**:
- Archivos parcialmente extraídos se pueden eliminar
- Ejecuta el instalador de nuevo cuando quieras
- Python instalado (si se instaló) permanece

---

### ❓ ¿Puedo mover el sistema después de instalado?

**Sí**, pero:
1. Copia toda la carpeta a la nueva ubicación
2. Ejecuta `ejecutar.bat` desde allí
3. Si creaste acceso directo en escritorio, actualízalo

---

### ❓ ¿Cómo ejecuto el programa después?

**Método 1 - Acceso Directo** (si lo creaste):
```
Doble clic en "Sistema Gestion Casos" en el escritorio
```

**Método 2 - ejecutar.bat**:
```
1. Ve a la carpeta de instalación
2. Doble clic en ejecutar.bat
```

**Método 3 - Manual**:
```
1. Abre CMD en la carpeta de instalación
2. Ejecuta: python main.py
```

---

### ❓ ¿El instalador modifica mi sistema?

**Cambios mínimos**:
- ✅ Instala Python (si no existe)
- ✅ Agrega Python al PATH
- ✅ Instala 4 librerías Python
- ✅ Crea carpeta de instalación
- ✅ (Opcional) Acceso directo en escritorio

**NO modifica**:
- ❌ Registro de Windows (excepto Python)
- ❌ Archivos del sistema
- ❌ Configuración de red
- ❌ Otros programas

---

### ❓ ¿Puedo ver el código antes de ejecutar?

**Sí**:
1. Clic derecho en `InstaladorUnico_SistemaGestionCasos.bat`
2. Selecciona "Editar" o "Abrir con Bloc de notas"
3. Verás el código del instalador y archivos embebidos en Base64

---

### ❓ ¿Es seguro?

**Sí**:
- ✅ Código abierto (puedes revisarlo)
- ✅ No conexiones sospechosas
- ✅ Solo descarga Python desde python.org
- ✅ Instala librerías desde PyPI oficial
- ✅ No modifica archivos del sistema
- ✅ No requiere permisos excesivos

---

## Desinstalación

### 🗑️ Desinstalar el Sistema

#### Paso 1: Eliminar Carpeta de Instalación

```
1. Ve a la ubicación donde instalaste
   Ejemplo: C:\Users\TuUsuario\Documents\SistemaGestionCasos
2. Clic derecho en la carpeta
3. Selecciona "Eliminar"
4. Confirma en la papelera de reciclaje
```

#### Paso 2: Eliminar Acceso Directo (si lo creaste)

```
1. Ve al escritorio
2. Busca "Sistema Gestion Casos"
3. Clic derecho → Eliminar
```

#### Paso 3: (Opcional) Desinstalar Python

**Solo si NO lo usas para nada más**:

```
1. Win + R
2. Escribe: appwiz.cpl
3. Presiona Enter
4. Busca "Python 3.12"
5. Clic derecho → Desinstalar
6. Sigue el asistente
```

---

## 📊 Resumen Rápido

### ✅ Proceso Completo en 3 Pasos:

```
1. Doble clic en InstaladorUnico_SistemaGestionCasos.bat
2. Elige ubicación (opción 1 recomendada)
3. Espera (automático)
```

### ⏱️ Tiempo Total:

- Con Python instalado: **5-8 minutos**
- Sin Python instalado: **10-15 minutos**

### 📦 Resultado:

- ✅ Sistema completo instalado
- ✅ Python configurado
- ✅ Todas las librerías instaladas
- ✅ Acceso directo creado
- ✅ Listo para usar

---

## 📞 Soporte

### 📖 Documentación Adicional:

- **Manual Completo**: Ver `MANUAL_COMPLETO.md`
- **Guía de Usuario**: Ver `GUIA_USUARIO.md`
- **Scripts Windows**: Ver `SCRIPTS_WINDOWS.md`
- **Instalación Windows**: Ver `INSTALACION_WINDOWS.md`

### 🆘 Si Necesitas Ayuda:

1. Lee la sección "Solución de Problemas"
2. Verifica las "Preguntas Frecuentes"
3. Revisa los logs de instalación
4. Contacta al soporte técnico

---

**Versión del Manual**: 1.0  
**Fecha**: Enero 2026  
**Sistema**: Gestión de Casos v3.0  
**Plataforma**: Windows 10/11

---

## 🎉 ¡Listo para Empezar!

Una vez instalado, el sistema está listo para:

- 📝 Registrar casos judiciales
- 📊 Generar estadísticas
- 📈 Visualizar gráficos
- 📄 Exportar reportes
- 💾 Gestionar documentos
- 🔍 Buscar y filtrar casos
- 📦 Crear respaldos automáticos

**¡Disfruta del Sistema de Gestión de Casos!**
