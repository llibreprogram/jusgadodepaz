# 💻 Guía de Instalación para Windows

**Copyright © 2026 Rafael Llibre. Todos los derechos reservados.**

## 📖 Instalación Paso a Paso en Windows

Esta guía está diseñada para usuarios que **nunca han instalado Python** y necesitan el sistema funcionando en Windows.

---

## ⚡ Instalación Rápida (Recomendada)

### Opción Totalmente Automática (MÁS FÁCIL):

**No necesitas tener Python instalado. El script lo hace todo.**

1. **Descarga** la carpeta completa del sistema
2. **Haz doble clic** en `instalar_windows.bat`
3. **Espera** mientras:
   - Verifica si Python está instalado
   - Si no lo está, lo **descarga e instala automáticamente** (Python 3.12)
   - Instala todas las librerías necesarias
   - Crea las carpetas y archivos necesarios
4. **Si Python se instaló**: El script te pedirá que lo ejecutes nuevamente
5. **Ejecuta** `instalar_windows.bat` una segunda vez (solo si instaló Python)
6. **Presiona S** cuando pregunte si quieres ejecutar el programa
7. ✅ **¡Listo!** El sistema está instalado y funcionando

⏱️ **Tiempo total**: 2-15 minutos (dependiendo de si necesita instalar Python)

📝 **Ver detalles**: [SCRIPTS_WINDOWS.md](SCRIPTS_WINDOWS.md) explica qué hace el instalador automático.

---

## 📖 Instalación Manual (Solo si la Automática Falla)

Si el instalador automático no funciona o prefieres instalación manual paso a paso:

---

## 📋 Requisitos Previos

- **Sistema Operativo**: Windows 10 o Windows 11
- **Espacio en Disco**: Al menos 500 MB libres
- **Conexión a Internet**: Necesaria para descargar Python y librerías
- **Permisos**: Debes poder instalar programas (usuario administrador)

---

## 🔧 Parte 1: Instalar Python

### Paso 1: Descargar Python

1. **Abre tu navegador** (Chrome, Edge, Firefox)
2. **Ve a**: [https://www.python.org/downloads/](https://www.python.org/downloads/)
3. Verás un botón grande que dice **"Download Python 3.12.x"** (o la versión más reciente)
4. **Haz clic** en ese botón
5. El archivo se descargará (se llama algo como `python-3.12.x.exe`)

### Paso 2: Instalar Python

1. **Busca el archivo descargado** (probablemente en tu carpeta "Descargas")
2. **Haz doble clic** en `python-3.12.x.exe`
3. **⚠️ MUY IMPORTANTE**: En la primera pantalla:
   - ✅ **MARCA** la casilla que dice **"Add Python to PATH"** (abajo)
   - ✅ **MARCA** la casilla **"Add Python to environment variables"**
   - Haz clic en **"Install Now"**
4. Espera a que termine (puede tomar 2-5 minutos)
5. Cuando veas **"Setup was successful"**, haz clic en **"Close"**

### Paso 3: Verificar que Python se instaló correctamente

1. **Abre el Símbolo del sistema** (Command Prompt):
   - Presiona la tecla **Windows** ⊞
   - Escribe: `cmd`
   - Presiona **Enter**
2. En la ventana negra que se abre, escribe:
   ```cmd
   python --version
   ```
3. Presiona **Enter**
4. Deberías ver algo como: `Python 3.12.1`

✅ **Si ves la versión de Python, todo está bien. Continúa al siguiente paso.**

❌ **Si dice "python no se reconoce..."**:
   - Python no se agregó al PATH correctamente
   - Desinstala Python y repite el Paso 2, asegurándote de marcar "Add Python to PATH"

---

## 📦 Parte 2: Descargar el Sistema

### Opción A: Si tienes el archivo ZIP

1. **Busca el archivo** `jusgadodepaz.zip` (o como se llame el archivo que te dieron)
2. **Haz clic derecho** sobre el archivo
3. Selecciona **"Extraer todo..."** o **"Extract here"**
4. Elige una ubicación fácil de encontrar, por ejemplo:
   - `C:\jusgadodepaz`
   - O tu carpeta de Documentos
5. Haz clic en **"Extraer"**

### Opción B: Si tienes Git instalado

1. Abre el **Símbolo del sistema** (cmd)
2. Navega a donde quieres guardar el programa:
   ```cmd
   cd C:\
   ```
3. Clona el repositorio:
   ```cmd
   git clone [URL_DEL_REPOSITORIO] jusgadodepaz
   ```

### Opción C: Si recibes los archivos por correo/USB

1. Copia toda la carpeta a una ubicación permanente
2. Por ejemplo: `C:\jusgadodepaz`
3. ⚠️ **No ejecutes el programa desde el USB o carpeta temporal**

---

## 📚 Parte 3: Instalar las Librerías Necesarias

### Paso 1: Abrir el Símbolo del sistema en la carpeta del programa

**Método Fácil:**
1. Abre el **Explorador de archivos** (Windows Explorer)
2. Navega a la carpeta donde está el sistema (ej: `C:\jusgadodepaz`)
3. Haz clic en la **barra de dirección** (donde dice la ruta)
4. Escribe: `cmd`
5. Presiona **Enter**
6. Se abrirá el símbolo del sistema ya en esa carpeta

**Método Alternativo:**
1. Abre el **Símbolo del sistema**
2. Escribe:
   ```cmd
   cd C:\jusgadodepaz
   ```
   (ajusta la ruta según donde guardaste el programa)
3. Presiona **Enter**

### Paso 2: Instalar las librerías

En el símbolo del sistema (que debe estar en la carpeta del programa), escribe:

```cmd
pip install -r requirements.txt
```

Presiona **Enter** y espera. Verás algo como:

```
Collecting PyQt6
  Downloading PyQt6-6.x.x...
Installing collected packages: PyQt6, matplotlib, pandas, openpyxl
Successfully installed...
```

⏱️ **Esto puede tomar 2-10 minutos** dependiendo de tu conexión a internet.

✅ **Si termina sin errores, todo está listo.**

❌ **Si hay errores**:
- Verifica que tienes conexión a internet
- Verifica que Python está en el PATH (Parte 1, Paso 3)
- Intenta cerrar y abrir de nuevo el símbolo del sistema

---

## 🚀 Parte 4: Ejecutar el Programa por Primera Vez

### Paso 1: Ejecutar

En el símbolo del sistema (en la carpeta del programa), escribe:

```cmd
python main.py
```

Presiona **Enter**.

### Paso 2: Primera Ejecución

La primera vez que ejecutas el programa:

1. Se creará automáticamente la **base de datos** (`cases.db`)
2. Se creará la carpeta **backups** para respaldos
3. Se creará la carpeta **documentos** para archivos adjuntos
4. Verás un mensaje: `✓ Respaldo automático creado`
5. La ventana del programa se abrirá

⏱️ **Puede tomar 5-10 segundos en abrir la primera vez.**

✅ **Si ves la ventana del programa, ¡felicidades! La instalación fue exitosa.**

---

## 📌 Parte 5: Crear un Acceso Directo (Opcional pero Recomendado)

Para no tener que abrir el símbolo del sistema cada vez:

### Método 1: Script BAT (Más Fácil)

1. Abre el **Bloc de notas** (Notepad)
2. Escribe exactamente esto:
   ```bat
   @echo off
   cd /d "C:\jusgadodepaz"
   python main.py
   pause
   ```
   ⚠️ **Ajusta** `C:\jusgadodepaz` a la ruta real donde está tu programa
3. Haz clic en **Archivo → Guardar como...**
4. En "Nombre": escribe `Ejecutar_Sistema.bat`
5. En "Tipo": selecciona **"Todos los archivos (*.*)"**
6. Guarda el archivo **en la carpeta del programa** (`C:\jusgadodepaz`)
7. Ahora puedes hacer **doble clic** en `Ejecutar_Sistema.bat` para abrir el programa

### Método 2: Acceso Directo en el Escritorio

1. Haz clic derecho en el archivo `Ejecutar_Sistema.bat` que creaste
2. Selecciona **"Enviar a → Escritorio (crear acceso directo)"**
3. Ahora tendrás un icono en el escritorio para abrir el programa

### Método 3: Asignar un Icono Bonito (Opcional)

1. Haz clic derecho en el acceso directo
2. Selecciona **"Propiedades"**
3. Haz clic en **"Cambiar icono..."**
4. Elige un icono que te guste
5. Haz clic en **"Aceptar"**

---

## 🔍 Verificación de la Instalación

### Lista de Verificación

✅ Python instalado y en el PATH  
✅ Carpeta del programa en ubicación permanente  
✅ Librerías instaladas (PyQt6, matplotlib, pandas, openpyxl)  
✅ Archivo `main.py` presente  
✅ Programa ejecuta sin errores  
✅ Se crea `cases.db` automáticamente  
✅ Carpetas `backups` y `documentos` creadas  

### Archivos que Debes Ver en la Carpeta

```
jusgadodepaz/
│
├── main.py                 ← Archivo principal
├── requirements.txt        ← Lista de librerías
├── cases.db               ← Base de datos (se crea automáticamente)
│
├── backups/               ← Respaldos automáticos
├── documentos/            ← Archivos adjuntos
│
├── controllers/           ← Carpeta de código
├── database/              ← Carpeta de código
├── models/                ← Carpeta de código
├── views/                 ← Carpeta de código
│
├── README.md              ← Documentación
├── MANUAL_COMPLETO.md     ← Manual de usuario
└── CATEGORIAS.md          ← Lista de categorías
```

---

## 🐛 Solución de Problemas Comunes

### Problema 1: "python no se reconoce como comando"

**Causa**: Python no está en el PATH

**Solución**:
1. Desinstala Python (Panel de Control → Programas)
2. Reinstala Python **marcando "Add Python to PATH"**
3. Reinicia la computadora
4. Intenta de nuevo

### Problema 2: "No module named 'PyQt6'"

**Causa**: Las librerías no se instalaron

**Solución**:
1. Abre cmd en la carpeta del programa
2. Ejecuta: `pip install -r requirements.txt`
3. Espera a que termine
4. Intenta ejecutar el programa de nuevo

### Problema 3: La ventana no se abre o se cierra inmediatamente

**Causa**: Puede haber un error en el código o falta un archivo

**Solución**:
1. Ejecuta el programa desde cmd: `python main.py`
2. Lee los mensajes de error que aparecen
3. Verifica que todos los archivos estén presentes
4. Verifica que `cases.db` se cree automáticamente

### Problema 4: Error de permisos al crear carpetas

**Causa**: No tienes permisos para escribir en esa ubicación

**Solución**:
1. Mueve el programa a tu carpeta de Documentos
2. O ejecuta el símbolo del sistema como **Administrador**:
   - Busca "cmd" en el menú inicio
   - Haz clic derecho
   - Selecciona **"Ejecutar como administrador"**

### Problema 5: "pip no se reconoce como comando"

**Causa**: pip no está instalado o no está en el PATH

**Solución**:
1. Intenta usar `python -m pip` en lugar de solo `pip`:
   ```cmd
   python -m pip install -r requirements.txt
   ```

### Problema 6: La instalación de librerías es muy lenta

**Causa**: Conexión lenta o problemas con el servidor PyPI

**Solución**:
1. Ten paciencia, puede tomar 10-15 minutos
2. Si falla, intenta de nuevo más tarde
3. Verifica tu conexión a internet

---

## 🔄 Actualización del Sistema

Si recibes una versión actualizada del programa:

### Paso 1: Respaldar tu base de datos

1. Busca el archivo `cases.db` en la carpeta del programa
2. **Cópialo** a un lugar seguro (USB, Documentos, etc.)
3. También copia la carpeta `documentos` si tienes archivos adjuntos

### Paso 2: Reemplazar los archivos

1. Descarga la nueva versión
2. Extrae los archivos **en una carpeta temporal**
3. **NO copies** `cases.db` (para mantener tus datos)
4. **NO copies** la carpeta `documentos` (para mantener tus archivos)
5. Copia todos los demás archivos y carpetas, reemplazando los antiguos

### Paso 3: Verificar

1. Ejecuta el programa: `python main.py`
2. Verifica que tus casos sigan ahí
3. Prueba las nuevas funciones

---

## 🆘 Necesitas Más Ayuda

### Documentación Disponible

- **[MANUAL_COMPLETO.md](MANUAL_COMPLETO.md)** - Cómo usar el sistema paso a paso
- **[GUIA_USUARIO.md](GUIA_USUARIO.md)** - Guía completa de funciones
- **[CATEGORIAS.md](CATEGORIAS.md)** - Lista de 21 categorías de casos
- **[GUIA_IMPORTACION.md](GUIA_IMPORTACION.md)** - Importar casos masivamente
- **[GUIA_DOCUMENTOS.md](GUIA_DOCUMENTOS.md)** - Sistema de documentos adjuntos

### Información del Sistema

Para obtener información técnica útil al pedir ayuda:

1. Abre cmd y ejecuta:
   ```cmd
   python --version
   pip list
   ```
2. Copia toda la información que aparece
3. Incluye esta información al pedir soporte

---

## ✅ Resumen Rápido

Para usuarios con experiencia:

```cmd
# 1. Instalar Python 3.8+ (con "Add to PATH" marcado)
# 2. Descargar/clonar el repositorio
# 3. Navegar a la carpeta
cd C:\jusgadodepaz

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar
python main.py
```

---

## 📝 Notas Importantes

- ⚠️ **Siempre** ejecuta el programa desde su carpeta permanente, no desde USB
- ⚠️ **Haz respaldos** periódicos de `cases.db`
- ⚠️ **No elimines** las carpetas `backups` y `documentos`
- ⚠️ El programa crea **respaldos automáticos** cada vez que lo abres
- ✅ Los respaldos están en la carpeta `backups`
- ✅ Puedes usar el sistema **sin conexión a internet** después de instalarlo

---

## 🎯 Inicio Rápido (Usuario Experimentado)

Si ya tienes Python instalado:

```cmd
pip install PyQt6 pandas matplotlib openpyxl
python main.py
```

---

**Versión**: 3.0  
**Última actualización**: Enero 2026  
**Plataforma**: Windows 10/11  
**Python requerido**: 3.8 o superior
