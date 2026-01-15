# 📜 Scripts de Windows - Referencia

**Copyright © 2026 Rafael Llibre. Todos los derechos reservados.**

Este documento explica los scripts BAT disponibles para Windows.

---

## 📦 Scripts Disponibles

### 1. `instalar_windows.bat` - Instalador Automático

**Propósito**: Automatiza completamente la instalación del sistema en Windows.

#### ¿Qué hace?

✅ **Verifica Python instalado (y lo instala si falta)**  
✅ **Verifica versión de Python (3.8+)**  
✅ **Descarga e instala Python 3.12 automáticamente si es necesario**  
✅ Verifica que pip funcione correctamente  
✅ Actualiza pip a la última versión  
✅ Instala todas las librerías necesarias automáticamente  
✅ Crea las carpetas `backups` y `documentos`  
✅ Crea el script `ejecutar.bat` para ejecutar fácilmente  
✅ Verifica que todas las librerías se instalaron correctamente  
✅ Ofrece ejecutar el programa inmediatamente  

#### Cómo usar:

1. **Haz doble clic** en `instalar_windows.bat`
2. Si Python no está instalado o la versión es antigua:
   - El script lo **descarga e instala automáticamente**
   - Espera 2-5 minutos para la instalación de Python
   - El script se reiniciará automáticamente
3. **Espera** a que complete la instalación de librerías (2-10 minutos)
4. **Sigue las instrucciones** en pantalla
5. Al finalizar, presiona **S** para ejecutar el programa

**Nota**: Si Python se instala automáticamente, el script pedirá que lo ejecutes una segunda vez para que Windows reconozca el PATH actualizado.

#### Salida del script:

```
╔═══════════════════════════════════════════════════════════════╗
║  INSTALADOR AUTOMÁTICO - SISTEMA DE GESTIÓN DE CASOS         ║
║  Versión 3.0 - Enero 2026                                     ║
╚═══════════════════════════════════════════════════════════════╝

[1/6] Verificando instalación de Python...
⚠ Python no está instalado

Descargando e instalando Python 3.12...
Descargando Python desde python.org...
✓ Python descargado correctamente

Instalando Python (esto puede tomar 2-5 minutos)...
✓ Python instalado correctamente

IMPORTANTE: Cerrando y reiniciando el script...
Por favor, ejecuta 'instalar_windows.bat' nuevamente.

--- (Segunda ejecución) ---

[1/6] Verificando instalación de Python...
✓ Python 3.12.1 detectado (versión correcta)

[2/6] Verificando pip (gestor de paquetes)...
✓ pip instalado correctamente

[3/6] Actualizando pip a la última versión...
✓ pip actualizado

[4/6] Instalando librerías necesarias...
Instalando desde requirements.txt...
✓ Todas las librerías instaladas desde requirements.txt

[5/6] Verificando instalación...
✓ PyQt6 verificado
✓ pandas verificado
✓ matplotlib verificado
✓ openpyxl verificado

✓ Carpeta 'backups' creada
✓ Carpeta 'documentos' creada
✓ Archivo 'ejecutar.bat' creado

╔═══════════════════════════════════════════════════════════════╗
║  ✓ INSTALACIÓN COMPLETADA EXITOSAMENTE                        ║
╚═══════════════════════════════════════════════════════════════╝
```

#### Ventajas:

- 🚀 **Instalación COMPLETAMENTE automática** (incluye Python)
- 🔍 **Detecta errores automáticamente**
- 📥 **Descarga Python si no está instalado**
- ✅ **Verifica versión de Python** (3.8+)
- 📦 **Instala todo lo necesario**
- ✅ **Verifica cada paso**
- 🎨 **Interfaz visual clara** con colores y símbolos
- ⚡ **Rápido** (2-15 minutos dependiendo de si instala Python)

---

### 2. `InstaladorUnico_SistemaGestionCasos.bat` - Instalador Autoextraíble ⭐

**Propósito**: Instalador de un solo archivo que contiene TODO el sistema embebido.

#### ¿Qué hace?

🎯 **Contiene todo el sistema embebido en Base64**  
🎯 **Extrae automáticamente 17 archivos Python**  
🎯 **Descarga e instala Python si falta**  
🎯 **Instala todas las dependencias**  
🎯 **Crea estructura completa de carpetas**  
🎯 **Genera ejecutar.bat**  
🎯 **Crea acceso directo en escritorio**  
🎯 **Todo en un solo archivo de 378 KB**  

#### Cómo usar:

1. **Descarga** `InstaladorUnico_SistemaGestionCasos.bat` (solo 378 KB)
2. **Doble clic** en el archivo
3. **Elige ubicación** de instalación (opción 1 recomendada)
4. **Espera** (automático - 5-15 minutos)
5. **¡Listo!** Sistema instalado completamente

**Nota**: Si Python no está instalado, lo descarga automáticamente (puede pedir ejecutar el instalador dos veces).

#### Salida del script:

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

Elige una opción (1-3): 1

Se instalará en: C:\Users\TuUsuario\Documents\SistemaGestionCasos

¿Continuar? (S/N): S

[1/7] Creando directorio de instalación...
✓ Directorio creado

[2/7] Extrayendo archivos del sistema...
  • main.py
  • requirements.txt
  • controllers/case_controller.py
  [... 14 archivos más ...]
✓ Todos los archivos extraídos correctamente

[3/7] Verificando Python...
✓ Python 3.12.1 detectado

[4/7] Instalando librerías necesarias...
✓ Librerías instaladas

[5/7] Verificando instalación...
✓ PyQt6
✓ pandas
✓ matplotlib
✓ openpyxl

[6/7] Creando acceso directo...
✓ Archivo ejecutar.bat creado

[7/7] ¿Crear acceso directo en el escritorio?
(S/N): S
✓ Acceso directo creado en el escritorio

╔═══════════════════════════════════════════════════════════════╗
║  ✓ INSTALACIÓN COMPLETADA EXITOSAMENTE                        ║
╚═══════════════════════════════════════════════════════════════╝

¿Ejecutar el programa ahora? (S/N): S
```

#### Ventajas:

- 🌟 **UN SOLO ARCHIVO** (378 KB)
- 📧 **Fácil de enviar** (email, WhatsApp, USB)
- 🚀 **Instalación 100% automática**
- 📦 **Todo embebido** (no necesita archivos adicionales)
- 🎯 **Instalación guiada** (paso a paso)
- ✅ **Instala Python automáticamente**
- 💾 **Portátil** (guarda en USB, manda por correo)
- 🔧 **No requiere conocimientos técnicos**

#### Desventajas:

- ⚠️ Antivirus puede dar falso positivo (es seguro)
- ⚠️ Si instala Python, requiere ejecutar 2 veces
- ⚠️ Necesita conexión a internet (para Python y librerías)

#### Contenido Embebido (17 archivos):

```
main.py
requirements.txt
controllers/
  ├── case_controller.py
  └── fiscal_history_controller.py
database/
  ├── db.py
  └── documents_db.py
models/
  ├── case.py
  └── fiscal_history.py
views/
  ├── main_window.py
  ├── fiscal_history_dialog.py
  └── fiscal_stats_dialog.py
services/
  └── document_service.py
utils/
  ├── backup_manager.py
  ├── export_service.py
  ├── graph_utils.py
  ├── import_service.py
  └── notification_manager.py
```

---

### 3. `build_windows.bat` - Constructor de Ejecutable

**Propósito**: Crea un ejecutable (.exe) independiente del sistema usando PyInstaller.

#### ¿Qué hace?

🔨 Crea un entorno virtual Python  
🔨 Instala todas las dependencias  
🔨 Instala PyInstaller  
🔨 Compila el programa en un ejecutable .exe  
🔨 Empaqueta todo en una carpeta `dist/`  
🔨 El ejecutable NO requiere Python instalado para funcionar  

#### Cómo usar:

1. **Ejecuta** `build_windows.bat` (desde cmd o doble clic)
2. **Espera** a que compile (puede tomar 5-15 minutos)
3. **Busca** el ejecutable en `dist\FiscaliaCases.exe`
4. **Distribuye** ese ejecutable a otras computadoras

#### Salida del script:

```
Build standalone Windows executable with PyInstaller.

Creando entorno virtual...
Instalando dependencias...
Instalando PyInstaller...
Limpiando compilaciones anteriores...
Compilando con PyInstaller...

Build finalizado. Encuentra el ejecutable en dist\FiscaliaCases.
```

#### Ventajas:

- ✅ **Ejecutable independiente** (.exe)
- ✅ **No requiere Python** en la máquina destino
- ✅ **Fácil de distribuir** a otros usuarios
- ✅ **Todo empaquetado** en un solo archivo/carpeta
- ✅ **Ideal para distribución masiva**

#### Desventajas:

- ⚠️ El archivo .exe es grande (100-200 MB)
- ⚠️ Puede ser detectado como falso positivo por antivirus
- ⚠️ Requiere más tiempo de compilación

---

## 🆚 Comparación

| Característica | `instalar_windows.bat` | `InstaladorUnico` ⭐ | `build_windows.bat` |
|---|---|---|---|
| **Propósito** | Instalar dependencias | Instalador completo | Crear ejecutable |
| **Archivos necesarios** | Carpeta completa | 1 solo archivo | Carpeta completa |
| **Tamaño distribución** | ~50 MB | **378 KB** | ~150 MB |
| **Instala Python** | ✅ Sí (automático) | ✅ Sí (automático) | ❌ No |
| **Requiere Python** | ❌ No (lo instala) | ❌ No (lo instala) | ✅ Sí |
| **Tiempo** | 2-15 minutos | 5-15 minutos | 5-15 minutos |
| **Para distribuir** | ❌ No | ✅✅ **Ideal** | ✅ Sí |
| **Fácil de enviar** | ❌ No | ✅✅ **Email/WhatsApp** | ⚠️ Grande |
| **Fácil actualización** | ✅ Sí | ✅ Sí | ❌ No |
| **Uso recomendado** | Desarrollo local | **Distribución fácil** | Distribución exe

## 📝 Cuándo usar cada uno

### Usa `InstaladorUnico_SistemaGestionCasos.bat` si: ⭐ RECOMENDADO

- ✅✅ Quieres **distribuir por email/WhatsApp** (solo 378 KB)
- ✅✅ Necesitas **un solo archivo** para compartir
- ✅✅ El usuario **no es técnico**
- ✅✅ Quieres **instalación super fácil** (doble clic)
- ✅✅ No quieres enviar carpetas completas
- ✅✅ Necesitas **portabilidad máxima** (USB, cloud)
- ✅✅ **Primera opción para distribución**

### Usa `instalar_windows.bat` si:

### Usa `instalar_windows.bat` si:

- ✅ Quieres **instalación completamente automática**
- ✅ **NO tienes Python** instalado (el script lo instala)
- ✅ Vas a instalar el sistema en **tu propia computadora**
- ✅ Quieres **actualizaciones fáciles** (solo copiar archivos)
- ✅ No tienes restricciones de tamaño
- ✅ Prefieres tener acceso al código fuente

### Usa `build_windows.bat` si:

- ✅ Necesitas **distribuir** el programa a muchos usuarios
- ✅ Los usuarios **NO tienen Python** instalado
- ✅ Quieres un **ejecutable profesional** (.exe)
- ✅ Los usuarios no son técnicos
- ✅ Prefieres **simplificar la instalación** para el usuario final

---

## 🚀 Flujo de Trabajo Recomendado

### Para Desarrollador/Administrador:
### Para Usuario Final (Opción 1 - Instalador Único) ⭐ RECOMENDADA:

```
1. Descarga InstaladorUnico_SistemaGestionCasos.bat (378 KB)
2. Doble clic
3. Elige ubicación
4. Espera (automático)
5. ¡Listo!
```

### Para Usuario Final (Opción 2 - Carpeta Completa):

```
1. Descarga el sistema (carpeta completa)
2. Ejecuta instalar_windows.bat
3. Espera (el script instala Python si es necesario)
4. Si Python se instaló, ejecuta instalar_windows.bat nuevamente
5. Usa ejecutar.bat para abrir el programa
```

## 🐛 Solución de Problemas

### `InstaladorUnico_SistemaGestionCasos.bat` no funciona

**Error: "No se pudo crear el directorio"**
- Ejecuta como Administrador (clic derecho → Ejecutar como administrador)
- O elige Opción 1 (Mis Documentos) que no requiere permisos

**Error: "No se pudo descargar Python"**
- Verifica conexión a internet
- Desactiva temporalmente firewall/antivirus
- O instala Python manualmente y ejecuta de nuevo

**Python se instaló pero no se reconoce**
- Esto es NORMAL
- Cierra la ventana
- Ejecuta el instalador de nuevo (ahora funcionará)

**Advertencia de seguridad de Windows**
- Es normal para archivos .bat
- Clic en "Más información"
- Clic en "Ejecutar de todas formas"
- El instalador es seguro (código verificable)

**Antivirus bloquea el archivo**
- Falso positivo común
- Agrega excepción en antivirus temporalmente
- O desactiva antivirus mientras instalas

### `instalar_windows.bat` no funciona
1. Recibe el archivo FiscaliaCases.exe
2. Haz doble clic
3. El programa abre directamente
```Si Python se instaló, ejecuta instalar_windows.bat nuevamente
5. Usa ejecutar.bat para abrir el programa
```

### Para Usuario Final (Opción 2 - Sin Python):

```
1. Recibe el archivo FiscaliaCases.exe
2. Haz doble clic
3. El programa abre directamente
```

---

## 🐛 Solución de Problemas

### `instalar_windows.bat` no funciona

**Error: "Python no está instalado"**
- El script debería instalar Python automáticamente
- Si falla la descarga automática:
  * Verifica conexión a internet
  * Descarga manualmente desde python.org
  * Durante instalación, marca "Add Python to PATH"
  * Ejecuta el script de nuevo

**Error: "Python X.X es demasiado antiguo"**
- El script detecta versiones antiguas (<3.8)
- Intentará descargar Python 3.12 automáticamente
- Si falla, desinstala Python viejo y ejecuta el script nuevamente

**Python se instaló pero el script sigue sin encontrarlo**
## 📁 Estructura de Archivos Generados

### Después de `InstaladorUnico_SistemaGestionCasos.bat`:

```
C:\Users\TuUsuario\Documents\SistemaGestionCasos\
├── ejecutar.bat            ← Creado automáticamente
├── main.py
├── requirements.txt
├── cases.db                ← Creado en primera ejecución
├── backups/                ← Creado automáticamente
├── documentos/             ← Creado automáticamente
├── documents/              ← Creado automáticamente
├── exports/                ← Creado automáticamente
├── controllers/
│   ├── case_controller.py
│   └── fiscal_history_controller.py
├── database/
│   ├── db.py
│   └── documents_db.py
├── models/
│   ├── case.py
│   └── fiscal_history.py
├── views/
│   ├── main_window.py
│   ├── fiscal_history_dialog.py
│   └── fiscal_stats_dialog.py
├── services/
│   └── document_service.py
└── utils/
    ├── backup_manager.py
    ├── export_service.py
    ├── graph_utils.py
    ├── import_service.py
    └── notification_manager.py
```

### Después de `instalar_windows.bat`:s.bat` de nuevo

**Error: "No se pudo descargar Python"**
- Verifica conexión a internet
- Desactiva temporalmente firewall/antivirus
- O descarga manualmente desde: https://www.python.org/downloads/
- Instala con "Add Python to PATH" marcado

**Error: "pip no se reconoce"**
- Ejecuta: `python -m pip install --upgrade pip`
## 🔄 Actualización del Sistema

### Si instalaste con `InstaladorUnico_SistemaGestionCasos.bat`:

1. **Respalda** `cases.db` y carpeta `documentos`
2. Descarga el **nuevo** `InstaladorUnico_SistemaGestionCasos.bat`
3. Ejecútalo en la **misma ubicación**
4. Confirma sobrescribir archivos existentes
5. Restaura `cases.db` y `documentos` si es necesario

### Si instalaste con `instalar_windows.bat`:ias"**
- Verifica conexión a internet
- Ejecuta el script como Administrador
- Desactiva temporalmente el antivirus/firewall

### `build_windows.bat` no funciona

**Error: "PyInstaller no se instaló"**
- Ejecuta manualmente: `pip install pyinstaller`
## 💡 Consejos

### Para `InstaladorUnico_SistemaGestionCasos.bat`:

- ✅ **Ideal para distribución por email** (solo 378 KB)
- ✅ Perfecto para **usuarios no técnicos**
- ✅ Guárdalo en **USB** para instalaciones offline (después de primera vez)
- ✅ Si instala Python, **ejecuta 2 veces** (normal)
- ✅ Usa **Opción 1** (Mis Documentos) - más seguro
- ✅ **Crea acceso directo** en escritorio (opción recomendada)
- ✅ El archivo es **reutilizable** en múltiples PCs

### Para `instalar_windows.bat`:no"**
- El script busca `assets\icon.ico`
- Si no existe, continúa sin icono
- Puedes crear la carpeta `assets` y agregar un icono

**El ejecutable es detectado como virus**
- Es un falso positivo común con PyInstaller
- Agrega excepción en el antivirus
- O distribuye el código fuente con `instalar_windows.bat`

---

## 📁 Estructura de Archivos Generados

### Después de `instalar_windows.bat`:

```
jusgadodepaz/
├── instalar_windows.bat    ← Script de instalación
├── ejecutar.bat            ← Creado automáticamente
├── main.py
├── requirements.txt
├── cases.db                ← Creado en primera ejecución
├── backups/                ← Creado automáticamente
├── documentos/             ← Creado automáticamente
├── controllers/
├── database/
├── models/
└── views/
```

### Después de `build_windows.bat`:

```
## 📞 Necesitas Más Ayuda

- **Manual del Instalador Único**: Ver [MANUAL_INSTALADOR_UNICO.md](MANUAL_INSTALADOR_UNICO.md) ⭐
- **Instalación detallada**: Ver [INSTALACION_WINDOWS.md](INSTALACION_WINDOWS.md)
- **Manual completo**: Ver [MANUAL_COMPLETO.md](MANUAL_COMPLETO.md)
- **Guía de usuario**: Ver [GUIA_USUARIO.md](GUIA_USUARIO.md)
├── build/                  ← Archivos temporales
└── dist/
    └── FiscaliaCases/      ← Carpeta con el ejecutable
        ├── FiscaliaCases.exe  ← Ejecutable principal
        ├── cases.db
        └── [librerías empaquetadas]
```

---

## 🔄 Actualización del Sistema

### Si instalaste con `instalar_windows.bat`:

1. Descarga la nueva versión
2. **Respalda** `cases.db` y carpeta `documentos`
3. Copia los nuevos archivos (excepto cases.db)
4. Ejecuta `instalar_windows.bat` de nuevo
5. Restaura `cases.db` y `documentos`

### Si distribuiste con `build_windows.bat`:

1. Realiza cambios en el código
2. Ejecuta `build_windows.bat` de nuevo
3. Distribuye el nuevo `FiscaliaCases.exe`
4. Los usuarios reemplazan el .exe viejo por el nuevo

---

## 💡 Consejos

### Para `instalar_windows.bat`:

- ✅ Ejecuta como **Administrador** si hay problemas de permisos
- ✅ Ten **conexión a internet** estable
- ✅ Cierra antivirus temporalmente si bloquea pip
- ✅ Usa el `ejecutar.bat` generado para abrir el programa fácilmente

### Para `build_windows.bat`:

- ✅ Ejecuta en una máquina con **buena RAM** (4GB+ recomendado)
- ✅ Ten **espacio en disco** (al menos 1GB libre)
- ✅ La primera compilación tarda más
- ✅ Compila en **Windows 10/11** para mejor compatibilidad
- ✅ Si tienes icono, ponlo en `assets/icon.ico`

---

## 📞 Necesitas Más Ayuda

- **Instalación detallada**: Ver [INSTALACION_WINDOWS.md](INSTALACION_WINDOWS.md)
- **Manual completo**: Ver [MANUAL_COMPLETO.md](MANUAL_COMPLETO.md)
- **Guía de usuario**: Ver [GUIA_USUARIO.md](GUIA_USUARIO.md)

---

**Versión**: 3.0  
**Última actualización**: Enero 2026  
**Plataforma**: Windows 10/11
