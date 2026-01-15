#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Gestión de Casos Judiciales
Copyright © 2026 Rafael Llibre
Todos los derechos reservados.

Aplicación principal para la gestión de carpetas judiciales
desarrollada con PyQt6 y SQLite.
"""

from views.main_window import MainWindow
from utils.backup_manager import BackupManager
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Create automatic backup on startup (skip if first run)
    try:
        backup_mgr = BackupManager()
        backup_path = backup_mgr.auto_backup_on_startup()
        if backup_path:
            print(f"✓ Respaldo automático creado: {backup_path}")
        else:
            print("✓ Primera ejecución - no hay respaldos previos")
    except Exception as e:
        print(f"⚠ No se pudo crear respaldo automático: {e}")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())