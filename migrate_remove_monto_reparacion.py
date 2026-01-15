#!/usr/bin/env python3
"""
Migration script to remove monto_reparacion column from database
This script will:
1. Create a backup of the current database
2. Create a new table with the correct schema (without monto_reparacion)
3. Copy data from old table to new table, skipping the monto_reparacion column
4. Drop old table and rename new table
"""

import sqlite3
import shutil
from datetime import datetime
import os

def migrate_database():
    db_path = 'cases.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file not found: cases.db")
        return False
    
    # Create backup
    backup_path = f'cases_backup_before_migration_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
    shutil.copy2(db_path, backup_path)
    print(f"✓ Backup created: {backup_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if monto_reparacion column exists
        cursor.execute("PRAGMA table_info(cases)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'monto_reparacion' not in column_names:
            print("✓ Column monto_reparacion does not exist. No migration needed.")
            conn.close()
            return True
        
        print(f"Found {len(column_names)} columns in current schema")
        print("Starting migration...")
        
        # Create new table with correct schema (without monto_reparacion)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cases_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_carpeta TEXT UNIQUE NOT NULL,
                categoria TEXT,
                etapa_procesal TEXT,
                victima TEXT,
                investigado TEXT,
                fecha_denuncia TEXT,
                fecha_formalizacion TEXT,
                fecha_acusacion TEXT,
                fecha_sentencia TEXT,
                fecha_archivo TEXT,
                estado_actual TEXT,
                resultado TEXT,
                apelacion INTEGER,
                fiscal_asignado TEXT,
                tiene_citacion INTEGER DEFAULT 0,
                fecha_emision_citacion TEXT,
                fecha_comparecencia TEXT,
                estado_citacion TEXT,
                observaciones_citacion TEXT,
                tiene_orden_arresto INTEGER DEFAULT 0,
                fecha_emision_orden TEXT,
                estado_orden TEXT,
                fecha_cumplimiento_orden TEXT,
                observaciones_orden TEXT,
                origen_orden_arresto TEXT,
                fiscal_inicial TEXT,
                departamento_actual TEXT,
                fiscal_cierre TEXT,
                monto_pension REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Copy data from old table to new table, excluding monto_reparacion
        cursor.execute('''
            INSERT INTO cases_new (
                id, numero_carpeta, categoria, etapa_procesal, victima, investigado,
                fecha_denuncia, fecha_formalizacion, fecha_acusacion, fecha_sentencia,
                fecha_archivo, estado_actual, resultado, apelacion,
                fiscal_asignado, tiene_citacion, fecha_emision_citacion, fecha_comparecencia,
                estado_citacion, observaciones_citacion, tiene_orden_arresto, fecha_emision_orden,
                estado_orden, fecha_cumplimiento_orden, observaciones_orden, origen_orden_arresto,
                fiscal_inicial, departamento_actual, fiscal_cierre, monto_pension,
                created_at, updated_at
            )
            SELECT 
                id, numero_carpeta, categoria, etapa_procesal, victima, investigado,
                fecha_denuncia, fecha_formalizacion, fecha_acusacion, fecha_sentencia,
                fecha_archivo, estado_actual, resultado, apelacion,
                fiscal_asignado, tiene_citacion, fecha_emision_citacion, fecha_comparecencia,
                estado_citacion, observaciones_citacion, tiene_orden_arresto, fecha_emision_orden,
                estado_orden, fecha_cumplimiento_orden, observaciones_orden, origen_orden_arresto,
                fiscal_inicial, departamento_actual, fiscal_cierre, monto_pension,
                created_at, updated_at
            FROM cases
        ''')
        
        rows_copied = cursor.rowcount
        print(f"✓ Copied {rows_copied} rows to new table")
        
        # Drop old table
        cursor.execute('DROP TABLE cases')
        print("✓ Dropped old table")
        
        # Rename new table
        cursor.execute('ALTER TABLE cases_new RENAME TO cases')
        print("✓ Renamed new table to 'cases'")
        
        # Also migrate historial_fiscales if it exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='historial_fiscales'")
        if cursor.fetchone():
            print("✓ Fiscal history table exists and will remain unchanged")
        
        conn.commit()
        print("\n✅ Migration completed successfully!")
        print(f"   - Removed column: monto_reparacion")
        print(f"   - Migrated {rows_copied} cases")
        print(f"   - Backup saved: {backup_path}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        conn.rollback()
        print(f"   Database remains unchanged")
        print(f"   Backup available: {backup_path}")
        return False
        
    finally:
        conn.close()

if __name__ == '__main__':
    print("=" * 60)
    print("DATABASE MIGRATION: Remove monto_reparacion column")
    print("=" * 60)
    print()
    
    success = migrate_database()
    
    if success:
        print("\n" + "=" * 60)
        print("You can now start the application with: python main.py")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("Migration failed. Please check the error above.")
        print("=" * 60)
