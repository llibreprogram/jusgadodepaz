# 📖 Guía de Usuario - Sistema de Gestión de Casos

**Copyright © 2026 Rafael Llibre. Todos los derechos reservados.**

## 🎯 ¿Qué puedes hacer con este programa?

Este sistema te permite gestionar eficientemente todos los casos judiciales de tu fiscalía o juzgado de paz. A continuación, descubre todo lo que puedes hacer:

---

## 1️⃣ Gestión de Casos

### ✏️ Crear Nuevos Casos
- Registra casos judiciales con información completa
- Incluye: número de caso, víctima, investigado, fiscal asignado
- **Asigna categorías** (21 tipos específicos organizados por área):
  - **Violencia de Género**: Violencia doméstica, psicológica, sexual, feminicidio, entre otras
  - **Pensión Alimentaria**: Apertura, modificación, ejecución (con monto de pensión)
  - **Tránsito**: Accidentes, infracciones, otros tránsito
  - **Propiedad**: Usurpación, daños, invasión, despojo
  - **Patrimoniales**: Estafa, apropiación ilícita, extorsión
  - **Otros**: Homicidio, lesiones, amenazas, narcotráfico, etc.
- Define etapa procesal (9 etapas disponibles)
- Agrega fechas importantes: denuncia, audiencias, sentencias
- **Gestiona citaciones**: Registro completo de citas judiciales
- **Gestiona órdenes de arresto**: fecha de emisión, estado y cumplimiento
- **Rastrea cadena de fiscales**: Fiscal inicial, actual y de cierre
- **Historial de transferencias**: Declinaciones y cambios de jurisdicción
- Incluye descripción detallada y observaciones
- **Interfaz responsive**: se adapta automáticamente al tamaño de tu pantalla

### 🔍 Buscar y Filtrar
- Busca por número de caso, víctima, investigado o fiscal
- **Filtros de categoría mejorados**:
  - "Todas" - Muestra todos los casos
  - "Pensión alimentaria (todas)" - Todos los casos de pensión
  - "Tránsito (todas)" - Todos los casos de tránsito
  - 21 categorías específicas individuales
- Filtra por etapa procesal
- Filtra por estado actual
- Filtra por fiscal asignado
- Filtra por rango de fechas
- Solo casos apelados
- Combina múltiples filtros simultáneamente
- Resultados en tiempo real con paginación (10/25/50/100 por página)

### ✏️ Editar Casos Existentes
- Actualiza información de casos en curso
- Modifica fechas y etapas procesales
- Agrega nuevas observaciones
- Marca casos como archivados

### 🗑️ Eliminar Casos
- Elimina casos con confirmación de seguridad
- Elimina automáticamente documentos asociados
- Mantiene integridad de la base de datos

---

## 2️⃣ Dashboard y Estadísticas

### 📊 Estadísticas por Área (NUEVO)

El dashboard ahora muestra estadísticas organizadas por áreas temáticas:

#### 🚨 Violencia de Género (8 categorías)
- Violencia doméstica
- Violencia psicológica
- Violencia sexual
- Acoso sexual
- Feminicidio
- Maltrato familiar
- Incumplimiento violencia
- Otros violencia género

#### 👨‍👩‍👧 Pensión Alimentaria (3 categorías + montos)
- Pensión - Apertura
- Pensión - Modificación
- Pensión - Ejecución
- **Seguimiento de montos de pensión**

#### 🚗 Tránsito (3 categorías)
- Tránsito - Accidente
- Tránsito - Infracción
- Tránsito - Otros

#### 🏠 Propiedad (4 categorías)
- Usurpación simple
- Usurpación agravada
- Daños a la propiedad
- Invasión
- Despojo

#### 💰 Patrimoniales (3 categorías)
- Estafa
- Apropiación ilícita
- Extorsión

#### 📋 Otros Delitos
- Homicidio
- Lesiones
- Amenazas
- Narcotráfico
- Y más...

### 📈 Gráficos Avanzados

1. **Distribución por Área** - Casos agrupados por área temática
2. **Tipos de Resolución** - Sentencias, sobreseimientos, etc.
3. **Estado Actual** - Distribución de estados
4. **Etapas Procesales** - Casos por etapa
5. **Evolución Temporal** - Tendencias en el tiempo

### 📊 Métricas en Tiempo Real

#### Métricas Generales
- **Total de casos** en el sistema
- **Casos resueltos** (cerrados/archivados)
- **Casos pendientes** (activos en proceso)
- **Casos en juicio** (etapa judicial)
- **Tiempo promedio de resolución** (en días)
- **Porcentaje de apelaciones** sobre total de casos

#### 👥 Métricas de Fiscales (NUEVO)
- **Fiscales Activos**: Total de fiscales con casos asignados
- **Total Asignados**: Casos actualmente en proceso por todos los fiscales
- **Total Cerrados**: Casos cerrados por todos los fiscales
- **Declinaciones**: Total de transferencias realizadas
- **Mayor Carga**: Fiscal con más casos asignados actualmente
- **Más Productivo**: Fiscal con más casos cerrados

#### Estadísticas Detalladas por Fiscal
Acceso mediante botón "📊 Ver Detalles por Fiscal" con 5 pestañas:

**1. Casos Asignados** 📋
- Lista de fiscales con casos actualmente asignados
- Cantidad de casos por fiscal
- Porcentaje del total de casos

**2. Casos Recibidos** 📥
- Fiscales que recibieron casos inicialmente
- Total de casos recibidos
- Distribución de casos inicial

**3. Casos Cerrados** ✅
- Fiscales que han cerrado casos
- Cantidad de casos finalizados
- Indicador de productividad

**4. Transferencias** ↪️
- **Casos Declinados**: Transferencias salientes por fiscal
- **Casos Recibidos por Declinación**: Transferencias entrantes
- Análisis de flujo de casos entre fiscales

**5. Resumen** 📊
- Tabla completa con todas las métricas por fiscal
- Vista consolidada: Recibidos, Asignados, Cerrados, Declinados
- Totales generales del sistema

### 📅 Próximos Eventos
- Lista de audiencias próximas (30 días)
- Fechas de sentencia programadas
- Organizado cronológicamente
- Información de víctima e investigado

### 📋 Actividad Reciente
- Últimos 10 casos creados o modificados
- Fecha de última actualización
- Acceso rápido a casos recientes

---

## 3️⃣ Sistema de Alertas Inteligente

### 🔔 5 Tipos de Alertas Automáticas

#### ⚠️ Casos Inactivos
- Detecta casos sin actualizaciones en 30+ días
- Te ayuda a identificar casos olvidados
- Previene prescripciones

#### ⏱️ Juicios Prolongados
- Identifica juicios en curso por 90+ días
- Control de tiempos procesales
- Evita dilaciones innecesarias

#### 📅 Sin Fecha de Denuncia
- Alerta sobre casos sin fecha registrada
- Asegura completitud de información
- Facilita cumplimiento normativo

#### 🕐 Pendientes Prolongados
- Detecta casos en investigación 180+ días
- Evita casos estancados
- Optimiza carga de trabajo

#### 🚨 Órdenes de Arresto Pendientes
- **NUEVO**: Monitoreo de órdenes sin cumplir
- Alerta crítica si supera 30 días sin ejecutar
- Alerta media para órdenes recientes
- Facilita seguimiento de capturas pendientes

### 🚨 3 Niveles de Severidad
- **🔴 Alta** - Requiere atención inmediata
- **🟡 Media** - Revisar próximamente
- **🟢 Baja** - Monitoreo regular

---

## 4️⃣ Gestión de Citaciones

### 📅 Control de Citas Judiciales

#### Registro de Citaciones
- **Checkbox de activación**: Marca si existe citación vigente
- **Fecha de emisión**: Cuándo fue emitida la citación
- **Fecha de comparecencia**: Cuándo debe comparecer el citado
- **Estado de la citación**: 
  - Pendiente
  - Compareció
  - No compareció
  - Cancelada
- **Observaciones**: Detalles adicionales sobre la citación

#### Flujo de Trabajo
- **Citación → No comparecencia → Orden de arresto**: El sistema permite rastrear cuando una citación no cumplida genera una orden de arresto
- **Campo origen de orden**: Especifica si la orden proviene de:
  - Directa con denuncia
  - Por no comparecencia a cita
  - Orden judicial posterior
  - Otro

---

## 5️⃣ Gestión de Órdenes de Arresto

### 🚔 Control de Órdenes Judiciales

#### Registro de Órdenes
- **Checkbox de activación**: Marca si existe orden vigente
- **Fecha de emisión**: Cuándo fue emitida la orden
- **Estado de la orden**: 
  - Pendiente de cumplimiento
  - Cumplida
  - Cancelada
  - Revocada
- **Fecha de cumplimiento**: Cuándo se ejecutó la captura
- **Observaciones**: Detalles adicionales sobre la orden

#### Visualización en Tabla
- Columna dedicada "Orden Arresto" en la vista de casos
- **Códigos de color**:
  - 🔴 **Rojo**: Orden pendiente de cumplimiento
  - 🟢 **Verde**: Orden cumplida
  - 🟡 **Amarillo**: Orden cancelada o revocada
- Información visible al instante

#### Métricas en Dashboard
- **Órdenes Pendientes**: Total sin cumplir (color rojo)
- **Órdenes Cumplidas**: Total ejecutadas (color verde)
- Seguimiento estadístico de eficiencia

#### Alertas Automáticas
- Notificación para órdenes pendientes por más de 30 días
- Prioridad crítica en el sistema de alertas
- Facilita el seguimiento y cumplimiento

---

## 6️⃣ Historial de Fiscales

### 👥 Cadena de Custodia Fiscal

#### Campos de Fiscales
- **Fiscal inicial**: Quien recibió el caso originalmente
- **Fiscal asignado actual**: Quien está trabajando el caso ahora
- **Departamento/Jurisdicción**: Ubicación actual del caso
- **Fiscal de cierre**: Quien cerró el caso (cuando aplica)

#### Historial de Transferencias
- **Registro completo**: Todas las declinaciones y transferencias
- **Información detallada**:
  - Fiscal origen y destino
  - Departamento origen y destino
  - Motivo de transferencia
  - Fecha del movimiento
  - Observaciones
- **Tipos de acciones**:
  - 📥 Recepción inicial
  - ↪️ Declinación
  - 🔄 Transferencia
  - ✅ Cierre

#### Motivos de Transferencia
- Cambio de jurisdicción
- Declinación de competencia
- Redistribución de carga
- Cambio de corte
- Conflicto de interés
- Otro (personalizable)

#### Visualización
- **Timeline visual**: Línea de tiempo con código de colores
- **Acceso fácil**: Botón "Ver Historial de Transferencias" en formulario
- **Información completa**: Cada movimiento con detalles de origen y destino

#### Estadísticas
- Casos recibidos por cada fiscal
- Casos actualmente asignados
- Casos cerrados por fiscal
- Total de declinaciones salientes
- Total de recepciones por declinación

---

## 7️⃣ Documentos Adjuntos

### 📎 Gestión de Archivos

#### Tipos Soportados
- **Documentos**: PDF, DOC, DOCX, TXT, RTF
- **Imágenes**: JPG, PNG, GIF, BMP
- **Hojas de cálculo**: XLS, XLSX
- **Presentaciones**: PPT, PPTX
- **Comprimidos**: ZIP, RAR

#### Funcionalidades
- Adjunta documentos a cualquier caso
- Organización automática por carpetas
- Visualiza lista de documentos por caso
- Abre archivos directamente desde la aplicación
- Elimina documentos obsoletos
- Información de tamaño y fecha

### 📁 Estructura Automática
```
documents/
├── caso_123/
│   ├── denuncia.pdf
│   ├── sentencia.pdf
│   └── evidencia.jpg
└── caso_456/
    └── testimonio.docx
```

---

## 8️⃣ Importación Masiva

### 📤 Carga de Datos en Lote

#### Formatos Compatibles
- Archivos CSV (valores separados por comas)
- Archivos Excel (.xlsx, .xls)

#### Proceso de Importación
1. **Selecciona archivo** - Elige tu CSV o Excel
2. **Vista previa** - Verifica primeros 10 registros
3. **Validación automática** - Detecta errores
4. **Importación** - Carga todos los casos válidos
5. **Reporte** - Casos importados y errores

#### Validaciones Incluidas
✅ Formato de archivo correcto  
✅ Columnas requeridas presentes  
✅ Formato de fechas válido  
✅ Números de caso únicos  
✅ Categorías válidas  

#### Descarga Plantilla
- Genera archivo de ejemplo con estructura correcta
- Incluye casos de muestra
- Listo para llenar y cargar

---

## 9️⃣ Exportación y Reportes

### 📊 Gráficos Estadísticos Avanzados

#### 1. Distribución por Área
- Casos agrupados por área temática
- Violencia de género, pensión, tránsito, etc.
- Visualización de prioridades

#### 2. Tipos de Resolución
- Sentencias, sobreseimientos, archivos
- Análisis de resultados finales
- Eficacia del sistema

#### 3. Estado Actual
- Investigación, formalizado, juicio, etc.
- Distribución de casos activos
- Control de avance procesal

#### 4. Etapas Procesales
- Gráfico de pastel/torta
- Estado procesal actual
- Porcentajes visuales

#### 5. Casos por Fiscal
- Gráfico de barras
- Carga de trabajo por fiscal
- Distribución equitativa

### 📁 Exportación de Estadísticas (Excel)

**Genera reporte completo con 8 hojas:**

#### Hoja 1: Resumen General
- Total de casos en el sistema
- Casos resueltos y pendientes
- Tiempo promedio de resolución
- Porcentaje de apelaciones
- Métricas globales

#### Hoja 2: Estadísticas por Categoría
- Desglose de las 21 categorías específicas
- Cantidad de casos por categoría
- Porcentaje del total
- Identificación de áreas críticas

#### Hoja 3: Estadísticas por Área
- Violencia de Género: 8 categorías
- Pensión Alimentaria: 3 tipos
- Tránsito: 3 categorías
- Propiedad: 4 tipos
- Patrimoniales: 3 categorías
- Otros: categorías generales

#### Hoja 4: Por Fiscal
- Casos asignados por fiscal
- Casos cerrados por fiscal
- Carga de trabajo
- Productividad

#### Hoja 5: Por Etapa Procesal
- Distribución por etapa
- Casos en investigación, juicio, etc.
- Análisis de flujo procesal

#### Hoja 6: Por Estado Actual
- Casos activos por estado
- Archivados, sobreseídos, etc.
- Control de resultados

#### Hoja 7: Por Tipo de Resolución
- Sentencias condenatorias
- Sobreseimientos
- Archivos definitivos
- Efectividad del sistema

#### Hoja 8: Pensión Alimentaria Detallada
- **Lista completa de casos de pensión**
- **Montos de pensión registrados**
- Tipo (Apertura, Modificación, Ejecución)
- Fechas y fiscales asignados
- Seguimiento específico de pensiones
- Eficiencia del sistema
- Indicadores de gestión

### 📄 Exportación a Excel

#### Reportes Profesionales
- Formato profesional con colores
- Columnas anchas automáticamente
- Filtros aplicados
- Nombres de archivo con fecha
- Abre automáticamente tras exportar

#### Contenido Exportado
- Todos los campos del caso
- Casos filtrados (si hay filtros activos)
- Formato listo para imprimir
- Compatible con Microsoft Excel y LibreOffice

---

## 🔟 Paginación Inteligente

### 📑 Manejo de Grandes Volúmenes

#### Opciones de Visualización
- **25 casos** por página
- **50 casos** por página
- **100 casos** por página
- **200 casos** por página

#### Navegación
- Botones **Anterior** y **Siguiente**
- Indicador de página actual
- Total de páginas visible
- Atajos de teclado: `Ctrl+→` y `Ctrl+←`

#### Rendimiento
- Carga solo casos visibles
- Respuesta instantánea
- Maneja miles de casos sin problemas

---

## 1️⃣1️⃣ Backups Automáticos

### 💾 Protección de Datos

#### Sistema Automático
- Backup al iniciar la aplicación
- Backup al cerrar la aplicación
- Carpeta dedicada: `backups/`
- Nombres con fecha y hora

#### Formato de Backup
```
backups/
├── auto_backup_20251222_103816.db
├── auto_backup_20251222_140521.db
└── auto_backup_20251223_084312.db
```

#### Restauración
- Copia cualquier backup a `database.db`
- Reinicia la aplicación
- Recuperación completa de datos

---

## 1️⃣2️⃣ Interfaz Responsive y Adaptativa

### 📱 Diseño que se Adapta a Tu Pantalla

#### Ajuste Automático
- **Ventana adaptativa**: Se ajusta al 90% del tamaño de tu pantalla
- **Centrado automático**: Posición óptima al iniciar
- **Tamaño mínimo**: 1000x600 píxeles para pantallas pequeñas

#### Formularios con Scroll
- **Scroll inteligente**: Navega fácilmente por formularios largos
- **Barras personalizadas**: Diseño moderno en color azul
- **Campos expansibles**: Se ajustan al ancho disponible

#### Elementos Responsive
- **Campos de entrada**: Altura consistente de 32px
- **Espaciado optimizado**: 12px entre campos
- **Fuentes ajustables**: Tamaños optimizados para lectura
- **Botones adaptativos**: Se expanden con la ventana

#### Dashboard Dinámico
- **Métricas responsive**: Tarjetas que se ajustan automáticamente
- **Grid flexible**: Estadísticas organizadas dinámicamente
- **Scroll automático**: Para contenido que excede la pantalla
- **Fondo consistente**: Color oscuro (#0c1220) en toda la interfaz

#### Beneficios
- ✅ **Mejor legibilidad**: Texto y campos siempre visibles
- ✅ **Sin amontonamiento**: Elementos espaciados correctamente
- ✅ **Experiencia fluida**: Navegación sin frustraciones
- ✅ **Profesional**: Apariencia moderna en cualquier resolución

---

## 1️⃣3️⃣ Atajos de Teclado

### ⌨️ Productividad Máxima

| Atajo | Función |
|-------|---------|
| `Ctrl+S` | Guardar caso actual |
| `Ctrl+N` | Limpiar formulario (nuevo caso) |
| `Ctrl+F` | Enfocar búsqueda |
| `Ctrl+E` | Ir a pestaña de exportación |
| `F5` | Actualizar lista de casos |
| `Ctrl+→` | Página siguiente |
| `Ctrl+←` | Página anterior |

---

## 1️⃣4️⃣ Casos de Uso Prácticos

### 👨‍⚖️ Para Fiscales
- Seguimiento de casos asignados
- Control de audiencias próximas
- **Gestión de citaciones y comparecencias**
- **Monitoreo de órdenes de arresto**
- **Historial de transferencias recibidas**
- Estadísticas de desempeño
- Documentación organizada

### 👩‍💼 Para Asistentes Judiciales
- Registro de nuevos casos
- Actualización de fechas
- **Registro de citaciones**
- **Gestión de órdenes de arresto**
- **Registro de transferencias entre fiscales**
- Gestión de documentos
- Generación de reportes

### 👔 Para Directores/Coordinadores
- Dashboard general con métricas de fiscales
- **Análisis de carga por fiscal**: Ver quién tiene más casos asignados
- **Seguimiento de productividad**: Identificar fiscales más productivos
- **Reporte de declinaciones y transferencias**: Análisis de flujo de casos
- Estadísticas del equipo con vista consolidada
- **Seguimiento de citaciones pendientes**
- **Seguimiento de órdenes pendientes**
- Identificación de cuellos de botella
- Distribución equitativa de carga de trabajo
- **Exportación de estadísticas detalladas** por fiscal

### 📊 Para Análisis y Planificación
- Exportación de datos completos
- Gráficos estadísticos visuales
- Tendencias temporales
- **Análisis de flujo de casos entre fiscales**
- **Estadísticas de comparecencias**
- **Métricas de productividad por fiscal**
- **Análisis de carga de trabajo**
- **Identificación de patrones de transferencias**
- Reportes ejecutivos para superiores
- Dashboard con KPIs en tiempo real

---

## 💡 Consejos de Uso

### ✨ Mejores Prácticas

1. **Actualiza regularmente** - Mantén fechas y etapas al día
2. **Usa alertas** - Revisa diariamente la pestaña de alertas
3. **Registra citaciones** - Lleva control de todas las comparecencias
4. **Registra órdenes de arresto** - Mantén control de capturas pendientes
5. **Documenta transferencias** - Registra todas las declinaciones con motivo claro
6. **Adjunta documentos** - Centraliza archivos importantes
7. **Backups periódicos** - Guarda copias en ubicación segura
8. **Filtra inteligentemente** - Usa combinaciones de filtros
9. **Exporta reportes** - Genera estadísticas mensuales
10. **Completa información** - Llena todos los campos posibles
11. **Revisa dashboard** - Chequea métricas semanalmente
12. **Revisa historial** - Consulta el historial de fiscales para entender el flujo del caso
13. **Aprovecha el diseño responsive** - Ajusta el tamaño de ventana según tu necesidad

### 🚫 Errores Comunes a Evitar

❌ No registrar fecha de denuncia  
❌ Olvidar actualizar etapa procesal  
❌ No registrar citaciones emitidas  
❌ No actualizar estado de comparecencias  
❌ No registrar órdenes de arresto vigentes  
❌ No actualizar estado de órdenes cumplidas  
❌ No documentar transferencias entre fiscales  
❌ No especificar motivo de declinación  
❌ No adjuntar documentos importantes  
❌ Ignorar alertas de casos inactivos  
❌ No hacer backups manuales adicionales  

---

## 🆘 Solución de Problemas

### Problema: No aparecen casos
- Verifica que no haya filtros activos
- Presiona `F5` para actualizar
- Verifica la base de datos en carpeta raíz

### Problema: Campos se ven apretados o cortados
- El sistema ahora es responsive y se ajusta automáticamente
- Intenta maximizar la ventana o ajustar su tamaño
- Usa el scroll para navegar por formularios largos

### Problema: No se ven los botones en el dashboard
- Los botones tienen color azul brillante sobre fondo oscuro
- Si no se ven, intenta reiniciar la aplicación
- Verifica que no haya errores en la consola

### Problema: No se pueden adjuntar documentos
- Verifica que existe la carpeta `documents/`
- Confirma permisos de escritura
- Revisa espacio en disco

### Problema: Errores al importar
- Descarga plantilla de ejemplo
- Verifica formato de fechas (YYYY-MM-DD)
- Asegura números de caso únicos

### Problema: Gráficos no se generan
- Instala matplotlib: `pip install matplotlib`
- Verifica que hay datos para graficar
- Revisa consola de errores

### Problema: Las alertas de órdenes de arresto no aparecen
- Verifica que el caso tenga marcado "Tiene orden de arresto vigente"
- Confirma que el estado sea "Pendiente de cumplimiento"
- Actualiza el dashboard con el botón 🔄

---

## 📞 Soporte

Para soporte técnico o sugerencias:
- Revisa esta documentación completa
- Consulta archivos GUIA_*.md adicionales
- Contacta al administrador del sistema

---

**Sistema de Gestión de Casos v3.0**  
*Herramienta profesional para administración judicial eficiente*

**Nuevas funcionalidades v3.0:**
- ✨ **Sistema de Citaciones**: Gestión completa de citas judiciales y comparecencias
- ✨ **Historial de Fiscales**: Rastreo completo de la cadena de custodia fiscal
- ✨ **Transferencias y Declinaciones**: Registro detallado de movimientos entre fiscales
- ✨ **Estadísticas de Fiscales**: Análisis de carga y desempeño por fiscal
- ✨ Gestión completa de órdenes de arresto con origen
- ✨ Interfaz responsive y adaptativa
- ✨ Dashboard optimizado con scroll inteligente

**Funcionalidades v2.5:**
- ✨ Gestión completa de órdenes de arresto
- ✨ Métricas mejoradas con seguimiento de órdenes
- ✨ Alertas automáticas para órdenes pendientes

Última actualización: Diciembre 2025
