# 📊 Propuesta: Sistema de Estadísticas Detalladas por Tipo de Caso

## 🎯 Objetivo
Implementar un sistema de estadísticas completo que refleje **los tipos de casos reales** que maneja el juzgado de paz, con capacidad de exportación e impresión.

---

## 📋 Análisis de lo que YA TIENES Funcionando

### ✅ Sistema Actual
Tu sistema actualmente tiene:

1. **16 Categorías genéricas:**
   - Delitos contra la propiedad
   - Delitos contra la persona
   - Delitos sexuales
   - Corrupción
   - Narcotráfico
   - Robo simple
   - Daños a la propiedad
   - Golpes y herida
   - Amenazas
   - Usurpación simple
   - Violencia intrafamiliar
   - Estafa
   - Accidente de tránsito
   - Penal laboral
   - Pensión alimentaria
   - Otros

2. **Dashboard funcional con:**
   - Total de casos
   - Casos resueltos
   - Casos pendientes
   - Tiempo promedio de resolución
   - Estadísticas por fiscal
   - Órdenes de arresto

3. **Sistema de exportación:**
   - Exportar a Excel
   - Exportar a CSV
   - Gráficos estadísticos (5 tipos)

4. **Gráficos disponibles:**
   - Casos por categoría
   - Casos por etapa
   - Evolución temporal
   - Casos por fiscal
   - Tasa de resolución

---

## 🆕 NUEVAS Categorías Específicas del Juzgado

### Categorías que quieres agregar:

**PENSIÓN ALIMENTARIA:**
1. Pensión (expedientes activos)
2. Acuerdos homologados de pensión
3. Desistimiento de pensión
4. Conciliaciones de pensión
5. No acuerdo de pensión
6. Condenas de pensión

**TRÁNSITO:**
7. Tránsito (daño a la propiedad)
8. Desistimiento de tránsito
9. Conciliación de tránsito
10. Condenas de tránsito
11. Apertura a juicio de tránsito
12. Auto no a lugar de tránsito

**OTROS CASOS:**
13. Violación a la propiedad
14. Riña (penal)
15. Penal laboral
16. Medidas de protección
17. Daño a la propiedad (general)
18. Conciliaciones de riña
19. Conciliaciones de daño a la propiedad
20. No acuerdo de daño a la propiedad
21. Archivos (casos archivados)

---

## 💡 PROPUESTA DE IMPLEMENTACIÓN

### Opción 1: Mantener Sistema Simple (RECOMENDADA)

**Estructura:**
- Agregar las nuevas categorías específicas
- Mantener el sistema actual de estadísticas
- Mejorar el dashboard con secciones por tipo de caso
- Agregar filtros específicos

**Ventajas:**
- ✅ Fácil de implementar
- ✅ Los usuarios ya conocen el sistema
- ✅ No requiere cambios en la base de datos
- ✅ Se puede hacer en 1-2 horas

**Implementación:**
1. Reemplazar las 16 categorías actuales por las 21 nuevas
2. Agregar nueva sección en el dashboard: "Estadísticas por Área"
3. Crear tarjetas agrupadas:
   - 📋 Pensión Alimentaria (6 subcategorías)
   - 🚗 Tránsito (6 subcategorías)
   - ⚖️ Otros Casos (9 subcategorías)
4. Mejorar exportación con hoja separada por área

---

### Opción 2: Sistema Avanzado con Subcategorías

**Estructura:**
- Mantener categorías principales (Pensión, Tránsito, Penal, etc.)
- Agregar campo "Subcategoría" o "Tipo de resolución"
- Dashboard con análisis por área y resolución

**Ventajas:**
- ✅ Más organizado
- ✅ Análisis más detallados
- ✅ Reportes por tipo de resolución

**Desventajas:**
- ❌ Requiere cambios en base de datos
- ❌ Más complejo de implementar
- ❌ Los usuarios necesitan entrenamiento

---

## 🎨 Diseño del Nuevo Dashboard

### Sección 1: Métricas Generales (Ya existe)
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Total Casos │  Resueltos  │ Pendientes  │  En Juicio  │
│     245     │     180     │     50      │     15      │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

### Sección 2: Estadísticas por Área (NUEVA)

**📋 PENSIÓN ALIMENTARIA**
```
┌──────────────────────────────────────────────────────┐
│ Total Pensión: 85 casos                              │
├────────────────────┬─────────────────────────────────┤
│ Activos            │ 25 casos                        │
│ Acuerdos           │ 30 casos                        │
│ Conciliaciones     │ 15 casos                        │
│ Condenas           │ 8 casos                         │
│ No acuerdos        │ 4 casos                         │
│ Desistimientos     │ 3 casos                         │
└────────────────────┴─────────────────────────────────┘
```

**🚗 TRÁNSITO**
```
┌──────────────────────────────────────────────────────┐
│ Total Tránsito: 67 casos                             │
├────────────────────┬─────────────────────────────────┤
│ Activos            │ 20 casos                        │
│ Conciliaciones     │ 25 casos                        │
│ Condenas           │ 10 casos                        │
│ Aperturas a juicio │ 5 casos                         │
│ Auto no a lugar    │ 4 casos                         │
│ Desistimientos     │ 3 casos                         │
└────────────────────┴─────────────────────────────────┘
```

**⚖️ OTROS CASOS**
```
┌──────────────────────────────────────────────────────┐
│ Total Otros: 93 casos                                │
├────────────────────┬─────────────────────────────────┤
│ Riña penal         │ 30 casos                        │
│ Daño a propiedad   │ 25 casos                        │
│ Penal laboral      │ 20 casos                        │
│ Medidas protección │ 10 casos                        │
│ Archivos           │ 8 casos                         │
└────────────────────┴─────────────────────────────────┘
```

### Sección 3: Gráficos Visuales (Mejorado)

**Nuevo Gráfico: "Distribución por Área"**
- Gráfico de pastel con 3 secciones:
  - Pensión (35%)
  - Tránsito (27%)
  - Otros (38%)

**Nuevo Gráfico: "Tipos de Resolución"**
- Gráfico de barras:
  - Conciliaciones: 40 casos
  - Condenas: 18 casos
  - Acuerdos: 30 casos
  - No acuerdos: 8 casos
  - Desistimientos: 6 casos
  - Archivos: 8 casos

---

## 📊 Sistema de Exportación Mejorado

### Exportar Estadísticas Completas

**Archivo Excel con 5 hojas:**

1. **Hoja "Resumen General"**
   - Total de casos por área
   - Porcentajes
   - Comparación mensual

2. **Hoja "Pensión Alimentaria"**
   - Tabla con todos los casos de pensión
   - Subtotales por tipo
   - Montos totales (si aplica)

3. **Hoja "Tránsito"**
   - Tabla con todos los casos de tránsito
   - Subtotales por tipo
   - Análisis de resoluciones

4. **Hoja "Otros Casos"**
   - Tabla con riña, laboral, etc.
   - Subtotales por tipo

5. **Hoja "Gráficos"**
   - Gráficos incrustados listos para imprimir

### Botón: "📊 Exportar Estadísticas Completas"
- Genera archivo con fecha: `estadisticas_completas_2024-12-29.xlsx`
- Incluye todos los gráficos
- Listo para imprimir o presentar

---

## 🖨️ Sistema de Impresión

### Nuevo Botón: "🖨️ Imprimir Reporte"

**Genera documento PDF con:**
1. Portada con fecha y logo
2. Resumen ejecutivo (1 página)
3. Estadísticas por área (3 páginas)
4. Gráficos visuales (2 páginas)
5. Tabla completa de casos (anexo)

---

## 🔧 Lista de Cambios Técnicos

### 1. Actualizar Categorías (archivo: `views/main_window.py`)
```python
self.categories = [
    # PENSIÓN ALIMENTARIA
    'Pensión alimentaria',
    'Acuerdo homologado de pensión',
    'Desistimiento de pensión',
    'Conciliación de pensión',
    'No acuerdo de pensión',
    'Condena de pensión',
    
    # TRÁNSITO
    'Tránsito - Daño a propiedad',
    'Desistimiento de tránsito',
    'Conciliación de tránsito',
    'Condena de tránsito',
    'Apertura a juicio de tránsito',
    'Auto no a lugar - Tránsito',
    
    # OTROS
    'Violación a la propiedad',
    'Riña penal',
    'Penal laboral',
    'Medidas de protección',
    'Daño a la propiedad',
    'Conciliación de riña',
    'Conciliación de daño a propiedad',
    'No acuerdo de daño a propiedad',
    'Archivo',
    'Otros'
]
```

### 2. Agregar Función de Agrupación
```python
def get_area_from_category(self, category):
    """Determina el área según la categoría"""
    pension_keywords = ['pensión', 'pension']
    transito_keywords = ['tránsito', 'transito']
    
    if any(k in category.lower() for k in pension_keywords):
        return 'Pensión Alimentaria'
    elif any(k in category.lower() for k in transito_keywords):
        return 'Tránsito'
    else:
        return 'Otros Casos'
```

### 3. Nueva Función para Estadísticas por Área
```python
def get_statistics_by_area(self):
    """Genera estadísticas agrupadas por área"""
    cases = self.controller.get_all_cases()
    
    areas = {
        'Pensión Alimentaria': [],
        'Tránsito': [],
        'Otros Casos': []
    }
    
    for case in cases:
        area = self.get_area_from_category(case.categoria)
        areas[area].append(case)
    
    return areas
```

### 4. Nuevo Widget en Dashboard
```python
def create_area_statistics_widget(self):
    """Crea widget con estadísticas por área"""
    # Código para crear las 3 tarjetas de área
    # Similar al widget de fiscales actual
```

### 5. Nueva Función de Exportación
```python
def export_complete_statistics(self):
    """Exporta estadísticas completas a Excel con múltiples hojas"""
    # Genera archivo Excel con 5 hojas
```

### 6. Nuevos Gráficos
```python
def plot_distribution_by_area(self):
    """Gráfico de pastel con distribución por área"""
    
def plot_resolution_types(self):
    """Gráfico de barras con tipos de resolución"""
```

---

## 📅 Plan de Implementación

### Fase 1: Básica (2-3 horas)
1. ✅ Actualizar lista de categorías
2. ✅ Agregar función de agrupación por área
3. ✅ Crear widget de estadísticas por área en dashboard
4. ✅ Probar que todo funciona

### Fase 2: Gráficos (1-2 horas)
1. ✅ Crear gráfico de distribución por área
2. ✅ Crear gráfico de tipos de resolución
3. ✅ Agregar botones en pestaña de exportación

### Fase 3: Exportación Avanzada (2-3 horas)
1. ✅ Implementar exportación con múltiples hojas
2. ✅ Agregar formato profesional
3. ✅ Incluir gráficos en el Excel

### Fase 4: Impresión (Opcional, 2-3 horas)
1. ⚪ Instalar librería ReportLab para PDF
2. ⚪ Crear plantilla de reporte
3. ⚪ Generar PDF con estadísticas

---

## 🎯 Recomendación Final

### MI RECOMENDACIÓN: Opción 1 con Fases 1, 2 y 3

**Por qué:**
1. ✅ **Rápido de implementar** (6-8 horas total)
2. ✅ **Mantiene sistema simple** que ya conoces
3. ✅ **Estadísticas detalladas** como necesitas
4. ✅ **Exportación profesional** para reportes
5. ✅ **Impresión fácil** desde Excel

**Resultado:**
- Dashboard con 3 secciones de estadísticas (Pensión, Tránsito, Otros)
- 21 categorías específicas de tu juzgado
- 7 tipos de gráficos (5 actuales + 2 nuevos)
- Exportación Excel con 5 hojas separadas
- Todo listo para imprimir

---

## ❓ Siguiente Paso

**¿Qué te parece esta propuesta?**

Si estás de acuerdo, puedo empezar a implementar:
1. Las nuevas categorías
2. El widget de estadísticas por área
3. Los nuevos gráficos
4. La exportación mejorada

O si prefieres ajustar algo, dime qué cambiarías.

**Tiempo estimado total: 6-8 horas de trabajo**

---

## 📝 Nota Importante

Para **monto de pensión** (dinero que tienen que pagar), podríamos:
- Agregar un campo nuevo: "Monto mensual de pensión"
- Solo se llena en casos de pensión
- El dashboard mostraría: "Monto total asignado: $XX,XXX"
- Esto requeriría cambio en la base de datos

¿Te interesa agregar este campo de monto?
