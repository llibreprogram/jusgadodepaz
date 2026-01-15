from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QPushButton, QFrame, QTabWidget, QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

class FiscalStatsDialog(QDialog):
    """Dialog showing detailed fiscal statistics"""
    
    def __init__(self, fiscal_stats, parent=None):
        super().__init__(parent)
        self.fiscal_stats = fiscal_stats
        
        self.setWindowTitle('📊 Estadísticas Detalladas por Fiscal')
        self.setMinimumSize(900, 600)
        self.setStyleSheet('''
            QDialog {
                background-color: #0f172a;
            }
            QLabel {
                color: #e2e8f0;
            }
            QTableWidget {
                background-color: #1e293b;
                alternate-background-color: #0f172a;
                color: #e2e8f0;
                border: 1px solid #334155;
                border-radius: 8px;
                gridline-color: #334155;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #334155;
                color: #e2e8f0;
            }
            QTableWidget::item:alternate {
                background-color: #0f172a;
                color: #e2e8f0;
            }
            QTableWidget::item:selected {
                background-color: #3b82f6;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #1e293b;
                color: #60a5fa;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #3b82f6;
                font-weight: 600;
            }
            QPushButton {
                background-color: #64748b;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 600;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #475569;
            }
            QTabWidget::pane {
                border: 1px solid #334155;
                border-radius: 8px;
                background-color: #1e293b;
            }
            QTabBar::tab {
                background-color: #1e293b;
                color: #94a3b8;
                padding: 10px 20px;
                border: 1px solid #334155;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #3b82f6;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #334155;
            }
        ''')
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(16)
        
        # Title
        title = QLabel('📊 Estadísticas Detalladas por Fiscal')
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title.setStyleSheet('color: #60a5fa; margin-bottom: 10px;')
        layout.addWidget(title)
        
        # Create tabs
        tabs = QTabWidget()
        
        # Tab 1: Casos Asignados
        asignados_tab = self.create_table_tab(
            self.fiscal_stats.get('asignados', {}),
            'Casos Actualmente Asignados',
            '#3b82f6'
        )
        tabs.addTab(asignados_tab, '📋 Asignados')
        
        # Tab 2: Casos Recibidos
        recibidos_tab = self.create_table_tab(
            self.fiscal_stats.get('recibidos', {}),
            'Casos Recibidos Inicialmente',
            '#10b981'
        )
        tabs.addTab(recibidos_tab, '📥 Recibidos')
        
        # Tab 3: Casos Cerrados
        cerrados_tab = self.create_table_tab(
            self.fiscal_stats.get('cerrados', {}),
            'Casos Cerrados por Fiscal',
            '#6366f1'
        )
        tabs.addTab(cerrados_tab, '✅ Cerrados')
        
        # Tab 4: Declinaciones
        declinaciones_tab = self.create_declinaciones_tab()
        tabs.addTab(declinaciones_tab, '↪️ Transferencias')
        
        # Tab 5: Resumen
        resumen_tab = self.create_resumen_tab()
        tabs.addTab(resumen_tab, '📊 Resumen')
        
        layout.addWidget(tabs)
        
        # Close button
        close_btn = QPushButton('Cerrar')
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def create_table_tab(self, data_dict, title, color):
        """Create a tab with a table showing fiscal statistics"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(12)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        title_label.setStyleSheet(f'color: {color};')
        layout.addWidget(title_label)
        
        # Summary
        total = sum(data_dict.values())
        summary = QLabel(f'Total: {total} casos | Fiscales: {len(data_dict)}')
        summary.setStyleSheet('color: #94a3b8; font-size: 13px;')
        layout.addWidget(summary)
        
        # Table
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['Fiscal', 'Casos', '% del Total'])
        table.setRowCount(len(data_dict))
        
        # Sort by cases descending
        sorted_items = sorted(data_dict.items(), key=lambda x: x[1], reverse=True)
        
        for row, (fiscal, count) in enumerate(sorted_items):
            # Fiscal name
            fiscal_item = QTableWidgetItem(fiscal)
            table.setItem(row, 0, fiscal_item)
            
            # Count
            count_item = QTableWidgetItem(str(count))
            count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            count_item.setForeground(QColor(color))
            count_item.setFont(QFont('Arial', 12, QFont.Weight.Bold))
            table.setItem(row, 1, count_item)
            
            # Percentage
            pct = (count / total * 100) if total > 0 else 0
            pct_item = QTableWidgetItem(f'{pct:.1f}%')
            pct_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row, 2, pct_item)
        
        # Configure table
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        table.setColumnWidth(1, 100)
        table.setColumnWidth(2, 100)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        
        layout.addWidget(table)
        widget.setLayout(layout)
        return widget
    
    def create_declinaciones_tab(self):
        """Create tab showing transfer/declination statistics"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(12)
        
        # Title
        title = QLabel('Transferencias y Declinaciones')
        title.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        title.setStyleSheet('color: #f59e0b;')
        layout.addWidget(title)
        
        # Two tables side by side
        tables_layout = QHBoxLayout()
        
        # Declinaciones salientes
        salida_container = QWidget()
        salida_layout = QVBoxLayout()
        salida_layout.setContentsMargins(0, 0, 0, 0)
        
        salida_label = QLabel('↗️ Casos Declinados')
        salida_label.setStyleSheet('color: #ef4444; font-weight: 600;')
        salida_layout.addWidget(salida_label)
        
        declinaciones_salida = self.fiscal_stats.get('declinaciones_salida', {})
        total_salida = sum(declinaciones_salida.values())
        
        salida_summary = QLabel(f'Total: {total_salida}')
        salida_summary.setStyleSheet('color: #94a3b8; font-size: 12px;')
        salida_layout.addWidget(salida_summary)
        
        salida_table = self.create_simple_table(declinaciones_salida, '#ef4444')
        salida_layout.addWidget(salida_table)
        salida_container.setLayout(salida_layout)
        
        # Declinaciones entrantes
        entrada_container = QWidget()
        entrada_layout = QVBoxLayout()
        entrada_layout.setContentsMargins(0, 0, 0, 0)
        
        entrada_label = QLabel('↙️ Casos Recibidos por Declinación')
        entrada_label.setStyleSheet('color: #10b981; font-weight: 600;')
        entrada_layout.addWidget(entrada_label)
        
        declinaciones_entrada = self.fiscal_stats.get('declinaciones_entrada', {})
        total_entrada = sum(declinaciones_entrada.values())
        
        entrada_summary = QLabel(f'Total: {total_entrada}')
        entrada_summary.setStyleSheet('color: #94a3b8; font-size: 12px;')
        entrada_layout.addWidget(entrada_summary)
        
        entrada_table = self.create_simple_table(declinaciones_entrada, '#10b981')
        entrada_layout.addWidget(entrada_table)
        entrada_container.setLayout(entrada_layout)
        
        tables_layout.addWidget(salida_container)
        tables_layout.addWidget(entrada_container)
        
        layout.addLayout(tables_layout)
        widget.setLayout(layout)
        return widget
    
    def create_simple_table(self, data_dict, color):
        """Create a simple 2-column table"""
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(['Fiscal', 'Cantidad'])
        table.setRowCount(len(data_dict))
        
        sorted_items = sorted(data_dict.items(), key=lambda x: x[1], reverse=True)
        
        for row, (fiscal, count) in enumerate(sorted_items):
            fiscal_item = QTableWidgetItem(fiscal)
            table.setItem(row, 0, fiscal_item)
            
            count_item = QTableWidgetItem(str(count))
            count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            count_item.setForeground(QColor(color))
            count_item.setFont(QFont('Arial', 11, QFont.Weight.Bold))
            table.setItem(row, 1, count_item)
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        table.setColumnWidth(1, 100)
        table.verticalHeader().setVisible(False)
        
        return table
    
    def create_resumen_tab(self):
        """Create summary tab with overall statistics"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        title = QLabel('📊 Resumen General')
        title.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        title.setStyleSheet('color: #60a5fa;')
        layout.addWidget(title)
        
        # Get all fiscals
        asignados = self.fiscal_stats.get('asignados', {})
        recibidos = self.fiscal_stats.get('recibidos', {})
        cerrados = self.fiscal_stats.get('cerrados', {})
        declinaciones_salida = self.fiscal_stats.get('declinaciones_salida', {})
        declinaciones_entrada = self.fiscal_stats.get('declinaciones_entrada', {})
        
        all_fiscals = set(
            list(asignados.keys()) + 
            list(recibidos.keys()) + 
            list(cerrados.keys()) +
            list(declinaciones_salida.keys()) +
            list(declinaciones_entrada.keys())
        )
        
        # Create comprehensive table
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            'Fiscal', 
            'Recibidos', 
            'Asignados', 
            'Cerrados',
            'Declinados',
            'Recibidos por Decl.'
        ])
        table.setRowCount(len(all_fiscals))
        
        sorted_fiscals = sorted(all_fiscals)
        
        for row, fiscal in enumerate(sorted_fiscals):
            # Fiscal name
            table.setItem(row, 0, QTableWidgetItem(fiscal))
            
            # Stats
            rec = recibidos.get(fiscal, 0)
            asig = asignados.get(fiscal, 0)
            cerr = cerrados.get(fiscal, 0)
            decl_sal = declinaciones_salida.get(fiscal, 0)
            decl_ent = declinaciones_entrada.get(fiscal, 0)
            
            for col, value, color in [
                (1, rec, '#10b981'),
                (2, asig, '#3b82f6'),
                (3, cerr, '#6366f1'),
                (4, decl_sal, '#ef4444'),
                (5, decl_ent, '#f59e0b')
            ]:
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if value > 0:
                    item.setForeground(QColor(color))
                    item.setFont(QFont('Arial', 11, QFont.Weight.Bold))
                table.setItem(row, col, item)
        
        # Configure table
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for col in range(1, 6):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
            table.setColumnWidth(col, 100)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        
        layout.addWidget(table)
        
        # Summary stats
        summary_frame = QFrame()
        summary_frame.setStyleSheet('background: #1e293b; border-radius: 8px; padding: 16px;')
        summary_layout = QHBoxLayout()
        
        totals = [
            ('Total Fiscales', len(all_fiscals), '#60a5fa'),
            ('Total Recibidos', sum(recibidos.values()), '#10b981'),
            ('Total Asignados', sum(asignados.values()), '#3b82f6'),
            ('Total Cerrados', sum(cerrados.values()), '#6366f1'),
            ('Total Transferencias', sum(declinaciones_salida.values()), '#f59e0b'),
        ]
        
        for label, value, color in totals:
            stat_label = QLabel(f'<b>{label}:</b> <span style="color: {color};">{value}</span>')
            stat_label.setStyleSheet('color: #e2e8f0; font-size: 13px;')
            summary_layout.addWidget(stat_label)
        
        summary_frame.setLayout(summary_layout)
        layout.addWidget(summary_frame)
        
        widget.setLayout(layout)
        return widget
