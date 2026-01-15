#!/usr/bin/env python3
"""
Script para generar casos de prueba con diversas características
para probar el rendimiento y funcionalidad del sistema
"""

import sys
import random
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database.db import Database

class GeneradorCasosPrueba:
    def __init__(self):
        self.db = Database()
        
        # Listas de datos variados para generar casos realistas
        self.categorias = [
            'Delitos contra la propiedad',
            'Delitos contra la persona',
            'Delitos sexuales',
            'Corrupción',
            'Narcotráfico',
            'Robo simple',
            'Daños a la propiedad',
            'Golpes y herida',
            'Amenazas',
            'Usurpación simple',
            'Violencia intrafamiliar',
            'Estafa',
            'Accidente de tránsito',
            'Penal laboral',
            'Pensión alimentaria',
            'Otros'
        ]
        
        self.etapas = [
            'Investigación',
            'Formalizado',
            'Acusación presentada',
            'En juicio',
            'Archivo provisional',
            'Archivo definitivo',
            'Sobreseimiento',
            'Sentencia'
        ]
        
        self.estados = [
            'Investigación',
            'Formalizado',
            'Acusación presentada',
            'En juicio',
            'Archivo provisional',
            'Archivo definitivo',
            'Sobreseimiento',
            'Sentencia'
        ]
        
        self.resultados = ['', 'Condena', 'Absolución', 'Conciliación', 'Acuerdo', 'Archivo', 'Sobreseimiento']
        
        self.estados_orden = ['', 'Pendiente de cumplimiento', 'Cumplida', 'Cancelada', 'Revocada']
        
        self.nombres = [
            'Juan Carlos', 'María Elena', 'Pedro Antonio', 'Ana Lucía', 'José Miguel',
            'Carmen Rosa', 'Luis Fernando', 'Patricia', 'Roberto Carlos', 'Sofía',
            'Diego Alejandro', 'Gabriela', 'Carlos Alberto', 'Valentina', 'Fernando',
            'Isabella', 'Manuel', 'Camila', 'Ricardo', 'Daniela', 'Andrés',
            'Paula', 'Francisco', 'Laura', 'Javier', 'Natalia', 'Sebastián',
            'Andrea', 'Miguel Ángel', 'Carolina', 'Rafael', 'Mónica', 'Arturo',
            'Verónica', 'Oscar', 'Lorena', 'Héctor', 'Silvia', 'Raúl', 'Teresa'
        ]
        
        self.apellidos = [
            'García', 'Rodríguez', 'Martínez', 'Hernández', 'López', 'González',
            'Pérez', 'Sánchez', 'Ramírez', 'Torres', 'Flores', 'Rivera', 'Gómez',
            'Díaz', 'Cruz', 'Morales', 'Reyes', 'Gutiérrez', 'Ortiz', 'Chavez',
            'Ruiz', 'Mendoza', 'Silva', 'Castro', 'Vargas', 'Jiménez', 'Romero',
            'Álvarez', 'Medina', 'Aguilar', 'Guerrero', 'León', 'Vega', 'Ramos'
        ]
        
        self.fiscales = [
            'Fiscal Dra. María González',
            'Fiscal Dr. Carlos Ramírez',
            'Fiscal Dra. Ana Torres',
            'Fiscal Dr. Luis Martínez',
            'Fiscal Dra. Carmen Flores',
            'Fiscal Dr. Roberto Sánchez',
            'Fiscal Dra. Patricia López',
            'Fiscal Dr. Fernando García'
        ]
    
    def generar_nombre_completo(self):
        """Genera un nombre completo aleatorio"""
        nombre = random.choice(self.nombres)
        apellido1 = random.choice(self.apellidos)
        apellido2 = random.choice(self.apellidos)
        return f"{nombre} {apellido1} {apellido2}"
    
    def generar_fecha_aleatoria(self, inicio_dias, fin_dias):
        """Genera una fecha aleatoria dentro de un rango de días desde hoy"""
        # Asegurar que inicio_dias <= fin_dias
        if inicio_dias > fin_dias:
            inicio_dias, fin_dias = fin_dias, inicio_dias
        # Evitar rangos vacíos
        if inicio_dias == fin_dias:
            dias = inicio_dias
        else:
            dias = random.randint(inicio_dias, fin_dias)
        return (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
    
    def generar_caso(self, numero):
        """Genera un caso con datos aleatorios pero coherentes"""
        # Número de carpeta
        anio = random.choice([2023, 2024, 2025])
        num_carpeta = f"MP-{anio}-{str(numero).zfill(5)}"
        
        # Datos básicos
        categoria = random.choice(self.categorias)
        etapa = random.choice(self.etapas)
        victima = self.generar_nombre_completo()
        investigado = self.generar_nombre_completo()
        fiscal = random.choice(self.fiscales)
        
        # Fechas progresivas (más antiguas primero)
        fecha_denuncia = self.generar_fecha_aleatoria(500, 10) if random.random() > 0.1 else ''
        
        # Fecha de formalización posterior a denuncia
        fecha_formalizacion = ''
        if fecha_denuncia and etapa not in ['Investigación'] and random.random() > 0.3:
            dias_despues = random.randint(30, 180)
            fecha_base = datetime.strptime(fecha_denuncia, '%Y-%m-%d')
            fecha_formalizacion = (fecha_base + timedelta(days=dias_despues)).strftime('%Y-%m-%d')
        
        # Fecha de acusación
        fecha_acusacion = ''
        if fecha_formalizacion and etapa in ['Acusación presentada', 'En juicio', 'Sentencia'] and random.random() > 0.4:
            dias_despues = random.randint(30, 120)
            fecha_base = datetime.strptime(fecha_formalizacion, '%Y-%m-%d')
            fecha_acusacion = (fecha_base + timedelta(days=dias_despues)).strftime('%Y-%m-%d')
        
        # Fecha de sentencia
        fecha_sentencia = ''
        if etapa == 'Sentencia' and random.random() > 0.5:
            fecha_sentencia = self.generar_fecha_aleatoria(30, 5)
        
        # Fecha de archivo
        fecha_archivo = ''
        if etapa in ['Archivo provisional', 'Archivo definitivo', 'Sobreseimiento'] and random.random() > 0.4:
            fecha_archivo = self.generar_fecha_aleatoria(60, 5)
        
        # Monto de reparación
        montos = [0, 5000, 10000, 15000, 20000, 25000, 50000, 100000]
        monto = random.choice(montos)
        
        # Estado y resultado
        estado = random.choice(self.estados)
        resultado = random.choice(self.resultados)
        
        # Apelación
        apelacion = 1 if random.random() > 0.85 else 0
        
        # Orden de arresto
        tiene_orden = 1 if random.random() > 0.85 else 0
        fecha_emision_orden = ''
        estado_orden = ''
        fecha_cumplimiento_orden = ''
        observaciones_orden = ''
        
        if tiene_orden:
            # Fecha de emisión de la orden
            if fecha_denuncia:
                dias_despues = random.randint(10, 200)
                fecha_base = datetime.strptime(fecha_denuncia, '%Y-%m-%d')
                fecha_emision_orden = (fecha_base + timedelta(days=dias_despues)).strftime('%Y-%m-%d')
            else:
                fecha_emision_orden = self.generar_fecha_aleatoria(300, 10)
            
            # Estado de la orden
            estado_orden = random.choice(['Pendiente de cumplimiento', 'Cumplida', 'Cancelada', 'Revocada'])
            
            # Si está cumplida, agregar fecha
            if estado_orden == 'Cumplida' and fecha_emision_orden:
                dias_despues = random.randint(5, 90)
                fecha_base = datetime.strptime(fecha_emision_orden, '%Y-%m-%d')
                fecha_cumplimiento_orden = (fecha_base + timedelta(days=dias_despues)).strftime('%Y-%m-%d')
            
            # Observaciones
            observaciones_lista = [
                'Orden emitida por el Juez de Garantías',
                'Coordinación con la policía para la captura',
                'Investigado en paradero desconocido',
                'Se solicita apoyo internacional',
                'Captura realizada en operativo policial',
                'Orden cancelada por acuerdo reparatorio',
                'Investigado se presentó voluntariamente'
            ]
            if random.random() > 0.5:
                observaciones_orden = random.choice(observaciones_lista)
        
        return (
            num_carpeta, categoria, etapa, victima, investigado,
            fecha_denuncia, fecha_formalizacion, fecha_acusacion, fecha_sentencia, fecha_archivo,
            monto, estado, resultado, apelacion, fiscal,
            tiene_orden, fecha_emision_orden, estado_orden, fecha_cumplimiento_orden, observaciones_orden
        )
    
    def generar_casos_masivos(self, cantidad=50):
        """Genera múltiples casos de prueba"""
        print(f"🔄 Generando {cantidad} casos de prueba...")
        print("=" * 60)
        
        casos_creados = 0
        casos_con_orden = 0
        ordenes_pendientes = 0
        
        for i in range(1, cantidad + 1):
            try:
                caso = self.generar_caso(i)
                self.db.insert_case(caso)
                casos_creados += 1
                
                # Estadísticas
                if caso[15] == 1:  # tiene_orden_arresto
                    casos_con_orden += 1
                    if caso[17] == 'Pendiente de cumplimiento':  # estado_orden
                        ordenes_pendientes += 1
                
                # Mostrar progreso cada 10 casos
                if i % 10 == 0:
                    print(f"✓ Creados {i} casos...")
                    
            except Exception as e:
                print(f"❌ Error al crear caso {i}: {e}")
        
        print("=" * 60)
        print(f"✅ Generación completada!")
        print(f"📊 Resumen:")
        print(f"   • Total de casos creados: {casos_creados}")
        print(f"   • Casos con orden de arresto: {casos_con_orden}")
        print(f"   • Órdenes pendientes: {ordenes_pendientes}")
        print(f"   • Distribución por etapas:")
        
        # Contar casos por etapa
        etapas_count = {}
        for etapa in self.etapas:
            conn = self.db.get_connection()
            cursor = conn.execute("SELECT COUNT(*) FROM cases WHERE etapa_procesal = ?", (etapa,))
            count = cursor.fetchone()[0]
            if count > 0:
                etapas_count[etapa] = count
                print(f"     - {etapa}: {count} casos")
        
        print("\n🎉 ¡Casos de prueba generados exitosamente!")
        print("💡 Ahora puedes abrir la aplicación y ver cómo se comporta con esta carga de datos.")

def main():
    print("=" * 60)
    print("🚀 GENERADOR DE CASOS DE PRUEBA")
    print("   Sistema de Gestión de Casos v2.5")
    print("=" * 60)
    print()
    
    # Solicitar cantidad de casos
    try:
        cantidad_input = input("¿Cuántos casos deseas generar? (por defecto 50): ").strip()
        cantidad = int(cantidad_input) if cantidad_input else 50
        
        if cantidad < 1:
            print("❌ La cantidad debe ser mayor a 0")
            return
        
        if cantidad > 500:
            confirmar = input(f"⚠️  Vas a generar {cantidad} casos. ¿Continuar? (s/n): ").strip().lower()
            if confirmar != 's':
                print("Operación cancelada.")
                return
        
    except ValueError:
        print("❌ Por favor ingresa un número válido")
        return
    
    print()
    
    # Generar casos
    generador = GeneradorCasosPrueba()
    generador.generar_casos_masivos(cantidad)
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
