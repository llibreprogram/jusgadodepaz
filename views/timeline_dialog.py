from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, 
    QListWidgetItem, QWidget, QDateEdit, QComboBox, QTextEdit, 
    QPushButton, QMessageBox, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor

class TimelineDialog(QDialog):
    def __init__(self, parent, controller, case_id):
        super().__init__(parent)
        self.controller = controller
        self.case_id = case_id
        
        self.setWindowTitle("Cronología del Caso")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                color: #e2e8f0;
            }
            QLabel {
                color: #e2e8f0;
            }
            QLineEdit, QTextEdit, QDateEdit, QComboBox {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 6px;
                color: #e2e8f0;
                padding: 8px;
            }
            QListWidget {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(16)
        self.layout.setContentsMargins(24, 24, 24, 24)
        
        self.setup_ui()
        self.load_events()
        
    def setup_ui(self):
        # Header
        header = QLabel("Historia del Caso")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #60a5fa;")
        self.layout.addWidget(header)
        
        # Splitter: Left (Timeline List), Right (Add Event Form)
        content_layout = QHBoxLayout()
        
        # --- Timeline List (Left) ---
        list_container = QWidget()
        list_layout = QVBoxLayout(list_container)
        list_layout.setContentsMargins(0, 0, 0, 0)
        
        self.event_list = QListWidget()
        self.event_list.setSpacing(4)
        list_layout.addWidget(self.event_list)
        
        content_layout.addWidget(list_container, stretch=2)
        
        # --- Add Event Form (Right) ---
        form_container = QFrame()
        form_container.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 12px;
                border: 1px solid #334155;
            }
            QLabel {
                color: #94a3b8;
                font-weight: 600;
                font-size: 13px;
            }
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(16, 16, 16, 16)
        
        form_title = QLabel("Agregar Nota / Evento")
        form_title.setStyleSheet("color: #e2e8f0; font-size: 16px; font-weight: bold; border: none;")
        form_layout.addWidget(form_title)
        
        # Date
        form_layout.addWidget(QLabel("Fecha:"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        form_layout.addWidget(self.date_edit)
        
        # Type
        form_layout.addWidget(QLabel("Tipo de Evento:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Nota General",
            "Audiencia",
            "Recepción de Documentos",
            "Diligencia",
            "Llamada / Contacto",
            "Cambio de Estado",
            "Otro"
        ])
        form_layout.addWidget(self.type_combo)
        
        # Description
        form_layout.addWidget(QLabel("Descripción:"))
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText("Escriba los detalles aquí...")
        form_layout.addWidget(self.desc_edit)
        
        # Button
        add_btn = QPushButton("➕ Agregar Evento")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        add_btn.clicked.connect(self.add_event)
        form_layout.addWidget(add_btn)
        
        form_layout.addStretch()
        
        content_layout.addWidget(form_container, stretch=1)
        self.layout.addLayout(content_layout)
        
    def load_events(self):
        self.event_list.clear()
        events = self.controller.get_case_events(self.case_id)
        
        if not events:
            item = QListWidgetItem("No hay eventos registrados.")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.event_list.addItem(item)
            return
            
        for event in events:
            # event is a Row object (id, case_id, type, desc, date, created_at)
            # Row access by index: 0=id, 1=case_id, 2=type, 3=desc, 4=date
            
            event_type = event[2]
            desc = event[3]
            date_str = event[4]
            
            # Create widget for item
            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(12, 8, 12, 8)
            layout.setSpacing(4)
            
            # Header line: Date | Type
            header_layout = QHBoxLayout()
            date_lbl = QLabel(f"📅 {date_str}")
            date_lbl.setStyleSheet("color: #94a3b8; font-size: 13px; font-weight: 600;")
            
            type_lbl = QLabel(event_type)
            type_lbl.setStyleSheet("""
                background-color: #334155; 
                color: #f1f5f9; 
                padding: 2px 8px; 
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            """)
            
            header_layout.addWidget(date_lbl)
            header_layout.addWidget(type_lbl)
            header_layout.addStretch()
            
            layout.addLayout(header_layout)
            
            # Description
            desc_lbl = QLabel(desc)
            desc_lbl.setWordWrap(True)
            desc_lbl.setStyleSheet("color: #e2e8f0; font-size: 14px; margin-top: 4px;")
            layout.addWidget(desc_lbl)
            
            # Create List Item
            item = QListWidgetItem(self.event_list)
            item.setSizeHint(widget.sizeHint())
            self.event_list.addItem(item)
            self.event_list.setItemWidget(item, widget)
            
    def add_event(self):
        desc = self.desc_edit.toPlainText().strip()
        if not desc:
            QMessageBox.warning(self, "Error", "La descripción no puede estar vacía.")
            return
            
        event_type = self.type_combo.currentText()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        
        try:
            self.controller.add_event(self.case_id, event_type, desc, date)
            self.desc_edit.clear()
            self.load_events()
            # QMessageBox.information(self, "Éxito", "Evento agregado correctamente.") # Optional, maybe too noisy
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar evento: {str(e)}")
