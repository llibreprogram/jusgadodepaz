#!/usr/bin/env python3
"""
Simple test for export service without GUI
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from models.case import Case
from utils.export_service import ExportService

def test_export_complete_statistics():
    """Test the new export_complete_statistics method"""
    print("\n=== Testing Export Complete Statistics ===\n")
    
    # Create test cases
    test_cases = [
        Case(
            numero_carpeta=1,
            categoria="Pensión alimentaria - Apertura",
            etapa_procesal="Investigación",
            victima="Juan Pérez",
            investigado="María García",
            fecha_denuncia="2024-01-01",
            fecha_formalizacion="2024-01-05",
            fecha_acusacion="",
            fecha_sentencia="",
            fecha_archivo="",
            estado_actual="Activo",
            resultado="Pendiente",
            apelacion=0,
            fiscal_asignado="Dr. Fiscal 1",
            monto_pension=5000.0
        ),
        Case(
            numero_carpeta=2,
            categoria="Pensión Condena",
            etapa_procesal="Sentencia",
            victima="Luis Ramírez",
            investigado="Elena Torres",
            fecha_denuncia="2024-01-02",
            fecha_formalizacion="2024-01-07",
            fecha_acusacion="2024-01-15",
            fecha_sentencia="2024-02-01",
            fecha_archivo="",
            estado_actual="Cerrado",
            resultado="Condena",
            apelacion=0,
            fiscal_asignado="Dr. Fiscal 2",
            monto_pension=3000.0
        ),
        Case(
            numero_carpeta=3,
            categoria="Tránsito - Acuerdo",
            etapa_procesal="Conciliación",
            victima="Pedro López",
            investigado="Ana Martínez",
            fecha_denuncia="2024-01-03",
            fecha_formalizacion="2024-01-08",
            fecha_acusacion="",
            fecha_sentencia="",
            fecha_archivo="2024-01-20",
            estado_actual="Cerrado",
            resultado="Acuerdo",
            apelacion=0,
            fiscal_asignado="Dr. Fiscal 1",
        ),
        Case(
            numero_carpeta=4,
            categoria="Tránsito - Daños",
            etapa_procesal="Investigación",
            victima="Carlos Silva",
            investigado="Marta Jiménez",
            fecha_denuncia="2024-01-04",
            fecha_formalizacion="",
            fecha_acusacion="",
            fecha_sentencia="",
            fecha_archivo="",
            estado_actual="Activo",
            resultado="Pendiente",
            apelacion=0,
            fiscal_asignado="Dr. Fiscal 3",
        ),
        Case(
            numero_carpeta=5,
            categoria="Violación de ley",
            etapa_procesal="Juicio",
            victima="Roberto Díaz",
            investigado="Laura Morales",
            fecha_denuncia="2024-01-05",
            fecha_formalizacion="2024-01-10",
            fecha_acusacion="2024-01-18",
            fecha_sentencia="",
            fecha_archivo="",
            estado_actual="Activo",
            resultado="Pendiente",
            apelacion=0,
            fiscal_asignado="Dr. Fiscal 2",
        ),
        Case(
            numero_carpeta=6,
            categoria="Medida de protección",
            etapa_procesal="Audiencia",
            victima="Carmen Vega",
            investigado="Jorge Castro",
            fecha_denuncia="2024-01-06",
            fecha_formalizacion="2024-01-09",
            fecha_acusacion="",
            fecha_sentencia="",
            fecha_archivo="",
            estado_actual="Activo",
            resultado="Pendiente",
            apelacion=0,
            fiscal_asignado="Dr. Fiscal 1",
        ),
    ]
    
    print(f"Created {len(test_cases)} test cases:")
    print(f"  - 2 Pensión Alimentaria (total: $8,000/mes)")
    print(f"  - 2 Tránsito")
    print(f"  - 2 Otros Casos")
    
    # Test export
    export_service = ExportService()
    
    try:
        filepath = export_service.export_complete_statistics(
            test_cases, 
            "test_estadisticas_completas.xlsx"
        )
        print(f"\n✅ Export successful!")
        print(f"   File: {filepath}")
        print(f"\nExpected sheets in Excel file:")
        print(f"  1. Resumen General")
        print(f"  2. Pensión Alimentaria")
        print(f"  3. Estadísticas Pensión")
        print(f"  4. Tránsito")
        print(f"  5. Estadísticas Tránsito")
        print(f"  6. Otros Casos")
        print(f"  7. Estadísticas Otros")
        print(f"  8. Tipos de Resolución")
        return 0
    except Exception as e:
        print(f"\n✗ Export failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(test_export_complete_statistics())
