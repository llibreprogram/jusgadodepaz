from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QScrollArea, QWidget, QFrame, QLineEdit,
                             QComboBox, QTextEdit, QMessageBox, QDateEdit)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from datetime import datetime

class FiscalHistoryDialog(QDialog):
    """Dialog to view and manage fiscal transfer history"""
    
    def __init__(self, caso_id, fiscal_controller, parent=None):
        super().__init__(parent)
        self.caso_id = caso_id
        self.fiscal_controller = fiscal_controller
        self.parent_window = parent
        
        self.setWindowTitle('📜 Historial de Transferencias Fiscales')
        self.setMinimumSize(800, 600)
        self.setStyleSheet('''
            QDialog {
                background-color: #0f172a;
            }
            QLabel {
                color: #e2e8f0;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QLineEdit, QComboBox, QTextEdit, QDateEdit {
                background-color: #1e293b;
                color: #e2e8f0;
                border: 1px solid #334155;
                border-radius: 4px;
                padding: 8px;
                min-height: 32px;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QDateEdit:focus {
                border: 1px solid #3b82f6;
            }
        ''')
        
        self.init_ui()
        self.load_history()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel('📜 Historial de Transferencias')
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title.setStyleSheet('color: #60a5fa; margin-bottom: 10px;')
        layout.addWidget(title)
        
        # Scroll area for history entries
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet('''
            QScrollArea {
                border: none;
                background-color: #0c1220;
            }
            QScrollBar:vertical {
                background-color: #1e293b;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #3b82f6;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #2563eb;
            }
        ''')
        
        self.history_container = QWidget()
        self.history_layout = QVBoxLayout()
        self.history_layout.setSpacing(12)
        self.history_container.setLayout(self.history_layout)
        scroll.setWidget(self.history_container)
        
        layout.addWidget(scroll, stretch=1)
        
        # Button to add new transfer
        add_btn = QPushButton('+ Registrar Nueva Transferencia')
        add_btn.setMinimumHeight(44)
        add_btn.clicked.connect(self.show_add_transfer_form)
        layout.addWidget(add_btn)
        
        # Close button
        close_btn = QPushButton('Cerrar')
        close_btn.setStyleSheet('''
            QPushButton {
                background-color: #64748b;
            }
            QPushButton:hover {
                background-color: #475569;
            }
        ''')
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def load_history(self):
        """Load and display fiscal history"""
        # Clear existing entries
        while self.history_layout.count():
            child = self.history_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Get history from database
        history = self.fiscal_controller.get_case_history(self.caso_id)
        
        if not history:
            no_data = QLabel('📋 No hay transferencias registradas para este caso.')
            no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data.setStyleSheet('color: #94a3b8; font-size: 14px; padding: 40px;')
            self.history_layout.addWidget(no_data)
        else:
            for entry in history:
                card = self.create_history_card(entry)
                self.history_layout.addWidget(card)
        
        self.history_layout.addStretch()
    
    def create_history_card(self, entry):
        """Create a card for a history entry"""
        card = QFrame()
        card.setStyleSheet(f'''
            QFrame {{
                background-color: #1e293b;
                border-left: 4px solid {entry.get_action_color()};
                border-radius: 6px;
                padding: 15px;
            }}
        ''')
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Action header
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(entry.get_action_icon())
        icon_label.setStyleSheet('font-size: 24px;')
        header_layout.addWidget(icon_label)
        
        action_label = QLabel(entry.accion)
        action_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        action_label.setStyleSheet(f'color: {entry.get_action_color()};')
        header_layout.addWidget(action_label)
        
        header_layout.addStretch()
        
        date_label = QLabel(entry.fecha_movimiento)
        date_label.setStyleSheet('color: #94a3b8; font-size: 12px;')
        header_layout.addWidget(date_label)
        
        layout.addLayout(header_layout)
        
        # Fiscal information
        fiscal_info = QLabel(f'<b>Fiscal:</b> {entry.fiscal_nombre}')
        fiscal_info.setStyleSheet('color: #e2e8f0; margin-top: 5px;')
        layout.addWidget(fiscal_info)
        
        if entry.departamento:
            dept_info = QLabel(f'<b>Departamento:</b> {entry.departamento}')
            dept_info.setStyleSheet('color: #cbd5e1;')
            layout.addWidget(dept_info)
        
        # Destination (for transfers/declinations)
        if entry.fiscal_destino:
            dest_info = QLabel(f'<b>Hacia:</b> {entry.fiscal_destino}')
            dest_info.setStyleSheet('color: #e2e8f0; margin-top: 8px;')
            layout.addWidget(dest_info)
            
            if entry.departamento_destino:
                dest_dept = QLabel(f'<b>Departamento destino:</b> {entry.departamento_destino}')
                dest_dept.setStyleSheet('color: #cbd5e1;')
                layout.addWidget(dest_dept)
        
        # Reason
        if entry.motivo:
            motivo_label = QLabel(f'<b>Motivo:</b> {entry.motivo}')
            motivo_label.setStyleSheet('color: #f59e0b; margin-top: 8px;')
            motivo_label.setWordWrap(True)
            layout.addWidget(motivo_label)
        
        # Observations
        if entry.observaciones:
            obs_label = QLabel(f'<b>Observaciones:</b><br>{entry.observaciones}')
            obs_label.setStyleSheet('color: #94a3b8; font-size: 12px; margin-top: 5px;')
            obs_label.setWordWrap(True)
            layout.addWidget(obs_label)
        
        card.setLayout(layout)
        return card
    
    def show_add_transfer_form(self):
        """Show form to add new transfer"""
        dialog = AddTransferDialog(self.caso_id, self.fiscal_controller, self.parent_window, self)
        if dialog.exec():
            self.load_history()


class AddTransferDialog(QDialog):
    """Dialog to add a new fiscal transfer"""
    
    def __init__(self, caso_id, fiscal_controller, main_window, parent=None):
        super().__init__(parent)
        self.caso_id = caso_id
        self.fiscal_controller = fiscal_controller
        self.main_window = main_window
        
        self.setWindowTitle('➕ Nueva Transferencia')
        self.setMinimumSize(600, 500)
        self.setStyleSheet('''
            QDialog {
                background-color: #0f172a;
            }
            QLabel {
                color: #e2e8f0;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-weight: 600;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QLineEdit, QComboBox, QTextEdit, QDateEdit {
                background-color: #1e293b;
                color: #e2e8f0;
                border: 1px solid #334155;
                border-radius: 4px;
                padding: 8px;
                min-height: 32px;
            }
        ''')
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel('➕ Registrar Nueva Transferencia')
        title.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        title.setStyleSheet('color: #60a5fa; margin-bottom: 10px;')
        layout.addWidget(title)
        
        # Fiscal origen
        layout.addWidget(QLabel('Fiscal origen:'))
        self.fiscal_origen = QLineEdit()
        self.fiscal_origen.setPlaceholderText('Nombre del fiscal que transfiere')
        layout.addWidget(self.fiscal_origen)
        
        # Departamento origen
        layout.addWidget(QLabel('Departamento origen:'))
        self.dept_origen = QComboBox()
        self.dept_origen.addItems([
            '', 'San Salvador', 'Santa Ana', 'San Miguel', 'La Libertad', 
            'Sonsonate', 'Usulután', 'La Paz', 'Chalatenango', 'Ahuachapán',
            'Cuscatlán', 'La Unión', 'Morazán', 'Cabañas', 'San Vicente'
        ])
        layout.addWidget(self.dept_origen)
        
        # Fiscal destino
        layout.addWidget(QLabel('Fiscal destino:'))
        self.fiscal_destino = QLineEdit()
        self.fiscal_destino.setPlaceholderText('Nombre del fiscal que recibe')
        layout.addWidget(self.fiscal_destino)
        
        # Departamento destino
        layout.addWidget(QLabel('Departamento destino:'))
        self.dept_destino = QComboBox()
        self.dept_destino.addItems([
            '', 'San Salvador', 'Santa Ana', 'San Miguel', 'La Libertad', 
            'Sonsonate', 'Usulután', 'La Paz', 'Chalatenango', 'Ahuachapán',
            'Cuscatlán', 'La Unión', 'Morazán', 'Cabañas', 'San Vicente'
        ])
        layout.addWidget(self.dept_destino)
        
        # Motivo
        layout.addWidget(QLabel('Motivo de transferencia:'))
        self.motivo = QComboBox()
        self.motivo.setEditable(True)
        self.motivo.addItems([
            '',
            'Cambio de jurisdicción',
            'Declinación de competencia',
            'Redistribución de carga',
            'Cambio de corte',
            'Conflicto de interés',
            'Otro'
        ])
        layout.addWidget(self.motivo)
        
        # Observaciones
        layout.addWidget(QLabel('Observaciones:'))
        self.observaciones = QTextEdit()
        self.observaciones.setPlaceholderText('Detalles adicionales...')
        self.observaciones.setMaximumHeight(100)
        layout.addWidget(self.observaciones)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton('💾 Guardar Transferencia')
        save_btn.clicked.connect(self.save_transfer)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton('Cancelar')
        cancel_btn.setStyleSheet('''
            QPushButton {
                background-color: #64748b;
            }
            QPushButton:hover {
                background-color: #475569;
            }
        ''')
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def save_transfer(self):
        """Save the transfer to database"""
        fiscal_origen = self.fiscal_origen.text().strip()
        fiscal_destino = self.fiscal_destino.text().strip()
        motivo = self.motivo.currentText().strip()
        
        if not fiscal_origen or not fiscal_destino or not motivo:
            QMessageBox.warning(
                self,
                'Campos incompletos',
                'Por favor complete los campos: Fiscal origen, Fiscal destino y Motivo.'
            )
            return
        
        try:
            # Register the transfer
            self.fiscal_controller.record_transfer(
                caso_id=self.caso_id,
                fiscal_origen=fiscal_origen,
                departamento_origen=self.dept_origen.currentText(),
                fiscal_destino=fiscal_destino,
                departamento_destino=self.dept_destino.currentText(),
                motivo=motivo,
                observaciones=self.observaciones.toPlainText().strip() or None
            )
            
            # Update main window fiscal fields
            if self.main_window:
                self.main_window.fiscal_asignado.setText(fiscal_destino)
                self.main_window.departamento_actual.setCurrentText(self.dept_destino.currentText())
            
            QMessageBox.information(
                self,
                'Éxito',
                'Transferencia registrada exitosamente.'
            )
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                'Error',
                f'Error al registrar transferencia:\n{str(e)}'
            )
