# 📥 Guía de Importación Masiva

## Pasos para Importar Casos

### 1. Descargar Plantilla
- Ve a la pestaña **"Importar"**
- Haz clic en **"⬇️ Descargar Plantilla Excel"** o **"⬇️ Descargar Plantilla CSV"**
- Guarda el archivo en tu computadora

### 2. Llenar la Plantilla

#### Columnas Requeridas (obligatorias):
- `numero_carpeta`: Número único de carpeta (ej: RUC-2025-001)
- `categoria`: Categoría del delito
- `etapa_procesal`: Etapa del proceso
- `victima`: Nombre de la víctima
- `investigado`: Nombre del investigado

#### Columnas Opcionales:
- `fecha_denuncia`: Formato YYYY-MM-DD (ej: 2025-01-15)
- `fecha_formalizacion`: Formato YYYY-MM-DD
- `fecha_acusacion`: Formato YYYY-MM-DD
- `fecha_sentencia`: Formato YYYY-MM-DD
- `fecha_archivo`: Formato YYYY-MM-DD
- `monto_reparacion`: Número (ej: 5000.50)
- `estado_actual`: Estado del caso
- `resultado`: Resultado final
- `apelacion`: 0 (No) o 1 (Sí)
- `fiscal_asignado`: Nombre del fiscal

### 3. Validar Archivo
- Haz clic en **"🔍 Examinar"** y selecciona tu archivo
- Marca/desmarca **"Omitir carpetas duplicadas"** según prefieras
- Haz clic en **"✓ Validar Archivo"**
- Revisa la vista previa de los primeros 10 registros

### 4. Importar
- Si la validación es exitosa, haz clic en **"📤 Importar Casos"**
- Confirma la importación
- Espera a que termine el proceso
- Revisa el resumen de resultados

## 📋 Ejemplo de Archivo CSV

Ver archivo: `ejemplo_importacion.csv` en el directorio del proyecto

## ⚠️ Notas Importantes

1. **Números de Carpeta Únicos**: No puede haber dos casos con el mismo número de carpeta
2. **Fechas**: Usar formato YYYY-MM-DD (año-mes-día con 4 dígitos para año)
3. **Apelación**: Usar 1 para Sí, 0 para No
4. **Campos Vacíos**: Las columnas opcionales pueden dejarse vacías
5. **Duplicados**: Si hay carpetas duplicadas con la base de datos:
   - Con "Omitir duplicadas" ✓: Se saltarán sin error
   - Sin "Omitir duplicadas": Se mostrarán como errores

## 🎯 Ventajas

- ✅ Importa hasta 200+ casos en segundos
- ✅ Validación automática antes de importar
- ✅ Vista previa de los datos
- ✅ Manejo inteligente de duplicados
- ✅ Reporte detallado de errores
- ✅ Compatible con Excel y CSV
