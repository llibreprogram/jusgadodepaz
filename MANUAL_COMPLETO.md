# 📘 Manual Completo - Sistema de Gestión de Casos Judiciales

**Copyright © 2026 Rafael Llibre. Todos los derechos reservados.**

## 🎓 Guía Para Principiantes y Usuarios Avanzados

Este manual está diseñado para que **cualquier persona** pueda usar el sistema, sin importar su experiencia con computadoras.

---

## 📋 Tabla de Contenidos

1. [Primeros Pasos](#primeros-pasos)
2. [Conociendo la Interfaz](#conociendo-la-interfaz)
3. [Crear Tu Primer Caso](#crear-tu-primer-caso)
4. [Buscar y Ver Casos](#buscar-y-ver-casos)
5. [Editar Casos Existentes](#editar-casos-existentes)
6. [Gestión de Citaciones](#gestión-de-citaciones)
7. [Gestión de Órdenes de Arresto](#gestión-de-órdenes-de-arresto)
8. [Transferencias Entre Fiscales](#transferencias-entre-fiscales)
9. [Adjuntar Documentos](#adjuntar-documentos)
10. [Dashboard y Estadísticas](#dashboard-y-estadísticas)
11. [Alertas del Sistema](#alertas-del-sistema)
12. [Importar Casos Masivamente](#importar-casos-masivamente)
13. [Exportar Reportes](#exportar-reportes)
14. [Consejos y Trucos](#consejos-y-trucos)

---

## 🚀 Primeros Pasos

### ¿Qué es este programa?

Este es un sistema para **gestionar casos judiciales**. Piensa en él como un archivero digital inteligente que:
- Guarda información de todos tus casos
- Te recuerda fechas importantes
- Genera reportes automáticos
- Mantiene todo organizado y seguro

### Iniciar el Programa

**Paso 1:** Encuentra el archivo llamado `main.py` en tu carpeta del programa

**Paso 2:** Haz doble clic sobre él, o abre una terminal y escribe:
```bash
python main.py
```

**Paso 3:** Espera unos segundos. Verás una ventana abrirse con el sistema.

✅ **¡Listo!** Ya tienes el programa abierto.

---

## 👀 Conociendo la Interfaz

Cuando abres el programa, verás **6 pestañas principales** en la parte superior:

### 1. 📊 Dashboard (Tablero Principal)
- Es la primera pantalla que ves
- Muestra resumen de todos tus casos
- Incluye estadísticas y números importantes
- **Es como el "escritorio" de tu oficina digital**

### 2. 📝 Casos
- Aquí ves la lista de TODOS tus casos
- Puedes crear nuevos casos
- Puedes editar o eliminar casos existentes
- **Es tu "archivero principal"**

### 3. 🔔 Alertas
- Muestra casos que necesitan atención
- Por ejemplo: casos sin actividad, audiencias próximas
- **Es tu "asistente personal" que te recuerda cosas**

### 4. 📂 Documentos
- Ves todos los archivos adjuntos
- Puedes abrir PDFs, imágenes, etc.
- **Es tu "caja de archivos físicos", pero digital**

### 5. 📥 Importar
- Para cargar muchos casos a la vez desde Excel
- **Solo úsalo si tienes datos en hojas de cálculo**

### 6. 📤 Exportar
- Para sacar datos del sistema
- Crea reportes en Excel
- Genera gráficos estadísticos
- **Es tu "fotocopiadora de reportes"**

---

## ✏️ Crear Tu Primer Caso

### Paso a Paso Muy Detallado

#### Paso 1: Ir a la Pestaña "Casos"
- Haz clic en la pestaña **"📝 Casos"** en la parte superior
- La pestaña se pondrá de color más claro (significa que está seleccionada)

#### Paso 2: Ver el Formulario en Blanco
Verás un formulario grande con muchos campos vacíos. **No te preocupes**, no tienes que llenar todos. Vamos uno por uno:

#### Paso 3: Llenar la Información Básica

**🔢 Número de Carpeta** *(OBLIGATORIO)*
- Este es el número único del caso
- Ejemplo: `2024-001`, `JPZ-2024-123`, `001/2024`
- Escribe el número que usa tu oficina
- ⚠️ **Importante:** Cada caso debe tener un número diferente

**👤 Víctima** *(OBLIGATORIO)*
- Nombre completo de la víctima
- Ejemplo: `María Pérez González`
- Solo escribe el nombre, sin más detalles

**🔍 Investigado** *(OBLIGATORIO)*
- Nombre de la persona investigada
- Ejemplo: `Juan López Martínez`
- Si no sabes el nombre, escribe: `Desconocido` o `Por identificar`

**👨‍⚖️ Fiscal Asignado** *(OBLIGATORIO)*
- Nombre del fiscal que tiene el caso AHORA
- Ejemplo: `Lic. Carlos Ramírez`
- Este es el fiscal actual

#### Paso 4: Seleccionar Categoría del Delito

- Haz clic en el menú desplegable **"Categoría"**
- Verás una lista organizada con **21 categorías específicas** agrupadas por área:

**🚨 Violencia de Género (8 tipos):**
  - Violencia doméstica
  - Violencia psicológica
  - Violencia sexual
  - Acoso sexual
  - Feminicidio
  - Maltrato familiar
  - Incumplimiento medidas de violencia
  - Otros violencia de género

**👨‍👩‍👧 Pensión Alimentaria (3 tipos):**
  - Pensión - Apertura
  - Pensión - Modificación  
  - Pensión - Ejecución
  - 💡 **Especial**: Si eliges pensión, podrás registrar el monto mensual

**🚗 Tránsito (3 tipos):**
  - Tránsito - Accidente
  - Tránsito - Infracción
  - Tránsito - Otros

**🏠 Propiedad (5 tipos):**
  - Usurpación simple
  - Usurpación agravada
  - Daños a la propiedad
  - Invasión
  - Despojo

**💰 Patrimoniales (3 tipos):**
  - Estafa
  - Apropiación ilícita
  - Extorsión

**📋 Otros Delitos:**
  - Homicidio
  - Lesiones
  - Amenazas
  - Narcotráfico
  - Robo
  - Hurto
  - Delitos contra la persona
  - Otros

- Haz clic en el que corresponde a tu caso
- 📝 **Ver lista completa**: Consulta [CATEGORIAS.md](CATEGORIAS.md) para descripciones detalladas

#### Paso 4.1: Monto de Pensión (Solo para Pensión Alimentaria)

**💰 Si elegiste una categoría de Pensión**, verás un campo adicional:

- **Monto de Pensión (S/)**
- Escribe el monto mensual de la pensión
- Ejemplo: `800.00` (para 800 soles)
- Solo números y punto decimal
- Este campo aparece SOLO para casos de pensión

#### Paso 5: Seleccionar Etapa Procesal

- Haz clic en el menú desplegable **"Etapa"**
- Elige en qué fase está el caso:
  - **Denuncia Recibida**: Acaba de llegar
  - **Investigación**: Están reuniendo pruebas
  - **Audiencia Preliminar**: Primera audiencia
  - **Juicio**: Está en juicio
  - **Sentencia**: Ya hay sentencia
  - **Apelación**: Alguien apeló
  - **Archivado**: Caso cerrado
  - **Suspendido**: En pausa temporal
  - **Desistimiento**: La víctima desistió

#### Paso 6: Agregar Fechas (Opcional pero Recomendado)

**📅 Fecha de Denuncia**
- Haz clic en el campo de fecha
- Aparecerá un calendario
- Selecciona el día que se hizo la denuncia
- Formato: `2024-12-25` (año-mes-día)

**📅 Fecha de Audiencia** (si ya está programada)
- Igual que la anterior
- Selecciona la fecha de la audiencia

**📅 Fecha de Sentencia** (solo si ya hay sentencia)
- Igual que las anteriores

**📅 Última Actualización**
- Esta se llena automáticamente
- No la toques

#### Paso 7: Información de Fiscales (Avanzado)

**👨‍⚖️ Fiscal Inicial**
- El fiscal que recibió el caso originalmente
- Puede ser diferente del fiscal actual si hubo transferencias

**🏢 Departamento**
- Nombre de la corte o jurisdicción
- Ejemplo: `Juzgado de Paz San Pedro`, `Primera Corte`

**👨‍⚖️ Fiscal de Cierre** (solo si el caso está cerrado)
- Quien cerró el caso

#### Paso 8: Descripción y Observaciones

**📄 Descripción del Caso**
- Aquí escribe un resumen del caso
- Ejemplo: `Robo de vehículo marca Toyota, placa ABC123, ocurrido en parqueo de centro comercial`
- Puedes escribir varios párrafos
- Usa la barra de desplazamiento si necesitas más espacio

**📝 Observaciones**
- Notas adicionales
- Cualquier cosa que consideres importante
- Ejemplo: `Víctima solicita protección. Testigos disponibles.`

#### Paso 9: Guardar el Caso

**Opción 1: Usar el Botón**
- Baja hasta el final del formulario
- Haz clic en el botón verde **"💾 Guardar Caso"**

**Opción 2: Atajo de Teclado**
- Presiona `Ctrl + S` en tu teclado
- (Ctrl y S al mismo tiempo)

✅ **¡Listo!** Verás un mensaje: "✓ Caso guardado correctamente"

El caso ahora aparecerá en la tabla de la derecha.

---

## 🔍 Buscar y Ver Casos

### Método 1: Ver Todos los Casos

1. Ve a la pestaña **"Ver Casos"**
2. Selecciona **"Todas"** en el filtro de categoría
3. Mira la tabla grande - ahí están TODOS tus casos
4. Cada fila es un caso diferente

### Método 2: Buscar un Caso Específico

**Por Búsqueda de Texto:**

1. Encuentra la caja que dice **"Buscar texto libre..."** arriba de la tabla
2. Haz clic dentro de la caja
3. Escribe lo que buscas:
   - Número de caso: `2024-001`
   - Nombre de víctima: `María`
   - Nombre de investigado: `Juan`
   - Nombre de fiscal: `Ramírez`
4. ¡La tabla se filtra automáticamente mientras escribes!

**Por Filtros de Categoría:**

Ahora tienes **filtros especiales** para búsqueda rápida:

1. **"Todas"** - Muestra absolutamente todos los casos

2. **Filtros Generales** (acceso rápido):
   - **"Pensión alimentaria (todas)"** - Todos los casos de pensión
   - **"Tránsito (todas)"** - Todos los casos de tránsito

3. **21 Categorías Específicas**:
   - Violencia doméstica, psicológica, sexual, etc.
   - Pensión - Apertura, Modificación, Ejecución
   - Tránsito - Accidente, Infracción, Otros
   - Usurpación, Estafa, Extorsión, etc.

4. **Otros Filtros Disponibles**:
   - **"Etapa"**: Filtra por fase procesal
   - **"Estado"**: Investigación, Formalizado, En juicio, etc.
   - **"Fiscal"**: Busca por nombre de fiscal
   - **"Solo apelados"**: Marca esta casilla
   - **"Fecha desde/hasta"**: Rango de fechas

5. Los filtros se aplican **automáticamente**
6. Para limpiar: Haz clic en **"🧹 Limpiar filtros"**

### Método 3: Navegar con Paginación

Si tienes muchos casos:
1. Abajo de la tabla verás: **"Página 1 de X"**
2. Usa los botones **"⬅️ Anterior"** y **"➡️ Siguiente"**
3. Cambia cuántos casos ver por página: **10, 25, 50, o 100**
4. Total de casos se muestra en tiempo real

---

## 📝 Editar Casos Existentes

### Paso a Paso

#### Paso 1: Seleccionar el Caso
1. Ve a la pestaña **"📝 Casos"**
2. En la tabla de la derecha, encuentra el caso que quieres editar
3. **Haz clic UNA VEZ** sobre la fila del caso
4. La fila se pondrá de color azul (significa que está seleccionada)

#### Paso 2: Ver los Datos en el Formulario
- Automáticamente, el formulario de la izquierda se llenará con los datos de ese caso
- **¡Magia!** Ya no tienes que copiar y pegar

#### Paso 3: Hacer los Cambios
- Haz clic en cualquier campo que quieras cambiar
- Borra lo que está y escribe lo nuevo
- O solo agrega más información

#### Paso 4: Guardar los Cambios
- Haz clic en **"💾 Guardar Caso"**
- O presiona `Ctrl + S`
- Verás: "✓ Caso actualizado correctamente"

✅ **¡Los cambios están guardados!**

### Actualizar la Etapa de un Caso

Este es un cambio muy común:

1. Selecciona el caso
2. Busca el campo **"Etapa"**
3. Haz clic en el menú desplegable
4. Selecciona la nueva etapa (ejemplo: de "Investigación" a "Juicio")
5. Guarda con `Ctrl + S`

---

## 📅 Gestión de Citaciones

### ¿Qué es una Citación?

Una citación es cuando le dices a alguien que debe venir a la corte en una fecha específica.

### Registrar una Citación

#### Paso 1: Seleccionar el Caso
- Haz clic en el caso en la tabla

#### Paso 2: Marcar que Hay Citación
- Busca la sección **"📅 Citación Judicial"**
- Verás un cuadrito (checkbox) que dice: **"Tiene citación vigente"**
- **Haz clic** en ese cuadrito para marcarlo
- Aparecerá una palomita ✓

#### Paso 3: Llenar los Datos de la Citación

**Fecha de Emisión:**
- ¿Cuándo se emitió la citación?
- Haz clic en el calendario y selecciona la fecha

**Fecha de Comparecencia:**
- ¿Cuándo debe presentarse la persona?
- Haz clic en el calendario y selecciona la fecha

**Estado de la Citación:**
- Haz clic en el menú desplegable
- Selecciona una opción:
  - **Pendiente**: Aún no ha pasado la fecha
  - **Compareció**: La persona sí vino
  - **No compareció**: La persona NO vino
  - **Cancelada**: Se canceló la citación

**Observaciones de Citación:**
- Escribe notas adicionales
- Ejemplo: `Primera citación. Notificado por correo.`

#### Paso 4: Guardar
- `Ctrl + S` o botón "💾 Guardar Caso"

### ¿Qué Pasa si No Compareció?

Si alguien no vino a su citación:
1. Cambia el estado a **"No compareció"**
2. Considera emitir una **Orden de Arresto** (ver siguiente sección)

---

## 🚔 Gestión de Órdenes de Arresto

### ¿Qué es una Orden de Arresto?

Es una orden judicial para que la policía capture a alguien.

### Registrar una Orden de Arresto

#### Paso 1: Seleccionar el Caso

#### Paso 2: Marcar que Hay Orden
- Busca la sección **"🚔 Orden de Arresto"**
- Haz clic en el checkbox: **"Tiene orden de arresto vigente"**

#### Paso 3: Llenar los Datos

**Fecha de Emisión:**
- ¿Cuándo se emitió la orden?

**Estado de la Orden:**
- **Pendiente de cumplimiento**: Aún no se ha capturado
- **Cumplida**: Ya se capturó a la persona
- **Cancelada**: Se canceló la orden
- **Revocada**: Se anuló la orden

**Origen de la Orden:**
- **Directa con denuncia**: Se emitió desde el inicio
- **Por no comparecencia a cita**: Porque no vino cuando fue citado
- **Orden judicial posterior**: Por decisión del juez después
- **Otro**: Otra razón

**Fecha de Cumplimiento** (solo si ya se capturó):
- La fecha en que se ejecutó la captura

**Observaciones de Orden:**
- Detalles adicionales

#### Paso 4: Guardar

### Ver Órdenes Pendientes

En el **Dashboard**:
- Verás una tarjeta roja que dice: **"Órdenes Pendientes: 5"**
- Ese número son las órdenes que aún no se han cumplido

---

## 🔄 Transferencias Entre Fiscales

### ¿Cuándo Transferir un Caso?

Cuando un caso pasa de un fiscal a otro por:
- Cambio de jurisdicción
- Declinación de competencia
- Redistribución de carga
- Conflicto de interés

### Registrar una Transferencia

#### Paso 1: Seleccionar el Caso

#### Paso 2: Cambiar el Fiscal Asignado
- En el campo **"Fiscal Asignado"**, cambia al nuevo fiscal
- Ejemplo: Cambias de `Lic. Pérez` a `Lic. Gómez`

#### Paso 3: Abrir el Historial
- Baja en el formulario hasta encontrar el botón:
  **"📋 Ver Historial de Transferencias"**
- Haz clic en él
- Se abrirá una nueva ventana

#### Paso 4: Agregar la Transferencia
- Haz clic en **"➕ Agregar Transferencia"**
- Llena el formulario que aparece:

**Fiscal Origen:**
- El fiscal que tenía el caso antes

**Fiscal Destino:**
- El fiscal que recibe el caso

**Departamento Origen y Destino:**
- Las jurisdicciones de cada uno

**Motivo:**
- Selecciona del menú:
  - Cambio de jurisdicción
  - Declinación de competencia
  - Redistribución de carga
  - Cambio de corte
  - Conflicto de interés
  - Otro

**Fecha:**
- Fecha de la transferencia

**Observaciones:**
- Detalles adicionales

#### Paso 5: Guardar la Transferencia
- Clic en **"💾 Guardar"**

#### Paso 6: Cerrar y Guardar el Caso
- Cierra la ventana del historial
- Guarda el caso principal con `Ctrl + S`

---

## 📎 Adjuntar Documentos

### Tipos de Archivos que Puedes Adjuntar

- **Documentos**: PDF, Word (.doc, .docx), TXT
- **Imágenes**: JPG, PNG, GIF
- **Hojas de cálculo**: Excel (.xls, .xlsx)
- **Otros**: ZIP, RAR, PPT

### Adjuntar un Documento

#### Paso 1: Seleccionar el Caso

#### Paso 2: Bajar al Final del Formulario
- Busca la sección **"📎 Documentos Adjuntos"**

#### Paso 3: Hacer Clic en "Adjuntar Documento"
- Haz clic en el botón verde **"📎 Adjuntar Documento"**

#### Paso 4: Seleccionar el Archivo
- Se abrirá una ventana de tu computadora
- Navega a donde está el archivo
- Haz clic en el archivo
- Haz clic en **"Abrir"**

#### Paso 5: Esperar Confirmación
- El archivo se copiará al sistema
- Verás un mensaje: "✓ Documento adjuntado"
- El archivo aparecerá en la lista

### Ver un Documento Adjuntado

1. En la lista de documentos del caso
2. Haz clic en el nombre del documento
3. Se abrirá automáticamente en tu programa predeterminado

### Eliminar un Documento

1. Selecciona el documento en la lista
2. Haz clic en **"🗑️ Eliminar Documento"**
3. Confirma que quieres eliminarlo

---

## 📊 Dashboard y Estadísticas

### ¿Qué Ves en el Dashboard?

#### Métricas Generales (Tarjetas de Colores)

**Total de Casos**
- Cuántos casos tienes en total en el sistema

**Casos Resueltos**
- Casos que ya están cerrados o archivados

**Casos Pendientes**
- Casos que aún están activos

**Casos en Juicio**
- Casos que están en etapa de juicio

**Tiempo Promedio**
- Cuántos días en promedio toma resolver un caso

**% Apelaciones**
- Qué porcentaje de casos van a apelación

**Órdenes Pendientes** (ROJO)
- Órdenes de arresto que no se han cumplido

**Órdenes Cumplidas** (VERDE)
- Órdenes que ya se ejecutaron

#### Estadísticas de Fiscales

**Botón "📊 Ver Detalles por Fiscal"**
- Haz clic aquí para ver métricas detalladas por cada fiscal
- Se abre una ventana con 5 pestañas:

**1. Casos Asignados**
- Quién tiene cuántos casos actualmente

**2. Casos Recibidos**
- Quién recibió cuántos casos inicialmente

**3. Casos Cerrados**
- Quién ha cerrado más casos

**4. Transferencias**
- Flujo de casos entre fiscales

**5. Resumen**
- Vista completa con todas las métricas

#### Próximos Eventos
- Lista de audiencias en los próximos 30 días
- Fechas importantes ordenadas cronológicamente

#### Actividad Reciente
- Últimos 10 casos que creaste o modificaste
- Para ver qué has trabajado recientemente

### Actualizar el Dashboard

- Haz clic en el botón **"🔄 Actualizar"**
- O presiona `F5` en tu teclado

---

## 🔔 Alertas del Sistema

### ¿Qué son las Alertas?

El sistema revisa automáticamente tus casos y te avisa si algo necesita atención.

### Tipos de Alertas

#### 🔴 Alertas de Prioridad Alta (Rojas)

**Casos Inactivos**
- Casos sin actualizaciones en más de 30 días
- Necesitan atención inmediata

**Órdenes de Arresto Antiguas**
- Órdenes pendientes por más de 30 días
- ¡Importante cumplirlas!

#### 🟡 Alertas de Prioridad Media (Amarillas)

**Juicios Prolongados**
- Juicios que llevan más de 90 días

**Pendientes Largos**
- Casos en investigación por más de 180 días

#### 🟢 Alertas de Prioridad Baja (Verdes)

**Sin Fecha de Denuncia**
- Casos que no tienen registrada la fecha de denuncia
- Importante completar información

### Revisar Alertas

1. Haz clic en la pestaña **"🔔 Alertas"**
2. Verás una lista de todos los casos con alertas
3. La alerta más importante está arriba
4. Cada alerta muestra:
   - Tipo de alerta
   - Nivel de prioridad (color)
   - Número de caso
   - Descripción del problema

### Resolver una Alerta

1. Haz clic en el caso en la lista de alertas
2. Te llevará automáticamente al caso en la pestaña "Casos"
3. Haz los cambios necesarios
4. Guarda el caso
5. La alerta desaparecerá automáticamente

---

## 📥 Importar Casos Masivamente

### ¿Cuándo Usar Esta Función?

Cuando tienes muchos casos en una hoja de Excel y quieres cargarlos todos al sistema de una vez.

### Preparar Tu Archivo Excel

#### Paso 1: Descargar la Plantilla

1. Ve a la pestaña **"📥 Importar"**
2. Haz clic en **"📥 Descargar Plantilla Excel"**
3. Se descargará un archivo llamado `plantilla_casos.xlsx`
4. Ábrelo en Excel o LibreOffice

#### Paso 2: Llenar la Plantilla

La plantilla tiene estas columnas (en este orden):

1. **numero_carpeta**: Número del caso
2. **victima**: Nombre de la víctima
3. **investigado**: Nombre del investigado
4. **fiscal_asignado**: Nombre del fiscal
5. **categoria**: Tipo de delito
6. **etapa**: Etapa procesal
7. **fecha_denuncia**: Formato YYYY-MM-DD (2024-12-25)
8. **fecha_audiencia**: Formato YYYY-MM-DD
9. **fecha_sentencia**: Formato YYYY-MM-DD
10. **descripcion**: Descripción del caso
11. **observaciones**: Observaciones adicionales
12. **archivado**: Escribe `1` si está archivado, `0` si no

**Ejemplo de una fila:**
```
2024-001 | María Pérez | Juan López | Lic. Ramírez | Robo | Investigación | 2024-01-15 | | | Robo de vehículo | Testigos disponibles | 0
```

#### Paso 3: Guardar el Archivo
- Guarda el archivo en tu computadora
- Recuerda dónde lo guardas

### Importar el Archivo

#### Paso 1: Seleccionar el Archivo
1. En la pestaña **"📥 Importar"**
2. Haz clic en **"📂 Seleccionar Archivo"**
3. Busca tu archivo Excel
4. Haz clic en **"Abrir"**

#### Paso 2: Vista Previa
- El sistema mostrará los primeros 10 casos
- Revisa que se vean bien
- Si algo está mal, cancela y corrige tu Excel

#### Paso 3: Importar
- Si todo se ve bien, haz clic en **"📥 Importar Datos"**
- Espera mientras el sistema carga los casos
- Puede tomar unos segundos o minutos dependiendo de cuántos casos sean

#### Paso 4: Ver Resultados
- El sistema te mostrará:
  - ✅ Casos importados correctamente
  - ❌ Casos con errores
- Si hubo errores, te dirá qué filas tienen problemas

### Consejos para Importar

✅ **DO (Hacer):**
- Usa la plantilla oficial
- Verifica las fechas (formato YYYY-MM-DD)
- Asegura que cada caso tenga número único
- Revisa las categorías y etapas (deben coincidir con las opciones del sistema)

❌ **DON'T (No Hacer):**
- No cambies los nombres de las columnas
- No dejes filas vacías en medio
- No uses formato de fecha diferente
- No importes el mismo archivo dos veces

---

## 📤 Exportar Reportes

### Exportar Casos Individuales

#### Exportar Un Solo Caso

1. Ve a la pestaña **"📤 Exportar"**
2. En la sección **"📄 Exportar Caso Individual"**:
3. Haz clic en el menú desplegable
4. Selecciona el caso que quieres exportar
5. Elige el formato:
   - **📄 Exportar a CSV**: Archivo de texto separado por comas
   - **📊 Exportar a Excel**: Archivo Excel con formato

El archivo se guardará en la carpeta `exports/` con el nombre del caso.

### Exportar Múltiples Casos

#### Exportar Todos los Casos

1. En la sección **"📦 Exportación Masiva"**
2. Haz clic en:
   - **📄 Exportar Todos a CSV**, o
   - **📊 Exportar Todos a Excel**

#### Exportar Solo Casos Filtrados

1. Primero, ve a la pestaña **"📝 Casos"**
2. Aplica los filtros que quieras (categoría, etapa, búsqueda)
3. Regresa a **"📤 Exportar"**
4. Haz clic en:
   - **📄 Exportar Filtrados a CSV**, o
   - **📊 Exportar Filtrados a Excel**

Solo se exportarán los casos que coincidan con tus filtros.

### Generar Gráficos Estadísticos

#### Paso 1: Seleccionar el Tipo de Gráfico

En la pestaña **"📤 Exportar"**, sección **"📊 Gráficos Estadísticos"**:

1. **Casos por Categoría**
   - Muestra cuántos casos hay de cada tipo de delito
   - Gráfico de barras horizontales

2. **Casos por Etapa**
   - Muestra cuántos casos hay en cada etapa
   - Gráfico de pastel (dona)

3. **Evolución Temporal**
   - Muestra cómo han aumentado/disminuido los casos por mes
   - Gráfico de líneas

4. **Casos por Fiscal**
   - Muestra cuántos casos tiene cada fiscal
   - Gráfico de barras

5. **Tasa de Resolución**
   - Compara casos activos vs archivados
   - Gráfico de barras comparativas

#### Paso 2: Generar el Gráfico
- Haz clic en el botón del gráfico que quieres
- Espera unos segundos
- El gráfico se abrirá automáticamente en una nueva ventana
- El archivo se guarda en `exports/` como imagen PNG

---

## 💡 Consejos y Trucos

### Atajos de Teclado

| Atajo | Función |
|-------|---------|
| `Ctrl + S` | Guardar caso actual |
| `Ctrl + N` | Limpiar formulario (nuevo caso) |
| `Ctrl + F` | Ir al cuadro de búsqueda |
| `Ctrl + E` | Ir a la pestaña de exportación |
| `F5` | Actualizar lista de casos |
| `Ctrl + →` | Página siguiente |
| `Ctrl + ←` | Página anterior |

### Mejores Prácticas

#### 📝 Al Crear Casos

1. **Siempre llena los campos obligatorios** (número, víctima, investigado, fiscal)
2. **Usa un formato consistente** para números de caso
3. **Registra la fecha de denuncia** inmediatamente
4. **Selecciona la categoría correcta** desde el inicio
5. **Escribe descripciones claras** y detalladas

#### 🔄 Al Actualizar Casos

1. **Actualiza la etapa** cuando cambie el estado del caso
2. **Registra las fechas** de audiencias y sentencias
3. **Agrega observaciones** con cada cambio importante
4. **Adjunta documentos** relevantes inmediatamente
5. **Guarda frecuentemente** con `Ctrl + S`

#### 📅 Gestión de Citaciones y Órdenes

1. **Registra citaciones** en cuanto se emitan
2. **Actualiza el estado** después de cada fecha de comparecencia
3. **Emite órdenes de arresto** rápidamente si no comparecen
4. **Marca como cumplidas** en cuanto se ejecuten

#### 🔔 Revisar Alertas

1. **Revisa alertas diariamente** (primera hora del día)
2. **Atiende las rojas primero** (prioridad alta)
3. **No ignores las verdes** (completa información faltante)
4. **Actualiza casos** para que desaparezcan alertas

#### 💾 Respaldos y Seguridad

1. **El sistema hace respaldos automáticos** al abrir y cerrar
2. **Haz respaldos manuales** semanalmente
3. **Copia la carpeta `backups/`** a un USB o nube
4. **Guarda la carpeta `documents/`** también
5. **No borres archivos** de la carpeta del programa

### Solución Rápida de Problemas

#### "No veo mis casos"
1. Verifica que no haya filtros activos (haz clic en "Limpiar Filtros")
2. Presiona `F5` para actualizar
3. Revisa que estés en la pestaña "Casos"

#### "No puedo guardar un caso"
1. Verifica que llenaste los campos obligatorios (tienen un asterisco *)
2. Verifica que el número de caso no esté duplicado
3. Cierra y abre el programa de nuevo

#### "No se adjuntan documentos"
1. Verifica que la carpeta `documents/` existe
2. Verifica que el archivo no esté abierto en otro programa
3. Intenta con un archivo más pequeño (menos de 10MB)

#### "Los gráficos no se generan"
1. Verifica que tengas casos en el sistema
2. Cierra ventanas abiertas de gráficos anteriores
3. Espera unos segundos más (puede tardar con muchos casos)

#### "La aplicación va lenta"
1. Cierra otras aplicaciones abiertas
2. Usa paginación de 25 casos por página
3. Aplica filtros para ver menos casos a la vez
4. Cierra la aplicación y ábrela de nuevo

---

## 🎯 Casos de Uso Paso a Paso

### Caso 1: Registrar Una Nueva Denuncia

**Situación:** Acaba de llegar una denuncia por robo.

1. Abre el programa
2. Ve a **"📝 Casos"**
3. Llena:
   - Número: `2024-045`
   - Víctima: `María García`
   - Investigado: `Desconocido`
   - Fiscal: `Lic. Ramírez`
   - Categoría: `Robo`
   - Etapa: `Denuncia Recibida`
   - Fecha denuncia: Hoy
   - Descripción: `Robo de celular iPhone 13 en transporte público`
4. Guarda con `Ctrl + S`
5. Adjunta la denuncia PDF (si la tienes)
6. ¡Listo!

### Caso 2: Programar Una Audiencia

**Situación:** Un caso en investigación tiene audiencia en 2 semanas.

1. Busca el caso en la tabla
2. Haz clic en él para seleccionarlo
3. Cambia la etapa a: `Audiencia Preliminar`
4. En "Fecha de Audiencia", selecciona la fecha (2 semanas adelante)
5. En observaciones agrega: `Audiencia programada, notificar a víctima`
6. Guarda con `Ctrl + S`
7. Ve al Dashboard para verificar que aparezca en "Próximos Eventos"

### Caso 3: Registrar No Comparecencia y Emitir Orden

**Situación:** El investigado no vino a su citación.

1. Selecciona el caso
2. En la sección de **Citación**:
   - Cambia estado a: `No compareció`
   - Agrega observación: `No se presentó a audiencia del 15/12/2024`
3. En la sección de **Orden de Arresto**:
   - Marca el checkbox "Tiene orden vigente"
   - Fecha de emisión: Hoy
   - Estado: `Pendiente de cumplimiento`
   - Origen: `Por no comparecencia a cita`
4. Guarda con `Ctrl + S`
5. Ve a **"🔔 Alertas"** para verificar que aparezca como orden pendiente

### Caso 4: Transferir Caso a Otro Fiscal

**Situación:** El caso cambia de jurisdicción.

1. Selecciona el caso
2. Cambia "Fiscal Asignado" de `Lic. Pérez` a `Lic. Gómez`
3. Cambia "Departamento" de `Corte 1` a `Corte 2`
4. Haz clic en **"📋 Ver Historial de Transferencias"**
5. Haz clic en **"➕ Agregar Transferencia"**
6. Llena:
   - Fiscal origen: `Lic. Pérez`
   - Fiscal destino: `Lic. Gómez`
   - Departamento origen: `Corte 1`
   - Departamento destino: `Corte 2`
   - Motivo: `Cambio de jurisdicción`
   - Fecha: Hoy
   - Observaciones: `Por competencia territorial`
7. Guarda la transferencia
8. Cierra la ventana de historial
9. Guarda el caso con `Ctrl + S`

### Caso 5: Cerrar un Caso

**Situación:** Se dictó sentencia y el caso se cierra.

1. Selecciona el caso
2. Cambia la etapa a: `Sentencia`
3. En "Fecha de Sentencia" pon la fecha de hoy
4. En "Fiscal de Cierre" pon el nombre del fiscal actual
5. Marca el checkbox **"Archivado"** (si no lo ves, baja en el formulario)
6. En observaciones agrega: `Sentencia: 5 años prisión. Caso cerrado.`
7. Guarda con `Ctrl + S`
8. El caso ahora aparecerá en estadísticas como "Resuelto"

### Caso 6: Exportar Reporte Mensual

**Situación:** Necesitas un reporte de casos de diciembre.

1. Ve a **"📝 Casos"**
2. En la búsqueda escribe: `2024-12` (para ver casos de diciembre)
3. Ve a **"📤 Exportar"**
4. Haz clic en **"📊 Exportar Filtrados a Excel"**
5. El archivo se guardará en `exports/`
6. Ábrelo en Excel
7. Genera gráficos haciendo clic en:
   - "Casos por Categoría"
   - "Casos por Etapa"
   - "Evolución Temporal"
8. Incluye estos gráficos en tu reporte

---

## 📞 Necesitas Más Ayuda?

### Recursos Adicionales

- **GUIA_USUARIO.md**: Guía técnica completa
- **README.md**: Información de instalación
- Carpeta `exports/`: Tus reportes exportados
- Carpeta `backups/`: Respaldos automáticos
- Carpeta `documents/`: Documentos adjuntos

### Contacto de Soporte

Si tienes problemas que no puedes resolver:
1. Revisa esta guía de nuevo
2. Verifica la sección "Solución de Problemas"
3. Contacta al administrador del sistema

---

## ✨ Conclusión

¡Felicidades! Ahora sabes cómo usar el Sistema de Gestión de Casos Judiciales.

**Recuerda:**
- 💾 Guarda frecuentemente (`Ctrl + S`)
- 🔔 Revisa alertas diariamente
- 📊 Genera reportes mensuales
- 💾 Haz respaldos semanales
- 📝 Mantén información actualizada

**Este sistema te ayudará a:**
- ✅ Organizar todos tus casos
- ✅ No olvidar fechas importantes
- ✅ Generar reportes rápidamente
- ✅ Trabajar más eficientemente

---

**Sistema de Gestión de Casos v3.0**  
*Manual Completo - Para Todos los Niveles*

Última actualización: Diciembre 2025

---

## 📚 Índice Rápido de Emergencia

¿Necesitas hacer algo URGENTE? Salta directamente a:

- **Crear caso nuevo**: [Página Crear Tu Primer Caso](#crear-tu-primer-caso)
- **Buscar un caso**: [Página Buscar y Ver Casos](#buscar-y-ver-casos)
- **Registrar citación**: [Página Gestión de Citaciones](#gestión-de-citaciones)
- **Emitir orden**: [Página Gestión de Órdenes](#gestión-de-órdenes-de-arresto)
- **Exportar reporte**: [Página Exportar Reportes](#exportar-reportes)
- **Problema técnico**: [Página Solución de Problemas](#💡-consejos-y-trucos)

---

¡Mucho éxito con tu trabajo! 🎉
