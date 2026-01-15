# 🏛️ Sistema de Gestión de Casos - Ministerio Público

Sistema integral de gestión de carpetas judiciales para fiscalías y juzgados de paz, desarrollado con PyQt6 y SQLite.

**Copyright © 2026 Rafael Llibre. Todos los derechos reservados.**

## ✨ Características Destacadas

✅ **Gestión Completa de Casos** - Registro, edición y seguimiento  
✅ **Dashboard Avanzado** - Métricas, gráficos y estadísticas detalladas  
✅ **21 Categorías Específicas** - Pensión, tránsito, violencia y más  
✅ **Sistema de Alertas** - 4 tipos con 3 niveles de severidad  
✅ **Documentos Adjuntos** - Archivos organizados por caso  
✅ **Importación Masiva** - CSV/Excel con validación  
✅ **Exportación Estadísticas** - Excel con 8 hojas analíticas  
✅ **Búsqueda y Filtros** - Múltiples criterios con filtros generales  
✅ **Paginación Inteligente** - Maneja miles de casos  
✅ **Backups Automáticos** - Protección de datos  

## 🚀 Inicio Rápido

### Instalación

**Windows**: Ver [INSTALACION_WINDOWS.md](INSTALACION_WINDOWS.md) para guía detallada paso a paso

**Linux/Mac**:
```bash
# Instalar dependencias
pip install -r requirements.txt

# O instalar individualmente
pip install PyQt6 pandas matplotlib openpyxl

# Ejecutar aplicación
python main.py
```

## 📊 Dashboard

### Estadísticas por Área
- **Violencia de Género**: 8 categorías específicas
- **Pensión Alimentaria**: 3 tipos con seguimiento de montos
- **Tránsito**: 3 categorías (accidentes, infracciones, otros)
- **Propiedad**: 4 tipos de delitos
- **Patrimoniales**: 3 categorías
- **Otros**: Categorías generales

### Gráficos Analíticos
- Distribución de casos por área
- Tipos de resolución
- Estado actual de casos
- Etapas procesales
- Evolución temporal

### Métricas en Tiempo Real
- Próximos eventos importantes (30 días)
- Actividad reciente
- Casos por fiscal
- Tasas de resolución

## 📎 Documentos

- Adjuntar PDFs, imágenes, documentos
- Organización automática por caso
- Apertura directa desde interfaz
- Control de versiones

## 🔔 Alertas

- Casos inactivos (30+ días)
- Juicios prolongados (90+ días)
- Sin fecha de denuncia
- Pendientes prolongados (180+ días)

## ⌨️ Atajos

- `Ctrl+S` - Guardar
- `Ctrl+N` - Nuevo caso
- `Ctrl+F` - Buscar
- `F5` - Actualizar
- `Ctrl+→/←` - Navegar páginas

## 📚 Documentación

- [INSTALACION_WINDOWS.md](INSTALACION_WINDOWS.md) - Instalación paso a paso en Windows
- [MANUAL_COMPLETO.md](MANUAL_COMPLETO.md) - Manual detallado para todos los usuarios
- [GUIA_USUARIO.md](GUIA_USUARIO.md) - Guía de uso del sistema
- [CATEGORIAS.md](CATEGORIAS.md) - Lista completa de 21 categorías
- [GUIA_IMPORTACION.md](GUIA_IMPORTACION.md) - Importación masiva
- [GUIA_DOCUMENTOS.md](GUIA_DOCUMENTOS.md) - Sistema de documentos

## 📈 Estadísticas y Reportes

### Exportación de Estadísticas Excel (8 hojas)
1. **Resumen General** - Métricas globales del sistema
2. **Por Categoría** - Desglose de 21 categorías específicas
3. **Por Área** - Agrupación por áreas temáticas
4. **Por Fiscal** - Carga de trabajo y desempeño
5. **Por Etapa** - Distribución procesal
6. **Por Estado** - Estados actuales
7. **Resoluciones** - Tipos de cierre
8. **Pensión Alimentaria** - Montos y seguimiento específico

---

## 📄 Licencia y Derechos de Autor

**Sistema de Gestión de Casos Judiciales**  
Copyright © 2026 Rafael Llibre  
Todos los derechos reservados.

Ver [LICENSE.md](LICENSE.md) para términos completos de uso.

---

**Desarrollado por Rafael Llibre - 2026**

**Versión 3.0** | Diciembre 2025
