# Sistema de Gestión de Carpetas - Fiscalía

Programa de escritorio para registrar y analizar estadísticas de carpetas fiscales. Opera offline con base de datos SQLite local.

## Características

- Registro de carpetas con campos de fiscalía (carpeta, categoría/delito, etapa procesal, víctima, investigado, fechas clave, resultado, apelación, fiscal asignado, monto de reparación)
- Almacenamiento local en base de datos SQLite
- Interfaz gráfica intuitiva con PyQt6
- Generación de visualizaciones gráficas de estadísticas
- Búsqueda y filtrado de datos
- Exportación de datos a CSV y Excel

## Instalación

1. Instalar Python 3.8 o superior
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar: `python main.py`

## Uso

- **Registrar Carpeta**: Ingresar datos en el formulario y guardar.
- **Ver Carpetas**: Visualizar tabla, buscar por texto libre.
- **Estadísticas**: Generar gráficos de estadísticas.
- **Exportar**: Exportar datos a archivo.

## Estadísticas Disponibles

- Casos resueltos vs pendientes
- Tiempo promedio de resolución
- Casos por categoría
- Porcentaje de apelaciones
- Casos por mes
- Distribución por fiscal asignado
- Tasa de éxito
- Casos cerrados por trimestre
- Demoras promedio