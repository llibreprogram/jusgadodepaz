# 📎 Sistema de Documentos Adjuntos

## Descripción General

El sistema de documentos permite adjuntar archivos (PDF, imágenes, documentos Word/Excel, etc.) a cada carpeta judicial, manteniendo toda la evidencia y documentación organizada digitalmente.

## Características

### ✅ Tipos de Archivos Soportados

- **Documentos**: PDF, DOC, DOCX, TXT, RTF
- **Imágenes**: JPG, JPEG, PNG, GIF, BMP
- **Hojas de cálculo**: XLS, XLSX, CSV
- **Archivos comprimidos**: ZIP, RAR, 7Z
- **Multimedia**: MP3, MP4, AVI, MOV

### 📂 Organización de Archivos

- Cada caso tiene su propia carpeta: `documents/case_{id}/`
- Nombres únicos con timestamp para evitar duplicados
- Se preserva el nombre original del archivo
- Metadata almacenada en base de datos

### 🔒 Seguridad

- Archivos almacenados localmente en el servidor
- Validación de tipos de archivo permitidos
- Control de acceso por caso
- Respaldo incluido en backup de base de datos

## Uso

### Ver Documentos de un Caso

1. Ve a la pestaña **"Ver Casos"**
2. Selecciona una carpeta en la tabla
3. Haz clic en el botón **"📎 Documentos"**
4. Se abrirá el diálogo de gestión de documentos

### Agregar Documento

1. En el diálogo de documentos, haz clic en **"📎 Agregar Documento"**
2. Selecciona el archivo desde tu computadora
3. (Opcional) Ingresa una descripción del documento
4. El archivo se copiará automáticamente a la carpeta del caso

### Abrir Documento

1. En la tabla de documentos, haz clic en el botón **"👁️"** (ojo)
2. El documento se abrirá con la aplicación predeterminada del sistema

### Eliminar Documento

1. En la tabla de documentos, haz clic en el botón **"🗑️"** (papelera)
2. Confirma la eliminación
3. El archivo se eliminará tanto del disco como de la base de datos

## Tabla de Documentos

La tabla muestra la siguiente información:

| Columna | Descripción |
|---------|-------------|
| **Archivo** | Nombre original del documento |
| **Tamaño** | Tamaño del archivo (KB/MB/GB) |
| **Descripción** | Descripción opcional del documento |
| **Fecha** | Fecha y hora de carga |
| **Acciones** | Botones para abrir o eliminar |

## Estadísticas

En el **Dashboard** se muestra:
- Total de documentos en el sistema
- Espacio total utilizado
- Integrado con las demás métricas del sistema

## Almacenamiento

### Estructura de Carpetas

```
documents/
├── case_1/
│   ├── 20251222_123045_denuncia.pdf
│   ├── 20251222_130512_evidencia.jpg
│   └── 20251222_142033_acta.docx
├── case_2/
│   └── 20251222_150045_sentencia.pdf
└── case_3/
    ├── 20251222_160123_informe.pdf
    └── 20251222_163045_foto1.jpg
```

### Base de Datos

Tabla `documents`:
- `id`: ID único del documento
- `case_id`: ID del caso asociado (FK)
- `filename`: Nombre único con timestamp
- `original_filename`: Nombre original del archivo
- `filepath`: Ruta completa del archivo
- `file_type`: Extensión del archivo
- `file_size`: Tamaño en bytes
- `description`: Descripción opcional
- `uploaded_at`: Timestamp de carga

## Ventajas

✅ **Centralización**: Todos los documentos del caso en un solo lugar  
✅ **Organización**: Estructura automática por caso  
✅ **Trazabilidad**: Registro de cuándo se agregó cada documento  
✅ **Búsqueda**: Metadata indexada en base de datos  
✅ **Respaldo**: Incluido en backups automáticos del sistema  
✅ **Acceso Rápido**: Apertura directa desde la interfaz  

## Mejores Prácticas

1. **Nombra los archivos descriptivamente** antes de subirlos
2. **Agrega descripciones** para facilitar identificación posterior
3. **Organiza por tipo**: denuncias, evidencias, actas, sentencias
4. **Verifica el tamaño**: archivos grandes pueden afectar respaldos
5. **Elimina duplicados**: evita tener múltiples versiones del mismo documento

## Límites y Consideraciones

- **Tamaño máximo**: Limitado por espacio en disco
- **Tipos permitidos**: Solo extensiones en lista blanca
- **Acceso**: Un documento pertenece a un solo caso
- **Eliminación en cascada**: Si se elimina un caso, se eliminan sus documentos

## Solución de Problemas

### No puedo abrir un documento
- Verifica que tengas la aplicación instalada para ese tipo de archivo
- Linux: Asegúrate de tener `xdg-utils` instalado
- Windows: El archivo se abrirá con la aplicación predeterminada
- macOS: Usa la aplicación predeterminada del sistema

### Error al agregar documento
- Verifica que el archivo exista
- Asegúrate de que el tipo de archivo esté permitido
- Verifica permisos de escritura en la carpeta `documents/`

### Documentos ocupan mucho espacio
- Revisa archivos grandes innecesarios
- Considera comprimir archivos grandes antes de subirlos
- Elimina versiones antiguas de documentos actualizados
