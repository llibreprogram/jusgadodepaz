#!/usr/bin/env python3
"""
Script to check pension cases in the database
"""
import sqlite3

def check_pension_cases():
    conn = sqlite3.connect('cases.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("REVISIÓN DE CASOS DE PENSIÓN ALIMENTARIA")
    print("=" * 80)
    print()
    
    # Get all cases with their categories
    cursor.execute("SELECT id, numero_carpeta, categoria FROM cases ORDER BY id")
    all_cases = cursor.fetchall()
    
    print(f"Total de casos en la base de datos: {len(all_cases)}")
    print()
    
    # Count pension cases using the same logic as the application
    pension_cases = []
    transito_cases = []
    otros_cases = []
    
    for case_id, numero_carpeta, categoria in all_cases:
        if categoria:
            cat_lower = categoria.lower()
            if 'pensión' in cat_lower or 'pension' in cat_lower:
                pension_cases.append((case_id, numero_carpeta, categoria))
            elif 'tránsito' in cat_lower or 'transito' in cat_lower:
                transito_cases.append((case_id, numero_carpeta, categoria))
            else:
                otros_cases.append((case_id, numero_carpeta, categoria))
        else:
            otros_cases.append((case_id, numero_carpeta, categoria or 'Sin categoría'))
    
    print(f"Casos de Pensión Alimentaria: {len(pension_cases)}")
    print(f"Casos de Tránsito: {len(transito_cases)}")
    print(f"Otros Casos: {len(otros_cases)}")
    print()
    
    # Show pension cases
    if pension_cases:
        print("-" * 80)
        print("CASOS DE PENSIÓN ALIMENTARIA ENCONTRADOS:")
        print("-" * 80)
        for case_id, numero_carpeta, categoria in pension_cases[:20]:  # Show first 20
            print(f"  ID: {case_id:3d} | Carpeta: {numero_carpeta:15s} | Categoría: {categoria}")
    else:
        print("⚠️  No se encontraron casos de pensión alimentaria en la base de datos")
    
    print()
    
    # Show all unique categories
    cursor.execute("SELECT DISTINCT categoria FROM cases WHERE categoria IS NOT NULL ORDER BY categoria")
    categories = cursor.fetchall()
    
    print("-" * 80)
    print("TODAS LAS CATEGORÍAS EN LA BASE DE DATOS:")
    print("-" * 80)
    for (cat,) in categories:
        count = sum(1 for _, _, c in all_cases if c == cat)
        # Check if it would be classified as pension
        cat_lower = cat.lower() if cat else ''
        tipo = "PENSIÓN" if ('pensión' in cat_lower or 'pension' in cat_lower) else \
               "TRÁNSITO" if ('tránsito' in cat_lower or 'transito' in cat_lower) else \
               "OTRO"
        print(f"  [{tipo:8s}] {cat:40s} : {count} casos")
    
    conn.close()
    print()
    print("=" * 80)

if __name__ == '__main__':
    check_pension_cases()
