#!/usr/bin/env python3
"""
Script to debug search and filter issues
"""
import sqlite3

def test_search_logic():
    conn = sqlite3.connect('cases.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("PRUEBA DE LÓGICA DE BÚSQUEDA Y FILTROS")
    print("=" * 80)
    print()
    
    # Get all cases
    cursor.execute("SELECT id, numero_carpeta, categoria, victima, investigado FROM cases ORDER BY id LIMIT 30")
    cases = cursor.fetchall()
    
    print(f"Primeros 30 casos en la base de datos:")
    print("-" * 80)
    for case_id, numero_carpeta, categoria, victima, investigado in cases:
        print(f"ID: {case_id:3d} | Carpeta: {numero_carpeta:15s} | Cat: {categoria:30s}")
    
    print()
    print("-" * 80)
    print("PRUEBA DE FILTRO: Pensión alimentaria (todas)")
    print("-" * 80)
    
    pension_count = 0
    for case_id, numero_carpeta, categoria, victima, investigado in cases:
        if categoria:
            case_cat = categoria.lower()
            if 'pensión' in case_cat or 'pension' in case_cat:
                pension_count += 1
                print(f"✓ ID {case_id}: {numero_carpeta} - {categoria}")
    
    print(f"\nTotal encontrados en primeros 30: {pension_count}")
    
    print()
    print("-" * 80)
    print("PRUEBA DE FILTRO: Tránsito (todas)")
    print("-" * 80)
    
    transito_count = 0
    for case_id, numero_carpeta, categoria, victima, investigado in cases:
        if categoria:
            case_cat = categoria.lower()
            if 'tránsito' in case_cat or 'transito' in case_cat:
                transito_count += 1
                print(f"✓ ID {case_id}: {numero_carpeta} - {categoria}")
    
    print(f"\nTotal encontrados en primeros 30: {transito_count}")
    
    print()
    print("-" * 80)
    print("PRUEBA DE BÚSQUEDA: Texto 'MP-2024'")
    print("-" * 80)
    
    search_text = 'mp-2024'
    match_count = 0
    for case_id, numero_carpeta, categoria, victima, investigado in cases:
        # Simulate text search across all fields
        all_text = f"{numero_carpeta} {categoria} {victima} {investigado}".lower()
        if search_text in all_text:
            match_count += 1
            print(f"✓ ID {case_id}: {numero_carpeta} - {victima} vs {investigado}")
    
    print(f"\nTotal encontrados en primeros 30: {match_count}")
    
    print()
    print("-" * 80)
    print("VERIFICACIÓN DE COLUMNAS EN LA TABLA")
    print("-" * 80)
    
    cursor.execute("PRAGMA table_info(cases)")
    columns = cursor.fetchall()
    print(f"Total de columnas: {len(columns)}")
    for col in columns:
        print(f"  {col[0]:2d}. {col[1]:30s} {col[2]:10s}")
    
    conn.close()
    print()
    print("=" * 80)

if __name__ == '__main__':
    test_search_logic()
