#!/usr/bin/env python3
"""
Test script to verify new statistics features
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from models.case import Case
from views.main_window import MainWindow
from utils.export_service import ExportService
from database.db import Database

def test_area_classification():
    """Test area classification from categories"""
    print("\n=== Testing Area Classification ===")
    
    # Create MainWindow instance to access classification method
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    
    test_cases = [
        ("Pensión alimentaria - Apertura", "Pensión Alimentaria"),
        ("Tránsito - Acuerdo", "Tránsito"),
        ("Violación de ley", "Otros Casos"),
        ("Medida de protección", "Otros Casos"),
        ("Pensión Cierre", "Pensión Alimentaria"),
    ]
    
    for category, expected_area in test_cases:
        area = window.get_area_from_category(category)
        status = "✓" if area == expected_area else "✗"
        print(f"{status} {category} -> {area} (expected: {expected_area})")
    
    print("\n=== Testing Statistics Grouping ===")
    
    # Create test cases
    test_case_list = [
        Case(
            numero_carpeta=1,
            categoria="Pensión alimentaria - Apertura",
            victima="Juan Pérez",
            investigado="María García",
            fecha_denuncia="2024-01-01",
            monto_pension=5000.0
        ),
        Case(
            numero_carpeta=2,
            categoria="Tránsito - Acuerdo",
            victima="Pedro López",
            investigado="Ana Martínez",
            fecha_denuncia="2024-01-02",
        ),
        Case(
            numero_carpeta=3,
            categoria="Violación de ley",
            victima="Carlos Ruiz",
            investigado="Sofía Hernández",
            fecha_denuncia="2024-01-03",
        ),
        Case(
            numero_carpeta=4,
            categoria="Pensión Condena",
            victima="Luis Ramírez",
            investigado="Elena Torres",
            fecha_denuncia="2024-01-04",
            monto_pension=3000.0
        ),
    ]
    
    # Get statistics by area
    stats = window.get_statistics_by_area(test_case_list)
    
    print(f"\nPensión Alimentaria: {stats['pension']['count']} casos")
    print(f"  - Total mensual: ${stats['pension']['total_pension']:,.2f}")
    print(f"Tránsito: {stats['transito']['count']} casos")
    print(f"Otros Casos: {stats['otros']['count']} casos")
    
    print("\n=== Testing Resolution Statistics ===")
    resolution_stats = window.get_resolution_statistics(test_case_list)
    for res_type, count in resolution_stats.items():
        if count > 0:
            print(f"{res_type}: {count}")
    
    print("\n✅ All tests completed!")
    return 0

def test_export_service():
    """Test export service with sample data"""
    print("\n=== Testing Export Service ===")
    
    export_service = ExportService()
    
    # Create test cases
    test_cases = [
        Case(
            numero_carpeta=1,
            categoria="Pensión alimentaria - Apertura",
            victima="Juan Pérez",
            investigado="María García",
            fecha_denuncia="2024-01-01",
            monto_pension=5000.0
        ),
        Case(
            numero_carpeta=2,
            categoria="Tránsito - Acuerdo",
            victima="Pedro López",
            investigado="Ana Martínez",
            fecha_denuncia="2024-01-02",
        ),
    ]
    
    try:
        filepath = export_service.export_complete_statistics(test_cases, "test_estadisticas.xlsx")
        print(f"✓ Export successful: {filepath}")
        return 0
    except Exception as e:
        print(f"✗ Export failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    try:
        result1 = test_area_classification()
        result2 = test_export_service()
        sys.exit(result1 + result2)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
