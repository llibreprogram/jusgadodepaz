import sys
import math
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QDateEdit, QComboBox, QCheckBox, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog,
    QFormLayout, QFrame, QSizePolicy, QSpacerItem, QCalendarWidget, QCompleter,
    QProgressBar, QScrollArea
)
from PyQt6.QtCore import QDate, Qt, QEvent
from PyQt6.QtGui import QKeySequence, QShortcut
from controllers.case_controller import CaseController
from utils.graph_utils import GraphUtils
from utils.export_service import ExportService
from utils.notification_manager import NotificationManager
from utils.import_service import ImportService
from services.document_service import DocumentService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = CaseController()
        self.graph_utils = GraphUtils()
        self.export_service = ExportService()
        self.notification_manager = NotificationManager()
        self.import_service = ImportService(self.controller)
        self.document_service = DocumentService()
        self.filtered_cases = []
        self.current_page = 1
        self.items_per_page = 50
        self.total_pages = 1
        self.categories = [
            # PENSIÓN ALIMENTARIA
            'Pensión alimentaria',
            'Acuerdo homologado de pensión',
            'Desistimiento de pensión',
            'Conciliación de pensión',
            'No acuerdo de pensión',
            'Condena de pensión',
            # TRÁNSITO
            'Tránsito - Daño a propiedad',
            'Desistimiento de tránsito',
            'Conciliación de tránsito',
            'Condena de tránsito',
            'Apertura a juicio de tránsito',
            'Auto no a lugar - Tránsito',
            # OTROS CASOS
            'Violación a la propiedad',
            'Riña penal',
            'Penal laboral',
            'Medidas de protección',
            'Daño a la propiedad',
            'Conciliación de riña',
            'Conciliación de daño a propiedad',
            'No acuerdo de daño a propiedad',
            'Archivo',
            'Otros'
        ]
        self.categories_without_otros = [c for c in self.categories if c != 'Otros']
        self.current_edit_id = None
        self.filter_etapas = [
            'Todas',
            'Investigación',
            'Formalizado',
            'Acusación presentada',
            'En juicio',
            'Archivo provisional',
            'Archivo definitivo',
            'Sobreseimiento',
            'Sentencia'
        ]
        self.init_ui()
        self.setup_shortcuts()
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts for common actions"""
        # Ctrl+S: Save case
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self.save_case)
        # Ctrl+N: Clear form (new case)
        QShortcut(QKeySequence("Ctrl+N"), self).activated.connect(self.clear_form)
        # Ctrl+F: Focus search
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(
            lambda: self.search_input.setFocus() if hasattr(self, 'search_input') else None
        )
        # Ctrl+E: Switch to export tab
        QShortcut(QKeySequence("Ctrl+E"), self).activated.connect(
            lambda: self.tabs.setCurrentIndex(3)
        )
        # F5: Refresh cases
        QShortcut(QKeySequence("F5"), self).activated.connect(
            lambda: self.load_cases() if hasattr(self, 'load_cases') else None
        )
        # Page navigation
        QShortcut(QKeySequence("Ctrl+Right"), self).activated.connect(
            lambda: self.next_page() if hasattr(self, 'next_page') else None
        )
        QShortcut(QKeySequence("Ctrl+Left"), self).activated.connect(
            lambda: self.previous_page() if hasattr(self, 'previous_page') else None
        )

    def get_area_from_category(self, category):
        """Determina el área según la categoría"""
        if not category:
            return 'Otros Casos'
        
        category_lower = category.lower()
        pension_keywords = ['pensión', 'pension']
        transito_keywords = ['tránsito', 'transito']
        
        if any(k in category_lower for k in pension_keywords):
            return 'Pensión Alimentaria'
        elif any(k in category_lower for k in transito_keywords):
            return 'Tránsito'
        else:
            return 'Otros Casos'
    
    def get_statistics_by_area(self):
        """Genera estadísticas agrupadas por área"""
        cases = self.controller.get_all_cases()
        
        areas = {
            'Pensión Alimentaria': [],
            'Tránsito': [],
            'Otros Casos': []
        }
        
        for case in cases:
            area = self.get_area_from_category(case.categoria)
            areas[area].append(case)
        
        return areas
    
    def get_resolution_statistics(self):
        """Obtiene estadísticas de tipos de resolución"""
        cases = self.controller.get_all_cases()
        
        resolution_types = {
            'Conciliaciones': 0,
            'Condenas': 0,
            'Acuerdos': 0,
            'No acuerdos': 0,
            'Desistimientos': 0,
            'Archivos': 0,
            'En proceso': 0
        }
        
        for case in cases:
            cat_lower = case.categoria.lower() if case.categoria else ''
            if 'conciliación' in cat_lower or 'conciliacion' in cat_lower:
                resolution_types['Conciliaciones'] += 1
            elif 'condena' in cat_lower:
                resolution_types['Condenas'] += 1
            elif 'acuerdo' in cat_lower:
                resolution_types['Acuerdos'] += 1
            elif 'no acuerdo' in cat_lower:
                resolution_types['No acuerdos'] += 1
            elif 'desistimiento' in cat_lower:
                resolution_types['Desistimientos'] += 1
            elif 'archivo' in cat_lower:
                resolution_types['Archivos'] += 1
            else:
                resolution_types['En proceso'] += 1
        
        return resolution_types

    def init_ui(self):
        self.setWindowTitle('Sistema de Gestión de Casos - Ministerio Público')
        
        # Get screen dimensions and set window to 90% of screen size
        screen = QApplication.primaryScreen().geometry()
        screen_width = screen.width()
        screen_height = screen.height()
        
        window_width = int(screen_width * 0.90)
        window_height = int(screen_height * 0.90)
        
        self.resize(window_width, window_height)
        self.setMinimumSize(1000, 600)
        
        # Center window on screen
        self.move(
            (screen_width - window_width) // 2,
            (screen_height - window_height) // 2
        )
        
        self.apply_theme()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(16, 16, 16, 16)
        container_layout.setSpacing(12)

        container_layout.addWidget(self.build_header())
        container_layout.addWidget(self.tabs)

        container.setLayout(container_layout)
        self.setCentralWidget(container)

        self.create_register_tab()
        self.create_view_tab()
        self.create_stats_tab()
        self.create_export_tab()
        self.create_import_tab()
        self.create_alerts_tab()
        self.setup_autocompleters()

    def setup_autocompleters(self):
        """Configure autocompleters for text fields"""
        try:
            # Get unique values from database
            fiscales = self.controller.get_unique_fiscales()
            victimas = self.controller.get_unique_victimas()
            investigados = self.controller.get_unique_investigados()
            
            # Fiscal autocompleter
            fiscal_completer = QCompleter(fiscales)
            fiscal_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            fiscal_completer.setFilterMode(Qt.MatchFlag.MatchContains)
            self.fiscal_asignado.setCompleter(fiscal_completer)
            
            # Victima autocompleter
            victima_completer = QCompleter(victimas)
            victima_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            victima_completer.setFilterMode(Qt.MatchFlag.MatchContains)
            self.victima.setCompleter(victima_completer)
            
            # Investigado autocompleter
            investigado_completer = QCompleter(investigados)
            investigado_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            investigado_completer.setFilterMode(Qt.MatchFlag.MatchContains)
            self.investigado.setCompleter(investigado_completer)
            
        except Exception as e:
            print(f"Error configurando autocompletado: {e}")
    
    def get_card_style(self, style_type='default'):
        """Get consistent card styling"""
        styles = {
            'default': """
                #card { 
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #1f2937, stop:1 #111827);
                    border: 1px solid #334155; 
                    border-radius: 14px;
                }
            """,
            'elevated': """
                #card { 
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #1a2332, stop:1 #0f1621);
                    border: 2px solid #1e293b; 
                    border-radius: 16px;
                }
            """,
            'highlight': """
                #card { 
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #1e3a4f, stop:1 #0f1621);
                    border: 2px solid rgba(34, 197, 94, 0.3); 
                    border-radius: 16px;
                }
            """
        }
        return styles.get(style_type, styles['default'])

    def apply_theme(self):
        accent = '#3b82f6'
        accent_hover = '#60a5fa'
        soft = '#1f2937'
        surface = '#0b1220'
        border = '#1e293b'
        text = '#e5e7eb'
        self.setStyleSheet(f"""
            QMainWindow {{ 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0a0f1a, stop:1 {surface});
                color: {text}; 
            }}
            QLabel {{ 
                color: {text}; 
                font-size: 14px;
                font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', Arial, sans-serif;
            }}
            QLineEdit, QComboBox, QDateEdit, QTextEdit {{
                background: {soft};
                color: {text};
                font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', Arial, sans-serif;
                border: 1px solid {border};
                border-radius: 6px;
                padding: 8px 10px;
            }}
            QComboBox QAbstractItemView {{
                background: {soft};
                color: {text};
                selection-background-color: {accent};
                selection-color: #0b1220;
                border: 2px solid {border};
                border-radius: 8px;
                padding: 8px;
            }}
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {{
                border: 2px solid {accent};
                background: #253244;
            }}
            QLineEdit:hover, QComboBox:hover, QDateEdit:hover {{
                border: 2px solid #334155;
                background: #232e3e;
            }}
            QTabWidget::pane {{ 
                border: 1px solid {border}; 
                border-radius: 12px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {soft}, stop:1 #151f2e);
            }}
            QTabBar::tab {{
                background: {soft}; 
                color: {text}; 
                padding: 12px 20px; 
                margin: 4px;
                border-radius: 10px; 
                border: 2px solid transparent;
                font-weight: 600;
                font-size: 13px;
            }}
            QTabBar::tab:hover {{
                background: #2a3a4f;
                border: 2px solid #334155;
            }}
            QTabBar::tab:selected {{ 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0ea5e9, stop:1 {accent}); 
                color: #ffffff;
                font-weight: 700;
            }}
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #60a5fa, stop:1 {accent});
                color: #ffffff; 
                border: none; 
                border-radius: 10px;
                padding: 12px 20px; 
                font-weight: 700;
                font-size: 13px;
                font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', Arial, sans-serif;
            }}
            QPushButton:hover {{ 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {accent_hover}, stop:1 #2563eb);
                padding: 12px 20px;
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563eb, stop:1 #1d4ed8);
                padding: 13px 20px 11px 20px;
            }}
            QPushButton:disabled {{ 
                background: #475569; 
                color: #94a3b8;
            }}
            QTableWidget {{ 
                background: {soft}; 
                color: {text}; 
                gridline-color: {border};
                border-radius: 8px;
            }}
            QTableWidget::item {{
                padding: 10px;
            }}
            QTableWidget::item:selected {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0ea5e9, stop:1 {accent});
                color: #ffffff;
            }}
            QTableWidget::item:hover {{
                background: #2a3a4f;
            }}
            QHeaderView::section {{ 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a3a4f, stop:1 {border});
                color: {text}; 
                padding: 12px; 
                border: none;
                font-weight: 700;
                font-size: 13px;
            }}
            QCheckBox {{ color: {text}; font-size: 14px; }}
            QScrollBar:vertical {{ 
                background: {surface}; 
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{ 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #334155, stop:1 {border});
                border-radius: 6px; 
                min-height: 40px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #475569, stop:1 #334155);
            }}
            QScrollBar:horizontal {{ 
                background: {surface}; 
                height: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:horizontal {{ 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #334155, stop:1 {border});
                border-radius: 6px; 
                min-width: 40px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #475569, stop:1 #334155);
            }}
        """)

    def build_header(self):
        accent = '#22c55e'
        frame = QFrame()
        frame.setObjectName('header')
        frame.setStyleSheet("""
            #header { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:0.5 #2563eb, stop:1 #1d4ed8);
                border-radius: 16px;
                border: 2px solid rgba(255,255,255,0.1);
            }
        """)
        layout = QHBoxLayout()
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # Icon/Logo section
        icon_label = QLabel('⚖️')
        icon_label.setStyleSheet("font-size: 42px; padding: 0px 8px;")
        
        title_box = QVBoxLayout()
        title_box.setSpacing(4)
        title = QLabel('Sistema de Gestión de Casos')
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: 800; 
            color: #ffffff;
            font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', Arial, sans-serif;
        """)
        subtitle = QLabel('Ministerio Público • Registre, analice y exporte expedientes')
        subtitle.setStyleSheet("""
            font-size: 13px; 
            color: rgba(255,255,255,0.95);
            font-weight: 500;
        """)
        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        # Status badges
        badges_layout = QVBoxLayout()
        badges_layout.setSpacing(6)
        
        badge_online = QLabel('🟢 Sistema Activo')
        badge_online.setAlignment(Qt.AlignmentFlag.AlignRight)
        badge_online.setStyleSheet("""
            background: rgba(255,255,255,0.25); 
            color: #ffffff; 
            padding: 6px 14px; 
            border-radius: 20px; 
            font-weight: 700;
            font-size: 12px;
            border: 1px solid rgba(255,255,255,0.3);
        """)
        
        badge_offline = QLabel('💾 Operación Local')
        badge_offline.setAlignment(Qt.AlignmentFlag.AlignRight)
        badge_offline.setStyleSheet("""
            background: rgba(255,255,255,0.2); 
            color: #ffffff; 
            padding: 6px 14px; 
            border-radius: 20px; 
            font-weight: 600;
            font-size: 11px;
            border: 1px solid rgba(255,255,255,0.2);
        """)
        
        badges_layout.addWidget(badge_online)
        badges_layout.addWidget(badge_offline)

        layout.addWidget(icon_label)
        layout.addLayout(title_box)
        layout.addStretch(1)
        layout.addLayout(badges_layout)
        frame.setLayout(layout)
        return frame

    def create_register_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create scroll area for the entire form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #1e293b;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #3b82f6;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #60a5fa;
            }
        """)

        # Content widget inside scroll area
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(12)
        content_layout.setContentsMargins(12, 12, 12, 12)

        card = QFrame()
        card.setObjectName('card')
        card.setStyleSheet("#card { background: #111827; border: 1px solid #1e293b; border-radius: 12px; }")
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(16)

        header = QLabel('Registrar nueva carpeta fiscal')
        header.setStyleSheet("font-size: 20px; font-weight: 700; margin-bottom: 10px;")
        card_layout.addWidget(header)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form.setHorizontalSpacing(15)
        form.setVerticalSpacing(12)
        form.setContentsMargins(0, 0, 0, 0)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        
        # Style for labels - smaller and more compact
        label_style = "font-weight: 600; color: #e5e7eb; font-size: 12px; padding: 4px 0;"

        # Section: Información Básica
        section1 = QLabel('━━━━ INFORMACIÓN BÁSICA ━━━━')
        section1.setStyleSheet('color: #60a5fa; font-weight: 700; font-size: 14px; margin-top: 5px; margin-bottom: 8px;')
        form.addRow(section1)

        lbl = QLabel('Número de Carpeta Fiscal')
        lbl.setStyleSheet(label_style)
        self.numero_carpeta = QLineEdit()
        self.numero_carpeta.setPlaceholderText('Ej. MP-2025-00123')
        self.numero_carpeta.setMinimumHeight(32)
        self.numero_carpeta.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form.addRow(lbl, self.numero_carpeta)

        lbl = QLabel('Categoría/Delito')
        lbl.setStyleSheet(label_style)
        self.categoria = QComboBox()
        self.categoria.addItems(self.categories)
        self.categoria.setMinimumHeight(32)
        self.categoria.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.categoria.currentTextChanged.connect(self.toggle_custom_category)
        form.addRow(lbl, self.categoria)

        lbl = QLabel('Categoría (otro)')
        lbl.setStyleSheet(label_style)
        self.categoria_custom = QLineEdit()
        self.categoria_custom.setPlaceholderText('Especifique la categoría')
        self.categoria_custom.setMinimumHeight(32)
        self.categoria_custom.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.categoria_custom.hide()
        form.addRow(lbl, self.categoria_custom)

        lbl = QLabel('Etapa procesal')
        lbl.setStyleSheet(label_style)
        self.etapa_procesal = QComboBox()
        self.etapa_procesal.addItems(['Investigación', 'Formalizado', 'Acusación presentada', 'En juicio', 'Archivo provisional', 'Archivo definitivo', 'Sobreseimiento'])
        self.etapa_procesal.setMinimumHeight(32)
        self.etapa_procesal.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form.addRow(lbl, self.etapa_procesal)

        # Section: Partes del Caso
        section2 = QLabel('━━━━ PARTES DEL CASO ━━━━')
        section2.setStyleSheet('color: #60a5fa; font-weight: 700; font-size: 14px; margin-top: 15px; margin-bottom: 8px;')
        form.addRow(section2)

        lbl = QLabel('Víctima')
        lbl.setStyleSheet(label_style)
        self.victima = QLineEdit()
        self.victima.setPlaceholderText('Víctima(s)')
        self.victima.setMinimumHeight(32)
        self.victima.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form.addRow(lbl, self.victima)

        lbl = QLabel('Investigado')
        lbl.setStyleSheet(label_style)
        self.investigado = QLineEdit()
        self.investigado.setPlaceholderText('Investigado(s)')
        self.investigado.setMinimumHeight(32)
        self.investigado.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form.addRow(lbl, self.investigado)

        # Section: FISCALES
        section_fiscales = QLabel('━━━━ FISCALES ━━━━')
        section_fiscales.setStyleSheet('color: #60a5fa; font-weight: 700; font-size: 14px; margin-top: 15px; margin-bottom: 8px;')
        form.addRow(section_fiscales)

        lbl = QLabel('Fiscal inicial')
        lbl.setStyleSheet(label_style)
        self.fiscal_inicial = QLineEdit()
        self.fiscal_inicial.setPlaceholderText('Fiscal que recibió el caso inicialmente')
        self.fiscal_inicial.setMinimumHeight(32)
        self.fiscal_inicial.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form.addRow(lbl, self.fiscal_inicial)

        lbl = QLabel('Fiscal asignado actual')
        lbl.setStyleSheet(label_style)
        self.fiscal_asignado = QLineEdit()
        self.fiscal_asignado.setPlaceholderText('Fiscal actualmente responsable')
        self.fiscal_asignado.setMinimumHeight(32)
        self.fiscal_asignado.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form.addRow(lbl, self.fiscal_asignado)

        lbl = QLabel('Departamento/Jurisdicción')
        lbl.setStyleSheet(label_style)
        self.departamento_actual = QComboBox()
        self.departamento_actual.addItems([
            '', 'San Salvador', 'Santa Ana', 'San Miguel', 'La Libertad', 
            'Sonsonate', 'Usulután', 'La Paz', 'Chalatenango', 'Ahuachapán',
            'Cuscatlán', 'La Unión', 'Morazán', 'Cabañas', 'San Vicente'
        ])
        self.departamento_actual.setMinimumHeight(32)
        self.departamento_actual.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form.addRow(lbl, self.departamento_actual)

        lbl = QLabel('Fiscal de cierre')
        lbl.setStyleSheet(label_style)
        self.fiscal_cierre = QLineEdit()
        self.fiscal_cierre.setPlaceholderText('Fiscal que cerró el caso (opcional)')
        self.fiscal_cierre.setMinimumHeight(32)
        self.fiscal_cierre.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form.addRow(lbl, self.fiscal_cierre)

        # Button to view transfer history
        history_btn = QPushButton('📋 Ver Historial de Transferencias')
        history_btn.setMinimumHeight(32)
        history_btn.setStyleSheet('''
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        ''')
        history_btn.clicked.connect(self.show_fiscal_history)
        form.addRow('', history_btn)

        # Section: Fechas Importantes
        section3 = QLabel('━━━━ FECHAS IMPORTANTES ━━━━')
        section3.setStyleSheet('color: #60a5fa; font-weight: 700; font-size: 14px; margin-top: 15px; margin-bottom: 8px;')
        form.addRow(section3)

        self._date_min = QDate(1900, 1, 1)

        def init_date_edit():
            widget = QDateEdit()
            widget.setCalendarPopup(True)
            widget.setDisplayFormat('yyyy-MM-dd')
            widget.setMinimumHeight(32)
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            max_date = QDate(7999, 12, 31)
            widget.setDateRange(self._date_min, max_date)
            widget.setSpecialValueText('Seleccione')
            widget.setDate(self._date_min)
            widget.lineEdit().setPlaceholderText('Seleccione')
            widget.lineEdit().clear()
            widget.calendarWidget().installEventFilter(self)
            return widget
        
        def create_date_field_with_clear(date_widget):
            """Create a date field with a clear button"""
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(8)
            
            layout.addWidget(date_widget, 1)  # Date widget takes most space
            
            clear_btn = QPushButton('🗑️')
            clear_btn.setFixedSize(50, 32)
            clear_btn.setToolTip('Limpiar fecha')
            clear_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #dc2626, stop:1 #b91c1c);
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 18px;
                    padding: 2px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #ef4444, stop:1 #dc2626);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #b91c1c, stop:1 #991b1b);
                }
            """)
            clear_btn.clicked.connect(lambda: self.clear_date_field(date_widget))
            layout.addWidget(clear_btn)
            
            return container

        lbl = QLabel('Fecha de denuncia')
        lbl.setStyleSheet(label_style)
        self.fecha_denuncia = init_date_edit()
        form.addRow(lbl, create_date_field_with_clear(self.fecha_denuncia))

        lbl = QLabel('Fecha de formalización')
        lbl.setStyleSheet(label_style)
        self.fecha_formalizacion = init_date_edit()
        form.addRow(lbl, create_date_field_with_clear(self.fecha_formalizacion))

        lbl = QLabel('Fecha de acusación')
        lbl.setStyleSheet(label_style)
        self.fecha_acusacion = init_date_edit()
        form.addRow(lbl, create_date_field_with_clear(self.fecha_acusacion))

        lbl = QLabel('Fecha de sentencia')
        lbl.setStyleSheet(label_style)
        self.fecha_sentencia = init_date_edit()
        form.addRow(lbl, create_date_field_with_clear(self.fecha_sentencia))

        lbl = QLabel('Fecha de archivo/cierre')
        lbl.setStyleSheet(label_style)
        self.fecha_archivo = init_date_edit()
        form.addRow(lbl, create_date_field_with_clear(self.fecha_archivo))

        # Section: Estado y Resultado
        section4 = QLabel('━━━━ ESTADO Y RESULTADO ━━━━')
        section4.setStyleSheet('color: #60a5fa; font-weight: 700; font-size: 14px; margin-top: 15px; margin-bottom: 8px;')
        form.addRow(section4)

        lbl = QLabel('💰 Monto de pensión mensual')
        lbl.setStyleSheet(label_style)
        self.monto_pension = QLineEdit()
        self.monto_pension.setPlaceholderText('Monto mensual de pensión alimentaria (solo para casos de pensión)')
        self.monto_pension.setMinimumHeight(32)
        self.monto_pension.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form.addRow(lbl, self.monto_pension)

        lbl = QLabel('Estado Actual')
        lbl.setStyleSheet(label_style)
        self.estado_actual = QComboBox()
        self.estado_actual.addItems(['Investigación', 'Formalizado', 'Acusación presentada', 'En juicio', 'Archivo provisional', 'Archivo definitivo', 'Sobreseimiento', 'Sentencia'])
        self.estado_actual.setMinimumHeight(32)
        self.estado_actual.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form.addRow(lbl, self.estado_actual)

        lbl = QLabel('Resultado')
        lbl.setStyleSheet(label_style)
        self.resultado = QComboBox()
        self.resultado.addItems(['', 'Condena', 'Absolución', 'Conciliación', 'Acuerdo', 'Archivo', 'Sobreseimiento'])
        self.resultado.setMinimumHeight(32)
        self.resultado.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form.addRow(lbl, self.resultado)

        lbl = QLabel('Apelación')
        lbl.setStyleSheet(label_style)
        self.apelacion = QCheckBox('Hubo apelación')
        self.apelacion.setMinimumHeight(32)
        self.apelacion.setStyleSheet("""
            QCheckBox {
                spacing: 8px;
                color: #f1f5f9;
            }
            QCheckBox::indicator {
                width: 22px;
                height: 22px;
                border: 2px solid #64748b;
                border-radius: 4px;
                background-color: #1e293b;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #94a3b8;
                background-color: #334155;
            }
            QCheckBox::indicator:checked {
                background-color: #3b82f6;
                border: 2px solid #2563eb;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #60a5fa;
                border: 2px solid #3b82f6;
            }
        """)
        form.addRow(lbl, self.apelacion)

        # Section: Citaciones
        section_cit = QLabel('━━━━ CITACIONES ━━━━')
        section_cit.setStyleSheet('color: #60a5fa; font-weight: 700; font-size: 14px; margin-top: 15px; margin-bottom: 8px;')
        form.addRow(section_cit)

        lbl = QLabel('')
        self.tiene_citacion = QCheckBox('Se emitió citación')
        self.tiene_citacion.setMinimumHeight(32)
        self.tiene_citacion.setStyleSheet("""
            QCheckBox {
                spacing: 8px;
                color: #f1f5f9;
            }
            QCheckBox::indicator {
                width: 22px;
                height: 22px;
                border: 2px solid #64748b;
                border-radius: 4px;
                background-color: #1e293b;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #94a3b8;
                background-color: #334155;
            }
            QCheckBox::indicator:checked {
                background-color: #3b82f6;
                border: 2px solid #2563eb;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #60a5fa;
                border: 2px solid #3b82f6;
            }
        """)
        self.tiene_citacion.stateChanged.connect(self.toggle_citation_fields)
        form.addRow(lbl, self.tiene_citacion)

        lbl = QLabel('Fecha de emisión de cita')
        lbl.setStyleSheet(label_style)
        self.fecha_emision_citacion = init_date_edit()
        form.addRow(lbl, create_date_field_with_clear(self.fecha_emision_citacion))

        lbl = QLabel('Fecha de comparecencia')
        lbl.setStyleSheet(label_style)
        self.fecha_comparecencia = init_date_edit()
        form.addRow(lbl, create_date_field_with_clear(self.fecha_comparecencia))

        lbl = QLabel('Estado de la cita')
        lbl.setStyleSheet(label_style)
        self.estado_citacion = QComboBox()
        self.estado_citacion.addItems(['', 'Pendiente', 'Compareció', 'No compareció', 'Cancelada'])
        self.estado_citacion.setMinimumHeight(32)
        self.estado_citacion.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form.addRow(lbl, self.estado_citacion)

        lbl = QLabel('Observaciones de cita')
        lbl.setStyleSheet(label_style)
        self.observaciones_citacion = QTextEdit()
        self.observaciones_citacion.setPlaceholderText('Detalles sobre la citación...')
        self.observaciones_citacion.setMinimumHeight(70)
        self.observaciones_citacion.setMaximumHeight(100)
        self.observaciones_citacion.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form.addRow(lbl, self.observaciones_citacion)

        # Ocultar campos de citación inicialmente
        self.fecha_emision_citacion.setEnabled(False)
        self.fecha_comparecencia.setEnabled(False)
        self.estado_citacion.setEnabled(False)
        self.observaciones_citacion.setEnabled(False)

        # Section: Orden de Arresto
        section5 = QLabel('━━━━ ORDEN DE ARRESTO ━━━━')
        section5.setStyleSheet('color: #60a5fa; font-weight: 700; font-size: 14px; margin-top: 15px; margin-bottom: 8px;')
        form.addRow(section5)

        lbl = QLabel('')
        self.tiene_orden_arresto = QCheckBox('Tiene orden de arresto vigente')
        self.tiene_orden_arresto.setMinimumHeight(32)
        self.tiene_orden_arresto.setStyleSheet("""
            QCheckBox {
                spacing: 8px;
                color: #f1f5f9;
            }
            QCheckBox::indicator {
                width: 22px;
                height: 22px;
                border: 2px solid #64748b;
                border-radius: 4px;
                background-color: #1e293b;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #94a3b8;
                background-color: #334155;
            }
            QCheckBox::indicator:checked {
                background-color: #3b82f6;
                border: 2px solid #2563eb;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #60a5fa;
                border: 2px solid #3b82f6;
            }
        """)
        self.tiene_orden_arresto.stateChanged.connect(self.toggle_arrest_fields)
        form.addRow(lbl, self.tiene_orden_arresto)

        lbl = QLabel('Origen de la orden')
        lbl.setStyleSheet(label_style)
        self.origen_orden_arresto = QComboBox()
        self.origen_orden_arresto.addItems(['', 'Directa con denuncia', 'Por no comparecencia a cita', 'Orden judicial posterior', 'Otro'])
        self.origen_orden_arresto.setMinimumHeight(32)
        self.origen_orden_arresto.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form.addRow(lbl, self.origen_orden_arresto)

        lbl = QLabel('Fecha de emisión')
        lbl.setStyleSheet(label_style)
        self.fecha_emision_orden = init_date_edit()
        form.addRow(lbl, create_date_field_with_clear(self.fecha_emision_orden))

        lbl = QLabel('Estado de la orden')
        lbl.setStyleSheet(label_style)
        self.estado_orden = QComboBox()
        self.estado_orden.addItems(['', 'Pendiente de cumplimiento', 'Cumplida', 'Cancelada', 'Revocada'])
        self.estado_orden.setMinimumHeight(32)
        self.estado_orden.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form.addRow(lbl, self.estado_orden)

        lbl = QLabel('Fecha de cumplimiento')
        lbl.setStyleSheet(label_style)
        self.fecha_cumplimiento_orden = init_date_edit()
        form.addRow(lbl, create_date_field_with_clear(self.fecha_cumplimiento_orden))

        lbl = QLabel('Observaciones')
        lbl.setStyleSheet(label_style)
        self.observaciones_orden = QTextEdit()
        self.observaciones_orden.setPlaceholderText('Detalles sobre la orden de arresto...')
        self.observaciones_orden.setMinimumHeight(70)
        self.observaciones_orden.setMaximumHeight(100)
        self.observaciones_orden.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form.addRow(lbl, self.observaciones_orden)

        # Ocultar campos inicialmente
        self.origen_orden_arresto.setEnabled(False)
        self.fecha_emision_orden.setEnabled(False)
        self.estado_orden.setEnabled(False)
        self.fecha_cumplimiento_orden.setEnabled(False)
        self.observaciones_orden.setEnabled(False)

        card_layout.addLayout(form)

        self.save_button = QPushButton('💾 Guardar Carpeta')
        self.save_button.setMinimumHeight(44)
        self.save_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                font-weight: 700;
            }
        """)
        self.save_button.clicked.connect(self.save_case)
        card_layout.addWidget(self.save_button)

        card.setLayout(card_layout)
        content_layout.addWidget(card)
        content_widget.setLayout(content_layout)
        
        # Set the content widget to the scroll area
        scroll.setWidget(content_widget)
        
        # Add scroll area to main layout
        layout.addWidget(scroll)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, 'Registrar Caso')

    def save_case(self):
        try:
            categoria_val = self.categoria_custom.text().strip() if self.categoria.currentText() == 'Otros' else self.categoria.currentText()

            def date_or_blank(widget):
                d = widget.date()
                if not widget.text() or widget.text() == widget.specialValueText():
                    return ''
                return d.toString('yyyy-MM-dd') if d.isValid() else ''

            case_data = (
                self.numero_carpeta.text(),
                categoria_val,
                self.etapa_procesal.currentText(),
                self.victima.text(),
                self.investigado.text(),
                date_or_blank(self.fecha_denuncia),
                date_or_blank(self.fecha_formalizacion),
                date_or_blank(self.fecha_acusacion),
                date_or_blank(self.fecha_sentencia),
                date_or_blank(self.fecha_archivo),
                self.estado_actual.currentText(),
                self.resultado.currentText(),
                1 if self.apelacion.isChecked() else 0,
                self.fiscal_asignado.text(),
                1 if self.tiene_citacion.isChecked() else 0,
                date_or_blank(self.fecha_emision_citacion),
                date_or_blank(self.fecha_comparecencia),
                self.estado_citacion.currentText(),
                self.observaciones_citacion.toPlainText(),
                1 if self.tiene_orden_arresto.isChecked() else 0,
                date_or_blank(self.fecha_emision_orden),
                self.estado_orden.currentText(),
                date_or_blank(self.fecha_cumplimiento_orden),
                self.observaciones_orden.toPlainText(),
                self.origen_orden_arresto.currentText(),
                self.fiscal_inicial.text(),
                self.departamento_actual.currentText(),
                self.fiscal_cierre.text(),
                float(self.monto_pension.text() or 0)
            )

            if self.current_edit_id:
                self.controller.update_case(self.current_edit_id, case_data)
                QMessageBox.information(self, 'Éxito', 'Carpeta actualizada exitosamente.')
            else:
                self.controller.add_case(case_data)
                QMessageBox.information(self, 'Éxito', 'Carpeta registrada exitosamente.')

            self.clear_form()
            self.load_cases()
            self.setup_autocompleters()  # Refresh autocompleters with new data
        except Exception as e:
            self._show_error_box(f'Error al guardar: {type(e).__name__}: {repr(e)}')

    def _show_error_box(self, message: str):
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setWindowTitle('Error')
        box.setText(message)
        box.setStyleSheet('QLabel { color: #0f172a; } QPushButton { color: #0f172a; }')
        box.exec()

    def clear_form(self):
        self.numero_carpeta.clear()
        self.categoria.setCurrentIndex(0)
        self.categoria_custom.clear()
        self.categoria_custom.hide()
        self.victima.clear()
        self.investigado.clear()
        self.monto_pension.clear()
        self.resultado.setCurrentIndex(0)
        self.apelacion.setChecked(False)
        self.fiscal_asignado.clear()
        self.fiscal_inicial.clear()
        self.departamento_actual.setCurrentIndex(0)
        self.fiscal_cierre.clear()
        self.tiene_citacion.setChecked(False)
        self.estado_citacion.setCurrentIndex(0)
        self.observaciones_citacion.clear()
        self.tiene_orden_arresto.setChecked(False)
        self.origen_orden_arresto.setCurrentIndex(0)
        self.estado_orden.setCurrentIndex(0)
        self.observaciones_orden.clear()
        self.current_edit_id = None
        if hasattr(self, 'save_button'):
            self.save_button.setText('💾 Guardar Carpeta')
        # Reset dates to blank display; calendar opens on today
        for widget in [self.fecha_denuncia, self.fecha_formalizacion, self.fecha_acusacion, 
                       self.fecha_sentencia, self.fecha_archivo, self.fecha_emision_citacion,
                       self.fecha_comparecencia, self.fecha_emision_orden, 
                       self.fecha_cumplimiento_orden]:
            widget.setDate(self._date_min)
            widget.lineEdit().setPlaceholderText('Seleccione')
            widget.lineEdit().clear()
    
    def clear_date_field(self, date_widget):
        """Clear a date field and reset it to blank/placeholder state"""
        date_widget.setDate(self._date_min)
        date_widget.lineEdit().setPlaceholderText('Seleccione')
        date_widget.lineEdit().clear()

    def create_view_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(12)

        layout.addWidget(self.build_summary_cards())

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Buscar texto libre (carpeta, nombres, etc.)')

        self.filter_categoria = QComboBox()
        # Add general categories first, then specific ones
        filter_categories = [
            'Todas',
            '─── Generales ───',
            'Pensión alimentaria (todas)',
            'Tránsito (todas)',
            '─── Específicas ───'
        ] + self.categories
        self.filter_categoria.addItems(filter_categories)
        self.filter_categoria.setCurrentIndex(0)  # Set "Todas" as default

        self.filter_etapa = QComboBox()
        self.filter_etapa.addItems(self.filter_etapas)

        self.filter_estado = QComboBox()
        self.filter_estado.addItems(['Todos', 'Investigación', 'Formalizado', 'Acusación presentada', 'En juicio', 'Archivo provisional', 'Archivo definitivo', 'Sobreseimiento', 'Sentencia'])

        self.filter_fiscal = QLineEdit()
        self.filter_fiscal.setPlaceholderText('Fiscal asignado')

        self.filter_apelados = QCheckBox('Solo apelados')
        self.filter_fecha_desde = QDateEdit()
        self.filter_fecha_desde.setCalendarPopup(True)
        self.filter_fecha_desde.setDisplayFormat('yyyy-MM-dd')
        self.filter_fecha_desde.setDate(QDate(1900, 1, 1))
        self.filter_fecha_desde.setMinimumDate(QDate(1900, 1, 1))
        self.filter_fecha_desde.setSpecialValueText('')
        self.filter_fecha_desde.lineEdit().clear()

        self.filter_fecha_hasta = QDateEdit()
        self.filter_fecha_hasta.setCalendarPopup(True)
        self.filter_fecha_hasta.setDisplayFormat('yyyy-MM-dd')
        self.filter_fecha_hasta.setDate(QDate(1900, 1, 1))
        self.filter_fecha_hasta.setSpecialValueText('')
        self.filter_fecha_hasta.lineEdit().clear()

        filters_row = QHBoxLayout()
        filters_row.addWidget(self.filter_categoria)
        filters_row.addWidget(self.filter_etapa)
        filters_row.addWidget(self.filter_estado)
        filters_row.addWidget(self.filter_fiscal)
        filters_row.addWidget(self.filter_apelados)

        fecha_layout = QHBoxLayout()
        fecha_layout.addWidget(QLabel('Denuncia desde'))
        fecha_layout.addWidget(self.filter_fecha_desde)
        fecha_layout.addWidget(QLabel('hasta'))
        fecha_layout.addWidget(self.filter_fecha_hasta)

        search_button = QPushButton('🔍 Buscar')
        search_button.clicked.connect(self.search_cases)
        
        clear_filters_button = QPushButton('🔄 Limpiar filtros')
        clear_filters_button.clicked.connect(self.clear_filters)
        clear_filters_button.setStyleSheet("""
            QPushButton {
                background: #ef4444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #dc2626;
            }
        """)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(clear_filters_button)

        search_card = QFrame()
        search_card.setObjectName('card')
        search_card.setStyleSheet(self.get_card_style('default'))
        search_card_layout = QVBoxLayout()
        search_card_layout.setContentsMargins(14, 14, 14, 14)
        search_card_layout.addLayout(search_layout)
        search_card_layout.addLayout(filters_row)
        search_card_layout.addLayout(fecha_layout)
        search_card.setLayout(search_card_layout)
        layout.addWidget(search_card)

        self.table = QTableWidget()
        self.table.setColumnCount(17)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Carpeta', 'Categoría/Delito', 'Etapa', 'Víctima', 'Investigado',
            'Fecha Denuncia', 'Fecha Formalización', 'Fecha Acusación', 'Fecha Sentencia',
            'Fecha Archivo', 'Estado', 'Resultado', 'Apelación', 'Citación', 'Fiscal', 'Orden Arresto'
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet(
            "QTableWidget::item { padding: 8px; } "
            "QTableWidget { alternate-background-color: #0f172a; }"
        )

        table_card = QFrame()
        table_card.setObjectName('card')
        table_card.setStyleSheet("#card { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; }")
        table_card_layout = QVBoxLayout()
        table_card_layout.setContentsMargins(10, 10, 10, 10)
        table_card_layout.addWidget(self.table)
        table_card.setLayout(table_card_layout)
        layout.addWidget(table_card)

        # Pagination controls
        pagination_layout = QHBoxLayout()
        pagination_layout.addStretch()
        
        self.prev_page_btn = QPushButton('◀ Anterior')
        self.prev_page_btn.clicked.connect(self.previous_page)
        self.prev_page_btn.setFixedWidth(120)
        
        self.page_label = QLabel('Página 1 de 1')
        self.page_label.setStyleSheet('font-size: 14px; font-weight: 600; color: #60a5fa; padding: 0 20px;')
        
        self.next_page_btn = QPushButton('Siguiente ▶')
        self.next_page_btn.clicked.connect(self.next_page)
        self.next_page_btn.setFixedWidth(120)
        
        self.items_per_page_combo = QComboBox()
        self.items_per_page_combo.addItems(['25', '50', '100', '200'])
        self.items_per_page_combo.setCurrentText('50')
        self.items_per_page_combo.currentTextChanged.connect(self.change_items_per_page)
        self.items_per_page_combo.setFixedWidth(80)
        
        pagination_layout.addWidget(QLabel('Por página:'))
        pagination_layout.addWidget(self.items_per_page_combo)
        pagination_layout.addWidget(self.prev_page_btn)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_page_btn)
        pagination_layout.addStretch()
        
        layout.addLayout(pagination_layout)

        refresh_button = QPushButton('🔄 Actualizar')
        refresh_button.clicked.connect(self.load_cases)
        actions_layout = QHBoxLayout()
        edit_button = QPushButton('✏️ Editar')
        edit_button.clicked.connect(self.load_selected_into_form)
        docs_button = QPushButton('📎 Documentos')
        docs_button.clicked.connect(self.open_documents_dialog)
        docs_button.setStyleSheet("background: #3b82f6;")
        delete_button = QPushButton('🗑️ Eliminar')
        delete_button.clicked.connect(self.delete_selected)
        actions_layout.addWidget(refresh_button)
        actions_layout.addWidget(edit_button)
        actions_layout.addWidget(docs_button)
        actions_layout.addWidget(delete_button)
        layout.addLayout(actions_layout)

        tab.setLayout(layout)
        self.tabs.addTab(tab, 'Ver Casos')
        self.load_cases()
        
        # Connect search events AFTER initial load
        self._connect_search_events()
    
    def _connect_search_events(self):
        """Connect search and filter events after tab is initialized"""
        self.search_input.textChanged.connect(self.search_cases)
        self.filter_categoria.currentIndexChanged.connect(self.search_cases)
        self.filter_etapa.currentIndexChanged.connect(self.search_cases)
        self.filter_estado.currentIndexChanged.connect(self.search_cases)
        self.filter_fiscal.textChanged.connect(self.search_cases)
        self.filter_apelados.stateChanged.connect(self.search_cases)

    def load_cases(self):
        # Invalidate cache to force fresh data from database
        self.controller.invalidate_caches()
        cases = self.controller.get_all_cases()
        self.filtered_cases = cases
        self.current_page = 1
        self._populate_table(cases)
        # Refresh export case list
        if hasattr(self, 'export_case_combo'):
            self.refresh_export_case_list()

    def _populate_table(self, cases):
        # Calculate pagination
        total_cases = len(cases)
        self.total_pages = max(1, math.ceil(total_cases / self.items_per_page))
        
        # Ensure current page is valid
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages
        
        # Calculate slice indices
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, total_cases)
        
        # Get page slice
        page_cases = cases[start_idx:end_idx]
        
        # Update table
        self.table.setRowCount(len(page_cases))
        for row, case in enumerate(page_cases):
            self.table.setItem(row, 0, QTableWidgetItem(str(case.id)))
            self.table.setItem(row, 1, QTableWidgetItem(case.numero_carpeta))
            self.table.setItem(row, 2, QTableWidgetItem(case.categoria))
            self.table.setItem(row, 3, QTableWidgetItem(case.etapa_procesal))
            self.table.setItem(row, 4, QTableWidgetItem(case.victima))
            self.table.setItem(row, 5, QTableWidgetItem(case.investigado))
            self.table.setItem(row, 6, QTableWidgetItem(case.fecha_denuncia))
            self.table.setItem(row, 7, QTableWidgetItem(case.fecha_formalizacion))
            self.table.setItem(row, 8, QTableWidgetItem(case.fecha_acusacion))
            self.table.setItem(row, 9, QTableWidgetItem(case.fecha_sentencia))
            self.table.setItem(row, 10, QTableWidgetItem(case.fecha_archivo))
            self.table.setItem(row, 11, QTableWidgetItem(case.estado_actual))
            self.table.setItem(row, 12, QTableWidgetItem(case.resultado))
            self.table.setItem(row, 13, QTableWidgetItem('Sí' if case.apelacion else 'No'))
            
            # Citation status
            tiene_cita = getattr(case, 'tiene_citacion', 0)
            estado_cita = getattr(case, 'estado_citacion', '')
            if tiene_cita == 1 and estado_cita:
                cita_item = QTableWidgetItem(estado_cita)
                # Color code by status
                if estado_cita == 'Pendiente':
                    cita_item.setForeground(QColor('#fbbf24'))  # Yellow
                elif estado_cita == 'Compareció':
                    cita_item.setForeground(QColor('#10b981'))  # Green
                elif estado_cita == 'No compareció':
                    cita_item.setForeground(QColor('#ef4444'))  # Red
                else:  # Cancelada
                    cita_item.setForeground(QColor('#6b7280'))  # Gray
                self.table.setItem(row, 14, cita_item)
            else:
                self.table.setItem(row, 14, QTableWidgetItem('N/A'))
            
            self.table.setItem(row, 15, QTableWidgetItem(case.fiscal_asignado))
            
            # Arrest warrant status
            tiene_orden = getattr(case, 'tiene_orden_arresto', 0)
            estado_orden = getattr(case, 'estado_orden', '')
            if tiene_orden == 1 and estado_orden:
                orden_item = QTableWidgetItem(estado_orden)
                # Color code by status
                if estado_orden == 'Pendiente de cumplimiento':
                    orden_item.setForeground(Qt.GlobalColor.red)
                elif estado_orden == 'Cumplida':
                    orden_item.setForeground(Qt.GlobalColor.green)
                else:
                    orden_item.setForeground(Qt.GlobalColor.yellow)
                self.table.setItem(row, 16, orden_item)
            else:
                self.table.setItem(row, 16, QTableWidgetItem('N/A'))
        
        # Update pagination controls
        self._update_pagination_controls(total_cases, start_idx, end_idx)
    
    def _update_pagination_controls(self, total_cases, start_idx, end_idx):
        """Update pagination UI controls"""
        # Update label
        if total_cases > 0:
            self.page_label.setText(
                f'Página {self.current_page} de {self.total_pages} | '
                f'Mostrando {start_idx + 1}-{end_idx} de {total_cases}'
            )
        else:
            self.page_label.setText('Sin resultados')
        
        # Enable/disable buttons
        self.prev_page_btn.setEnabled(self.current_page > 1)
        self.next_page_btn.setEnabled(self.current_page < self.total_pages)
    
    def next_page(self):
        """Go to next page"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._populate_table(self.filtered_cases)
    
    def previous_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self._populate_table(self.filtered_cases)
    
    def change_items_per_page(self, value):
        """Change number of items per page"""
        self.items_per_page = int(value)
        self.current_page = 1  # Reset to first page
        self._populate_table(self.filtered_cases)

    def _filter_cases(self):
        query = self.search_input.text().lower()
        cases = self.controller.get_all_cases()
        selected_cat = self.filter_categoria.currentText()
        selected_etapa = self.filter_etapa.currentText()
        selected_estado = self.filter_estado.currentText()
        fiscal_txt = self.filter_fiscal.text().lower().strip()
        only_apelados = self.filter_apelados.isChecked()

        # Check if date filters are active (not empty and not minimum date)
        min_date = QDate(1900, 1, 1)
        fecha_desde_active = self.filter_fecha_desde.date() > min_date
        fecha_hasta_active = self.filter_fecha_hasta.date() > min_date
        
        fd = self.filter_fecha_desde.date().toString('yyyy-MM-dd') if fecha_desde_active else None
        fh = self.filter_fecha_hasta.date().toString('yyyy-MM-dd') if fecha_hasta_active else None

        def matches(case):
            text_match = query in str(vars(case)).lower()
            
            # Category matching
            if selected_cat == 'Todas':
                cat_match = True
            elif selected_cat in ['─── Generales ───', '─── Específicas ───']:
                # Separators should show everything
                cat_match = True
            elif selected_cat == 'Pensión alimentaria (todas)':
                # Match all pension cases
                case_cat = (case.categoria or '').lower()
                cat_match = 'pensión' in case_cat or 'pension' in case_cat
            elif selected_cat == 'Tránsito (todas)':
                # Match all transit cases  
                case_cat = (case.categoria or '').lower()
                cat_match = 'tránsito' in case_cat or 'transito' in case_cat or 'accidente' in case_cat
            elif selected_cat == 'Otros':
                cat_match = case.categoria not in self.categories_without_otros
            else:
                # Use partial match to support both old and new category formats
                # This allows "Pensión alimentaria" to match any "Pensión" category
                case_cat = (case.categoria or '').lower()
                selected_cat_lower = selected_cat.lower()
                
                # Extract base category (e.g., "Pensión" from "Pensión - Apertura")
                if ' - ' in selected_cat_lower:
                    base_cat = selected_cat_lower.split(' - ')[0]
                else:
                    base_cat = selected_cat_lower
                
                # Match if the case category contains the base category or exact match
                cat_match = base_cat in case_cat or case_cat == selected_cat_lower

            etapa_match = True if selected_etapa == 'Todas' else case.etapa_procesal == selected_etapa
            estado_match = True if selected_estado == 'Todos' else case.estado_actual == selected_estado
            fiscal_match = True if not fiscal_txt else fiscal_txt in (case.fiscal_asignado or '').lower()
            apelacion_match = True if not only_apelados else bool(case.apelacion)

            date_match = True
            if fd:
                date_match = date_match and (case.fecha_denuncia >= fd)
            if fh:
                date_match = date_match and (case.fecha_denuncia <= fh)

            return text_match and cat_match and etapa_match and estado_match and fiscal_match and apelacion_match and date_match

        return [c for c in cases if matches(c)]

    def get_selected_case_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        return int(item.text()) if item else None

    def load_selected_into_form(self):
        case_id = self.get_selected_case_id()
        if case_id is None:
            QMessageBox.information(self, 'Seleccionar', 'Seleccione una fila para editar.')
            return
        
        # Get full case data from database
        all_cases = self.controller.get_all_cases()
        case = None
        for c in all_cases:
            # Handle both Case objects and dictionaries
            c_id = getattr(c, 'id', None) if hasattr(c, 'id') else c.get('id', None)
            if c_id == case_id:
                case = c
                break
        
        if not case:
            QMessageBox.warning(self, 'Error', 'No se pudo cargar el caso.')
            return
        
        # Helper function to get value from Case object or dict
        def get_value(obj, key, default=''):
            if hasattr(obj, key):
                return getattr(obj, key, default)
            elif isinstance(obj, dict):
                return obj.get(key, default)
            return default
        
        self.current_edit_id = case_id
        self.numero_carpeta.setText(get_value(case, 'numero_carpeta', ''))

        categoria_val = get_value(case, 'categoria', '')
        if categoria_val in self.categories:
            idx = self.categories.index(categoria_val)
            self.categoria.setCurrentIndex(idx)
            self.categoria_custom.hide()
            self.categoria_custom.clear()
        else:
            self.categoria.setCurrentText('Otros')
            self.categoria_custom.show()
            self.categoria_custom.setText(categoria_val)

        # Safe ComboBox handling for etapa_procesal
        etapa = str(get_value(case, 'etapa_procesal', ''))
        if etapa and etapa in [self.etapa_procesal.itemText(i) for i in range(self.etapa_procesal.count())]:
            self.etapa_procesal.setCurrentText(etapa)
        else:
            self.etapa_procesal.setCurrentIndex(0)
        
        self.victima.setText(get_value(case, 'victima', ''))
        self.investigado.setText(get_value(case, 'investigado', ''))

        def set_date(widget, value):
            if value:
                widget.setDate(QDate.fromString(value, 'yyyy-MM-dd'))
                widget.lineEdit().setText(widget.date().toString('yyyy-MM-dd'))
            else:
                widget.setDate(self._date_min)
                widget.lineEdit().setPlaceholderText('Seleccione')
                widget.lineEdit().clear()

        set_date(self.fecha_denuncia, get_value(case, 'fecha_denuncia', ''))
        set_date(self.fecha_formalizacion, get_value(case, 'fecha_formalizacion', ''))
        set_date(self.fecha_acusacion, get_value(case, 'fecha_acusacion', ''))
        set_date(self.fecha_sentencia, get_value(case, 'fecha_sentencia', ''))
        set_date(self.fecha_archivo, get_value(case, 'fecha_archivo', ''))

        self.monto_pension.setText(str(get_value(case, 'monto_pension', '')))
        self.estado_actual.setCurrentText(str(get_value(case, 'estado_actual', '')))
        self.resultado.setCurrentText(str(get_value(case, 'resultado', '')))
        self.apelacion.setChecked(get_value(case, 'apelacion', 0) == 1)
        self.fiscal_asignado.setText(get_value(case, 'fiscal_asignado', ''))
        self.fiscal_inicial.setText(get_value(case, 'fiscal_inicial', ''))
        
        # Safe ComboBox handling for departamento_actual
        depto_actual = str(get_value(case, 'departamento_actual', ''))
        if depto_actual and depto_actual in [self.departamento_actual.itemText(i) for i in range(self.departamento_actual.count())]:
            self.departamento_actual.setCurrentText(depto_actual)
        else:
            self.departamento_actual.setCurrentIndex(0)
        
        self.fiscal_cierre.setText(get_value(case, 'fiscal_cierre', ''))
        
        # Load citation data
        tiene_cita = get_value(case, 'tiene_citacion', 0) == 1
        self.tiene_citacion.setChecked(tiene_cita)
        set_date(self.fecha_emision_citacion, get_value(case, 'fecha_emision_citacion', ''))
        set_date(self.fecha_comparecencia, get_value(case, 'fecha_comparecencia', ''))
        
        # Safe ComboBox handling for estado_citacion
        estado_cita = str(get_value(case, 'estado_citacion', ''))
        if estado_cita and estado_cita in [self.estado_citacion.itemText(i) for i in range(self.estado_citacion.count())]:
            self.estado_citacion.setCurrentText(estado_cita)
        else:
            self.estado_citacion.setCurrentIndex(0)
        
        self.observaciones_citacion.setPlainText(get_value(case, 'observaciones_citacion', ''))
        
        # Load arrest warrant data
        tiene_orden = get_value(case, 'tiene_orden_arresto', 0) == 1
        self.tiene_orden_arresto.setChecked(tiene_orden)
        
        # Safe ComboBox handling for origen_orden_arresto
        origen_orden = str(get_value(case, 'origen_orden_arresto', ''))
        if origen_orden and origen_orden in [self.origen_orden_arresto.itemText(i) for i in range(self.origen_orden_arresto.count())]:
            self.origen_orden_arresto.setCurrentText(origen_orden)
        else:
            self.origen_orden_arresto.setCurrentIndex(0)
        
        set_date(self.fecha_emision_orden, get_value(case, 'fecha_emision_orden', ''))
        
        # Safe ComboBox handling for estado_orden
        estado_orden_val = str(get_value(case, 'estado_orden', ''))
        if estado_orden_val and estado_orden_val in [self.estado_orden.itemText(i) for i in range(self.estado_orden.count())]:
            self.estado_orden.setCurrentText(estado_orden_val)
        else:
            self.estado_orden.setCurrentIndex(0)
        
        set_date(self.fecha_cumplimiento_orden, get_value(case, 'fecha_cumplimiento_orden', ''))
        self.observaciones_orden.setPlainText(get_value(case, 'observaciones_orden', ''))
        
        if hasattr(self, 'save_button'):
            self.save_button.setText('✏️ Actualizar Carpeta')
        self.tabs.setCurrentIndex(0)

    def eventFilter(self, source, event):
        if isinstance(source, QCalendarWidget) and event.type() == QEvent.Type.Show:
            today = QDate.currentDate()
            source.setCurrentPage(today.year(), today.month())
        return super().eventFilter(source, event)

    def delete_selected(self):
        case_id = self.get_selected_case_id()
        if case_id is None:
            QMessageBox.information(self, 'Seleccionar', 'Seleccione una fila para eliminar.')
            return
        confirm = QMessageBox.question(self, 'Confirmar', '¿Eliminar la carpeta seleccionada?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self.controller.delete_case(case_id)
                QMessageBox.information(self, 'Éxito', 'Carpeta eliminada.')
                self.load_cases()
                self.setup_autocompleters()  # Refresh autocompleters after deletion
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'No se pudo eliminar: {str(e)}')

    def search_cases(self):
        filtered = self._filter_cases()
        self.filtered_cases = filtered
        self.current_page = 1  # Reset to first page on search
        self._populate_table(filtered)

    def clear_filters(self):
        """Clear all search filters and show all cases"""
        # Temporarily disconnect signals to avoid multiple search calls
        self._disconnect_search_events()
        
        self.search_input.clear()
        self.filter_categoria.setCurrentIndex(0)  # "Todas"
        self.filter_etapa.setCurrentIndex(0)  # "Todas"
        self.filter_estado.setCurrentIndex(0)  # "Todos"
        self.filter_fiscal.clear()
        self.filter_apelados.setChecked(False)
        self.filter_fecha_desde.lineEdit().clear()
        self.filter_fecha_hasta.lineEdit().clear()
        
        # Reconnect signals
        self._connect_search_events()
        
        # Trigger search once after clearing all filters
        self.search_cases()
    
    def _disconnect_search_events(self):
        """Disconnect search and filter events temporarily"""
        try:
            self.search_input.textChanged.disconnect(self.search_cases)
            self.filter_categoria.currentIndexChanged.disconnect(self.search_cases)
            self.filter_etapa.currentIndexChanged.disconnect(self.search_cases)
            self.filter_estado.currentIndexChanged.disconnect(self.search_cases)
            self.filter_fiscal.textChanged.disconnect(self.search_cases)
            self.filter_apelados.stateChanged.disconnect(self.search_cases)
        except:
            pass  # Signals may not be connected yet

    def create_stats_tab(self):
        """Create comprehensive dashboard tab"""
        tab = QWidget()
        tab.setStyleSheet("background: #0c1220;")
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scroll area for dashboard
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: #0c1220;
            }
            QScrollBar:vertical {
                background: #1e293b;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #3b82f6;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #60a5fa;
            }
        """)
        
        # Content widget
        content = QWidget()
        content.setStyleSheet("background: #0c1220;")
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Header
        header = QLabel('📊 Dashboard y Estadísticas')
        header.setStyleSheet('font-size: 22px; font-weight: 700; color: #60a5fa; margin-bottom: 8px;')
        layout.addWidget(header)
        
        # Quick stats cards
        stats_card = self._create_dashboard_stats_card()
        layout.addWidget(stats_card)
        
        # Statistics by area (NEW)
        area_stats_card = self._create_area_statistics_widget()
        layout.addWidget(area_stats_card)
        
        # Upcoming hearings / Important dates
        hearings_card = self._create_upcoming_hearings_card()
        layout.addWidget(hearings_card)
        
        # Recent activity card
        activity_card = self._create_recent_activity_card()
        layout.addWidget(activity_card)
        
        # Charts section
        charts_card = QFrame()
        charts_card.setObjectName('card')
        charts_card.setStyleSheet("""
            #card { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a2332, stop:1 #0f1621);
                border: 2px solid #1e293b; 
                border-radius: 16px;
            }
        """)
        charts_layout = QVBoxLayout()
        charts_layout.setContentsMargins(16, 16, 16, 16)
        charts_layout.setSpacing(12)
        
        charts_title = QLabel('📈 Gráficos y Análisis')
        charts_title.setStyleSheet('font-size: 16px; font-weight: 600; color: #f1f5f9;')
        charts_layout.addWidget(charts_title)
        
        # Chart buttons in responsive grid
        charts_grid = QHBoxLayout()
        charts_grid.setSpacing(12)
        charts_col1 = QVBoxLayout()
        charts_col2 = QVBoxLayout()
        
        buttons = [
            ('📊 Resueltos vs Pendientes', self.graph_utils.plot_resolved_vs_pending),
            ('🏷️ Casos por Categoría', self.graph_utils.plot_cases_by_category),
            ('📅 Casos por Mes', self.graph_utils.plot_cases_per_month),
            ('🔄 Casos por Estado', self.graph_utils.plot_cases_by_estado),
            ('⚖️ Proporción de Apelaciones', self.graph_utils.plot_appeals_ratio),
            ('🎯 Distribución por Área', self.graph_utils.plot_distribution_by_area),
            ('📑 Tipos de Resolución', self.graph_utils.plot_resolution_types),
        ]
        
        for i, (text, func) in enumerate(buttons):
            btn = QPushButton(text)
            btn.setObjectName(f'chart_btn_{i}')
            # Force blue gradient style for visibility
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #60a5fa, stop:1 #3b82f6);
                    color: #ffffff; 
                    border: none; 
                    border-radius: 10px;
                    padding: 12px 20px; 
                    font-weight: 700;
                    font-size: 13px;
                }
                QPushButton:hover { 
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #60a5fa, stop:1 #2563eb);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #2563eb, stop:1 #1d4ed8);
                }
            """)
            btn.clicked.connect(func)
            btn.setMinimumHeight(40)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            if i < 4:  # First 4 buttons in column 1
                charts_col1.addWidget(btn)
            else:  # Last 3 buttons in column 2
                charts_col2.addWidget(btn)
        
        charts_grid.addLayout(charts_col1)
        charts_grid.addLayout(charts_col2)
        charts_layout.addLayout(charts_grid)
        
        charts_card.setLayout(charts_layout)
        layout.addWidget(charts_card)
        
        # Refresh button
        refresh_dashboard_btn = QPushButton('🔄 Actualizar Dashboard')
        refresh_dashboard_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #60a5fa, stop:1 #3b82f6);
                color: #ffffff; 
                border: none; 
                border-radius: 10px;
                padding: 12px 20px; 
                font-weight: 700;
                font-size: 13px;
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #60a5fa, stop:1 #2563eb);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }
        """)
        refresh_dashboard_btn.clicked.connect(self.refresh_dashboard)
        refresh_dashboard_btn.setMinimumHeight(40)
        refresh_dashboard_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(refresh_dashboard_btn)
        
        # Export complete statistics button
        export_stats_btn = QPushButton('📊 Exportar Estadísticas Completas')
        export_stats_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #10b981, stop:1 #059669);
                color: #ffffff; 
                border: none; 
                border-radius: 10px;
                padding: 12px 20px; 
                font-weight: 700;
                font-size: 13px;
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #10b981, stop:1 #047857);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #047857, stop:1 #065f46);
            }
        """)
        export_stats_btn.clicked.connect(self.export_complete_statistics)
        export_stats_btn.setMinimumHeight(40)
        export_stats_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(export_stats_btn)
        
        layout.addStretch()
        content.setLayout(layout)
        scroll.setWidget(content)
        
        main_layout.addWidget(scroll)
        tab.setLayout(main_layout)
        self.tabs.addTab(tab, 'Dashboard')
    
    def _create_dashboard_stats_card(self):
        """Create dashboard statistics card"""
        main_container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # First section - General stats
        card = QFrame()
        card.setObjectName('card')
        card.setStyleSheet("#card { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; }")
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        title = QLabel('📈 Resumen Estadístico')
        title.setStyleSheet('font-size: 16px; font-weight: 600; color: #f1f5f9;')
        layout.addWidget(title)
        
        # Stats grid - responsive with wrapping
        stats_grid = QHBoxLayout()
        stats_grid.setSpacing(8)
        
        stats = self.controller.get_statistics()
        storage_info = self.document_service.get_storage_info()
        
        # Count arrest warrants
        all_cases = self.controller.get_all_cases()
        ordenes_pendientes = sum(1 for c in all_cases 
                                if getattr(c, 'tiene_orden_arresto', 0) == 1 
                                and getattr(c, 'estado_orden', '') == 'Pendiente de cumplimiento')
        ordenes_cumplidas = sum(1 for c in all_cases 
                               if getattr(c, 'tiene_orden_arresto', 0) == 1 
                               and getattr(c, 'estado_orden', '') == 'Cumplida')
        
        # Count citations
        citaciones_totales = sum(1 for c in all_cases if getattr(c, 'tiene_citacion', 0) == 1)
        citaciones_pendientes = sum(1 for c in all_cases 
                                    if getattr(c, 'tiene_citacion', 0) == 1 
                                    and getattr(c, 'estado_citacion', '') == 'Pendiente')
        citaciones_comparecidas = sum(1 for c in all_cases 
                                     if getattr(c, 'tiene_citacion', 0) == 1 
                                     and getattr(c, 'estado_citacion', '') == 'Compareció')
        citaciones_no_comparecidas = sum(1 for c in all_cases 
                                        if getattr(c, 'tiene_citacion', 0) == 1 
                                        and getattr(c, 'estado_citacion', '') == 'No compareció')
        
        stat_items = [
            ('Total Casos', len(self.controller.get_all_cases()), 'En el sistema', '#3b82f6'),
            ('Resueltos', stats.get('resolved', 0), 'Casos cerrados', '#3b82f6'),
            ('Pendientes', stats.get('pending', 0), 'Casos activos', '#f59e0b'),
            ('En Juicio', self._count_cases_by_estado('En juicio'), 'Etapa judicial', '#ef4444'),
            ('Citaciones Totales', citaciones_totales, 'Emitidas', '#8b5cf6'),
            ('Citas Pendientes', citaciones_pendientes, 'Sin comparecer', '#f59e0b'),
            ('Compareció', citaciones_comparecidas, 'Asistieron', '#22c55e'),
            ('No Compareció', citaciones_no_comparecidas, 'Ausentes', '#ef4444'),
            ('Órdenes Pendientes', ordenes_pendientes, 'Sin cumplimiento', '#ef4444'),
            ('Órdenes Cumplidas', ordenes_cumplidas, 'Ejecutadas', '#22c55e'),
        ]
        
        for title, value, detail, color in stat_items:
            stat_card = self._build_stat_card(title, str(value), detail, color)
            stats_grid.addWidget(stat_card)
        
        layout.addLayout(stats_grid)
        card.setLayout(layout)
        main_layout.addWidget(card)
        
        # Second section - Fiscal metrics
        fiscal_metrics = self.build_fiscal_metrics()
        if fiscal_metrics:
            main_layout.addWidget(fiscal_metrics)
        
        main_container.setLayout(main_layout)
        return main_container
    
    def _create_area_statistics_widget(self):
        """Create widget with statistics grouped by area"""
        card = QFrame()
        card.setObjectName('card')
        card.setStyleSheet("#card { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; }")
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)
        
        title = QLabel('📊 Estadísticas por Área')
        title.setStyleSheet('font-size: 18px; font-weight: 700; color: #60a5fa;')
        main_layout.addWidget(title)
        
        # Get statistics by area
        areas = self.get_statistics_by_area()
        
        # Create grid for area cards
        grid = QHBoxLayout()
        grid.setSpacing(16)
        
        # PENSIÓN ALIMENTARIA
        pension_card = self._create_area_detail_card(
            '📋 PENSIÓN ALIMENTARIA',
            areas['Pensión Alimentaria'],
            '#10b981'  # Verde
        )
        grid.addWidget(pension_card)
        
        # TRÁNSITO
        transito_card = self._create_area_detail_card(
            '🚗 TRÁNSITO',
            areas['Tránsito'],
            '#f59e0b'  # Naranja
        )
        grid.addWidget(transito_card)
        
        # OTROS CASOS
        otros_card = self._create_area_detail_card(
            '⚖️ OTROS CASOS',
            areas['Otros Casos'],
            '#8b5cf6'  # Púrpura
        )
        grid.addWidget(otros_card)
        
        main_layout.addLayout(grid)
        card.setLayout(main_layout)
        return card
    
    def _create_area_detail_card(self, title, cases, color):
        """Create detailed card for an area"""
        frame = QFrame()
        frame.setObjectName('areaCard')
        frame.setStyleSheet(f"""
            #areaCard {{
                background: #1a2332;
                border: 2px solid {color};
                border-radius: 12px;
                padding: 16px;
            }}
        """)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        
        # Title
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {color};")
        layout.addWidget(title_lbl)
        
        # Total count
        total = len(cases)
        total_lbl = QLabel(f'Total: {total} casos')
        total_lbl.setStyleSheet(f"font-size: 24px; font-weight: 800; color: {color};")
        layout.addWidget(total_lbl)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"background: {color}; max-height: 2px;")
        layout.addWidget(separator)
        
        # Category breakdown
        category_counts = {}
        total_pension_amount = 0
        
        for case in cases:
            cat = case.categoria if case.categoria else 'Sin categoría'
            category_counts[cat] = category_counts.get(cat, 0) + 1
            
            # Sum pension amounts if this is pension area
            if 'Pensión' in title and hasattr(case, 'monto_pension') and case.monto_pension:
                try:
                    total_pension_amount += float(case.monto_pension)
                except (ValueError, TypeError):
                    pass
        
        # Sort by count
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Show top 5 categories
        for cat, count in sorted_categories[:5]:
            cat_lbl = QLabel(f'• {cat}: {count}')
            cat_lbl.setStyleSheet("font-size: 12px; color: #cbd5e1; padding-left: 8px;")
            cat_lbl.setWordWrap(True)
            layout.addWidget(cat_lbl)
        
        # Show total pension amount if applicable
        if total_pension_amount > 0:
            layout.addSpacing(8)
            pension_total_lbl = QLabel(f'💰 Total Mensual: ${total_pension_amount:,.2f}')
            pension_total_lbl.setStyleSheet(f"font-size: 14px; font-weight: 700; color: {color}; padding: 8px; background: #0f172a; border-radius: 6px;")
            layout.addWidget(pension_total_lbl)
        
        layout.addStretch()
        frame.setLayout(layout)
        return frame
    
    def _create_upcoming_hearings_card(self):
        """Create upcoming hearings/important dates card"""
        card = QFrame()
        card.setObjectName('card')
        card.setStyleSheet("#card { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; }")
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        title = QLabel('📅 Próximos Eventos Importantes')
        title.setStyleSheet('font-size: 16px; font-weight: 600; color: #f1f5f9;')
        layout.addWidget(title)
        
        # Get upcoming events
        upcoming = self._get_upcoming_events()
        
        if not upcoming:
            no_events = QLabel('✓ No hay eventos próximos en los siguientes 30 días')
            no_events.setStyleSheet('font-size: 14px; color: #94a3b8; padding: 20px;')
            layout.addWidget(no_events)
        else:
            # Create table for events
            events_table = QTableWidget()
            events_table.setColumnCount(4)
            events_table.setHorizontalHeaderLabels(['Fecha', 'Tipo', 'Carpeta', 'Detalles'])
            events_table.setRowCount(len(upcoming))
            events_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            events_table.verticalHeader().setVisible(False)
            events_table.setMaximumHeight(250)
            events_table.setAlternatingRowColors(True)
            events_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            events_table.setStyleSheet("""
                QTableWidget { 
                    background-color: #1e293b; 
                    color: #f1f5f9;
                    gridline-color: #334155;
                    border: none;
                }
                QTableWidget::item { 
                    padding: 8px;
                    color: #f1f5f9;
                }
                QTableWidget::item:alternate { 
                    background-color: #0f172a;
                }
                QHeaderView::section { 
                    background-color: #0f172a;
                    color: #cbd5e1;
                    padding: 8px;
                    border: none;
                    border-bottom: 2px solid #334155;
                    font-weight: 600;
                }
            """)
            
            for row, event in enumerate(upcoming):
                events_table.setItem(row, 0, QTableWidgetItem(event['date']))
                events_table.setItem(row, 1, QTableWidgetItem(event['type']))
                events_table.setItem(row, 2, QTableWidgetItem(event['carpeta']))
                events_table.setItem(row, 3, QTableWidgetItem(event['details']))
            
            layout.addWidget(events_table)
        
        card.setLayout(layout)
        return card
    
    def _build_stat_card(self, title, value, detail, color):
        """Build a statistic card"""
        frame = QFrame()
        frame.setObjectName('metric')
        frame.setStyleSheet(f"#metric {{ background: #111827; border-left: 4px solid {color}; border-radius: 8px; padding: 12px; }}")
        frame.setMinimumWidth(140)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        vbox = QVBoxLayout()
        vbox.setSpacing(4)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 11px; color: #94a3b8; font-weight: 500;")
        title_lbl.setWordWrap(True)
        value_lbl = QLabel(value)
        value_lbl.setStyleSheet(f"font-size: 24px; font-weight: 800; color: {color};")
        detail_lbl = QLabel(detail)
        detail_lbl.setStyleSheet("font-size: 10px; color: #cbd5e1;")
        detail_lbl.setWordWrap(True)
        
        vbox.addWidget(title_lbl)
        vbox.addWidget(value_lbl)
        vbox.addWidget(detail_lbl)
        frame.setLayout(vbox)
        return frame
    
    def _count_cases_by_estado(self, estado):
        """Count cases by estado"""
        cases = self.controller.get_all_cases()
        return sum(1 for c in cases if c.estado_actual == estado)
    
    def _get_upcoming_events(self):
        """Get upcoming events (hearings, important dates) in next 30 days"""
        from datetime import datetime, timedelta
        import pandas as pd
        
        cases = self.controller.get_all_cases()
        events = []
        today = datetime.now()
        thirty_days = today + timedelta(days=30)
        
        for case in cases:
            # Check formalization dates
            if case.fecha_formalizacion:
                try:
                    date = pd.to_datetime(case.fecha_formalizacion)
                    if today <= date <= thirty_days:
                        events.append({
                            'date': date.strftime('%Y-%m-%d'),
                            'date_obj': date,
                            'type': 'Formalización',
                            'carpeta': case.numero_carpeta,
                            'details': f'Víctima: {case.victima}'
                        })
                except:
                    pass
            
            # Check accusation dates
            if case.fecha_acusacion:
                try:
                    date = pd.to_datetime(case.fecha_acusacion)
                    if today <= date <= thirty_days:
                        events.append({
                            'date': date.strftime('%Y-%m-%d'),
                            'date_obj': date,
                            'type': 'Acusación',
                            'carpeta': case.numero_carpeta,
                            'details': f'Fiscal: {case.fiscal_asignado}'
                        })
                except:
                    pass
            
            # Check sentence dates
            if case.fecha_sentencia:
                try:
                    date = pd.to_datetime(case.fecha_sentencia)
                    if today <= date <= thirty_days:
                        events.append({
                            'date': date.strftime('%Y-%m-%d'),
                            'date_obj': date,
                            'type': 'Sentencia',
                            'carpeta': case.numero_carpeta,
                            'details': f'Estado: {case.estado_actual}'
                        })
                except:
                    pass
        
        # Sort by date
        events.sort(key=lambda x: x['date_obj'])
        
        # Remove date_obj from display
        for event in events:
            del event['date_obj']
        
        return events[:10]  # Return max 10 events
    
    def _create_recent_activity_card(self):
        """Create recent activity card showing recently modified cases"""
        card = QFrame()
        card.setObjectName('card')
        card.setStyleSheet("#card { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; }")
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        title = QLabel('🕐 Actividad Reciente')
        title.setStyleSheet('font-size: 16px; font-weight: 600; color: #f1f5f9;')
        layout.addWidget(title)
        
        # Get recent cases (with updated_at timestamp)
        recent_cases = self._get_recent_cases(limit=8)
        
        if not recent_cases:
            no_activity = QLabel('Sin actividad reciente')
            no_activity.setStyleSheet('font-size: 14px; color: #94a3b8; padding: 20px;')
            layout.addWidget(no_activity)
        else:
            # Create list of recent cases
            for case in recent_cases:
                case_item = QFrame()
                case_item.setStyleSheet('background: #111827; border-radius: 6px; padding: 10px; margin: 2px;')
                case_layout = QHBoxLayout()
                case_layout.setContentsMargins(8, 8, 8, 8)
                
                # Case info
                info_layout = QVBoxLayout()
                info_layout.setSpacing(4)
                
                carpeta_label = QLabel(f"📁 {case['carpeta']}")
                carpeta_label.setStyleSheet('font-size: 13px; font-weight: 600; color: #f1f5f9;')
                
                details_label = QLabel(f"{case['categoria']} • {case['estado']}")
                details_label.setStyleSheet('font-size: 12px; color: #94a3b8;')
                
                info_layout.addWidget(carpeta_label)
                info_layout.addWidget(details_label)
                
                case_layout.addLayout(info_layout)
                case_layout.addStretch()
                
                # Timestamp
                time_label = QLabel(case['time_ago'])
                time_label.setStyleSheet('font-size: 11px; color: #64748b; font-style: italic;')
                case_layout.addWidget(time_label)
                
                case_item.setLayout(case_layout)
                layout.addWidget(case_item)
        
        card.setLayout(layout)
        return card
    
    def _get_recent_cases(self, limit=8):
        """Get recently modified cases"""
        try:
            conn = self.controller.db.get_connection()
            cursor = conn.execute(
                "SELECT numero_carpeta, categoria, estado_actual, updated_at FROM cases "
                "ORDER BY updated_at DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            
            recent = []
            for row in rows:
                carpeta, categoria, estado, updated_at = row
                time_ago = self._format_time_ago(updated_at)
                recent.append({
                    'carpeta': carpeta,
                    'categoria': categoria or 'Sin categoría',
                    'estado': estado or 'Sin estado',
                    'time_ago': time_ago
                })
            
            return recent
        except Exception as e:
            print(f"Error getting recent cases: {e}")
            return []
    
    def _format_time_ago(self, timestamp_str):
        """Format timestamp as 'time ago' string"""
        try:
            from datetime import datetime
            if not timestamp_str:
                return 'Desconocido'
            
            timestamp = datetime.fromisoformat(timestamp_str)
            now = datetime.now()
            diff = now - timestamp
            
            if diff.days > 0:
                if diff.days == 1:
                    return 'Hace 1 día'
                elif diff.days < 7:
                    return f'Hace {diff.days} días'
                elif diff.days < 30:
                    weeks = diff.days // 7
                    return f'Hace {weeks} semana{"s" if weeks > 1 else ""}'
                else:
                    months = diff.days // 30
                    return f'Hace {months} mes{"es" if months > 1 else ""}'
            
            hours = diff.seconds // 3600
            if hours > 0:
                return f'Hace {hours} hora{"s" if hours > 1 else ""}'
            
            minutes = diff.seconds // 60
            if minutes > 0:
                return f'Hace {minutes} minuto{"s" if minutes > 1 else ""}'
            
            return 'Hace un momento'
        except:
            return 'Desconocido'
    
    def refresh_dashboard(self):
        """Refresh dashboard data"""
        try:
            # Remove old stats card
            tab = self.tabs.widget(2)  # Dashboard tab is index 2
            if tab:
                layout = tab.layout()
                # Remove old cards and recreate
                for i in reversed(range(layout.count())):
                    item = layout.itemAt(i)
                    if item and item.widget():
                        widget = item.widget()
                        if isinstance(widget, QFrame):
                            widget.deleteLater()
                
                # Recreate stats, hearings, and activity cards
                layout.insertWidget(1, self._create_dashboard_stats_card())
                layout.insertWidget(2, self._create_upcoming_hearings_card())
                layout.insertWidget(3, self._create_recent_activity_card())
            
            QMessageBox.information(self, 'Actualizado', 'Dashboard actualizado exitosamente.')
        except Exception as e:
            self._show_error_box(f'Error al actualizar dashboard: {str(e)}')

    def create_export_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Card for individual case export
        single_card = QFrame()
        single_card.setObjectName('card')
        single_card.setStyleSheet("#card { background: #111827; border: 1px solid #1e293b; border-radius: 12px; }")
        single_card_layout = QVBoxLayout()
        single_card_layout.setContentsMargins(16, 16, 16, 16)
        single_card_layout.setSpacing(12)
        
        # Title for single case export
        single_title = QLabel('📄 Exportar Caso Individual')
        single_title.setStyleSheet('font-size: 16px; font-weight: bold; color: #3b82f6;')
        single_card_layout.addWidget(single_title)
        
        # ComboBox for case selection
        case_selector_layout = QHBoxLayout()
        case_selector_label = QLabel('Seleccionar caso:')
        case_selector_label.setStyleSheet('color: #94a3b8;')
        self.export_case_combo = QComboBox()
        self.export_case_combo.setMinimumHeight(32)
        self.export_case_combo.setStyleSheet("""
            QComboBox {
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 4px 8px;
                color: #e2e8f0;
            }
            QComboBox:hover {
                border-color: #3b82f6;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background: #1e293b;
                border: 1px solid #334155;
                selection-background-color: #3b82f6;
                color: #e2e8f0;
            }
        """)
        case_selector_layout.addWidget(case_selector_label)
        case_selector_layout.addWidget(self.export_case_combo, 1)
        single_card_layout.addLayout(case_selector_layout)
        
        # Buttons for single case export
        single_btn_layout = QHBoxLayout()
        export_single_csv_btn = QPushButton('📄 Exportar a CSV')
        export_single_csv_btn.setStyleSheet("background: #10b981;")
        export_single_csv_btn.clicked.connect(lambda: self.export_single_case('csv'))
        single_btn_layout.addWidget(export_single_csv_btn)
        
        export_single_excel_btn = QPushButton('📊 Exportar a Excel')
        export_single_excel_btn.setStyleSheet("background: #10b981;")
        export_single_excel_btn.clicked.connect(lambda: self.export_single_case('excel'))
        single_btn_layout.addWidget(export_single_excel_btn)
        single_card_layout.addLayout(single_btn_layout)
        
        single_card.setLayout(single_card_layout)
        layout.addWidget(single_card)

        # Card for bulk export
        card = QFrame()
        card.setObjectName('card')
        card.setStyleSheet("#card { background: #111827; border: 1px solid #1e293b; border-radius: 12px; }")
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(12)
        
        # Title for bulk export
        bulk_title = QLabel('📦 Exportación Masiva')
        bulk_title.setStyleSheet('font-size: 16px; font-weight: bold; color: #3b82f6;')
        card_layout.addWidget(bulk_title)

        export_csv_btn = QPushButton('Exportar a CSV (todos)')
        export_csv_btn.clicked.connect(lambda: self.export_data('csv', filtered=False))
        card_layout.addWidget(export_csv_btn)

        export_excel_btn = QPushButton('Exportar a Excel (todos)')
        export_excel_btn.clicked.connect(lambda: self.export_data('excel', filtered=False))
        card_layout.addWidget(export_excel_btn)

        export_csv_filtered_btn = QPushButton('Exportar filtrados a CSV')
        export_csv_filtered_btn.clicked.connect(lambda: self.export_data('csv', filtered=True))
        card_layout.addWidget(export_csv_filtered_btn)

        export_excel_filtered_btn = QPushButton('Exportar filtrados a Excel')
        export_excel_filtered_btn.clicked.connect(lambda: self.export_data('excel', filtered=True))
        card_layout.addWidget(export_excel_filtered_btn)
        
        # Add statistics export
        export_stats_btn = QPushButton('Exportar Reporte de Estadísticas')
        export_stats_btn.setStyleSheet("background: #3b82f6;")
        export_stats_btn.clicked.connect(self.export_statistics_report)
        card_layout.addWidget(export_stats_btn)
        
        # Add manual backup button
        backup_btn = QPushButton('Crear Respaldo Manual de BD')
        backup_btn.setStyleSheet("background: #f59e0b;")
        backup_btn.clicked.connect(self.create_manual_backup)
        card_layout.addWidget(backup_btn)

        card.setLayout(card_layout)
        layout.addWidget(card)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, 'Exportar')
        
        # Load cases into combo box
        self.refresh_export_case_list()

    def build_summary_cards(self):
        stats = self.controller.get_statistics()
        resolved = self._safe_number(stats.get('resolved', 0))
        pending = self._safe_number(stats.get('pending', 0))
        avg_time = self._safe_number(stats.get('avg_resolution_time', 0))
        appeal_pct = self._safe_number(stats.get('appeal_percentage', 0))
        
        # Add total cases card
        total_cases = len(self.filtered_cases) if self.filtered_cases else len(self.controller.get_all_cases())

        # General metrics only (fiscal metrics are now in Dashboard)
        wrapper = QFrame()
        wrapper.setObjectName('card')
        wrapper.setStyleSheet("#card { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; }")
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        for title, value, detail in [
            ('Total Casos', total_cases, 'En el sistema'),
            ('Resueltos', resolved, 'Casos cerrados'),
            ('Pendientes', pending, 'Casos activos'),
            ('Tiempo prom. (días)', round(avg_time, 1) if avg_time else 0, 'Resolución promedio'),
            ('% Apelaciones', f"{appeal_pct:.1f}%" if appeal_pct else '0%', 'Sobre total de casos'),
        ]:
            card = self._metric_card(title, value, detail)
            layout.addWidget(card)

        layout.addStretch(1)
        wrapper.setLayout(layout)
        return wrapper

    def _metric_card(self, title: str, value, detail: str):
        frame = QFrame()
        frame.setObjectName('metric')
        frame.setStyleSheet("#metric { background: #111827; border: 1px solid #1e293b; border-radius: 10px; }")
        vbox = QVBoxLayout()
        vbox.setContentsMargins(14, 12, 14, 12)
        vbox.setSpacing(6)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 13px; color: #94a3b8;")
        value_lbl = QLabel(str(value))
        value_lbl.setStyleSheet("font-size: 24px; font-weight: 800; color: #60a5fa;")
        detail_lbl = QLabel(detail)
        detail_lbl.setStyleSheet("font-size: 12px; color: #cbd5e1;")

        vbox.addWidget(title_lbl)
        vbox.addWidget(value_lbl)
        vbox.addWidget(detail_lbl)
        frame.setLayout(vbox)
        return frame
    
    def build_fiscal_metrics(self):
        """Build fiscal performance metrics section"""
        try:
            from controllers.fiscal_history_controller import FiscalHistoryController
            fiscal_controller = FiscalHistoryController()
            fiscal_stats = fiscal_controller.get_statistics()
            
            # Create container (always show, even with zero values)
            wrapper = QFrame()
            wrapper.setObjectName('fiscalCard')
            wrapper.setStyleSheet("#fiscalCard { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; }")
            main_layout = QVBoxLayout()
            main_layout.setContentsMargins(16, 16, 16, 16)
            main_layout.setSpacing(12)
            
            # Title
            title = QLabel('👥 Métricas de Fiscales')
            title.setStyleSheet("font-size: 16px; font-weight: 700; color: #60a5fa; margin-bottom: 8px;")
            main_layout.addWidget(title)
            
            # Metrics layout
            metrics_layout = QHBoxLayout()
            metrics_layout.setSpacing(12)
            
            # Get top fiscals (default to empty dicts if no data)
            asignados = fiscal_stats.get('asignados', {}) if fiscal_stats else {}
            recibidos = fiscal_stats.get('recibidos', {}) if fiscal_stats else {}
            cerrados = fiscal_stats.get('cerrados', {}) if fiscal_stats else {}
            declinaciones_salida = fiscal_stats.get('declinaciones_salida', {}) if fiscal_stats else {}
            declinaciones_entrada = fiscal_stats.get('declinaciones_entrada', {}) if fiscal_stats else {}
            
            # Total fiscals active
            total_fiscales = len(set(list(asignados.keys()) + list(recibidos.keys())))
            
            # Total cases per category
            total_asignados = sum(asignados.values())
            total_recibidos = sum(recibidos.values())
            total_cerrados = sum(cerrados.values())
            total_declinados = sum(declinaciones_salida.values())
            
            # Create metric cards
            for title, value, detail, color in [
                ('Fiscales Activos', total_fiscales, 'Con casos asignados', '#10b981'),
                ('Total Asignados', total_asignados, 'Casos actuales', '#3b82f6'),
                ('Total Cerrados', total_cerrados, 'Por todos los fiscales', '#6366f1'),
                ('Declinaciones', total_declinados, 'Transferencias realizadas', '#f59e0b'),
            ]:
                card = self._fiscal_metric_card(title, value, detail, color)
                metrics_layout.addWidget(card)
            
            # Top performers section
            if asignados:
                top_fiscal = max(asignados.items(), key=lambda x: x[1])
                top_card = self._fiscal_metric_card(
                    'Mayor Carga',
                    f"{top_fiscal[1]} casos",
                    f"Fiscal: {top_fiscal[0][:20]}...",
                    '#ef4444'
                )
                metrics_layout.addWidget(top_card)
            
            if cerrados:
                top_closer = max(cerrados.items(), key=lambda x: x[1])
                closer_card = self._fiscal_metric_card(
                    'Más Productivo',
                    f"{top_closer[1]} cerrados",
                    f"Fiscal: {top_closer[0][:20]}...",
                    '#10b981'
                )
                metrics_layout.addWidget(closer_card)
            
            metrics_layout.addStretch(1)
            main_layout.addLayout(metrics_layout)
            
            # Add detailed breakdown button
            details_btn = QPushButton('📊 Ver Detalles por Fiscal')
            details_btn.setMinimumHeight(36)
            details_btn.setEnabled(bool(fiscal_stats and (asignados or recibidos or cerrados)))  # Only enable if there's data
            details_btn.setStyleSheet('''
                QPushButton {
                    background-color: #1e293b;
                    color: #60a5fa;
                    border: 1px solid #334155;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #334155;
                    border-color: #3b82f6;
                }
            ''')
            details_btn.clicked.connect(lambda: self.show_fiscal_details_dialog(fiscal_stats))
            main_layout.addWidget(details_btn)
            
            wrapper.setLayout(main_layout)
            return wrapper
            
        except Exception as e:
            print(f"Error building fiscal metrics: {e}")
            return None
    
    def _fiscal_metric_card(self, title: str, value, detail: str, color: str):
        """Create a colored metric card for fiscal stats"""
        frame = QFrame()
        frame.setObjectName('fiscalMetric')
        frame.setStyleSheet(f"#fiscalMetric {{ background: #111827; border-left: 4px solid {color}; border-radius: 10px; }}")
        vbox = QVBoxLayout()
        vbox.setContentsMargins(14, 12, 14, 12)
        vbox.setSpacing(6)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 13px; color: #94a3b8; font-weight: 600;")
        value_lbl = QLabel(str(value))
        value_lbl.setStyleSheet(f"font-size: 22px; font-weight: 800; color: {color};")
        detail_lbl = QLabel(detail)
        detail_lbl.setStyleSheet("font-size: 11px; color: #cbd5e1;")
        detail_lbl.setWordWrap(True)

        vbox.addWidget(title_lbl)
        vbox.addWidget(value_lbl)
        vbox.addWidget(detail_lbl)
        frame.setLayout(vbox)
        return frame
    
    def show_fiscal_details_dialog(self, fiscal_stats):
        """Show detailed fiscal statistics dialog"""
        from views.fiscal_stats_dialog import FiscalStatsDialog
        dialog = FiscalStatsDialog(fiscal_stats, self)
        dialog.exec()

    def toggle_custom_category(self, text):
        if text == 'Otros':
            self.categoria_custom.show()
        else:
            self.categoria_custom.hide()
            self.categoria_custom.clear()

    def toggle_arrest_fields(self, state):
        """Enable/disable arrest warrant fields based on checkbox"""
        enabled = state == 2  # Qt.CheckState.Checked
        self.origen_orden_arresto.setEnabled(enabled)
        self.fecha_emision_orden.setEnabled(enabled)
        self.estado_orden.setEnabled(enabled)
        self.fecha_cumplimiento_orden.setEnabled(enabled)
        self.observaciones_orden.setEnabled(enabled)

    def toggle_citation_fields(self, state):
        """Enable/disable citation fields based on checkbox"""
        enabled = state == 2  # Qt.CheckState.Checked
        self.fecha_emision_citacion.setEnabled(enabled)
        self.fecha_comparecencia.setEnabled(enabled)
        self.estado_citacion.setEnabled(enabled)
        self.observaciones_citacion.setEnabled(enabled)

    def _safe_number(self, value):
        try:
            if value is None:
                return 0
            if isinstance(value, (int, float)) and math.isfinite(value):
                return value
            return 0
        except Exception:
            return 0

    def export_data(self, format, filtered=False):
        cases = self.filtered_cases if (filtered and self.filtered_cases) else self.controller.get_all_cases()
        if not cases:
            QMessageBox.warning(self, 'Sin datos', 'No hay casos para exportar.')
            return
        
        try:
            if format == 'csv':
                filepath = self.export_service.export_to_csv(cases, filtered=filtered)
            elif format == 'excel':
                filepath = self.export_service.export_to_excel(cases, filtered=filtered)
            else:
                QMessageBox.warning(self, 'Error', 'Formato no soportado.')
                return
            
            QMessageBox.information(self, 'Éxito', f'Datos exportados exitosamente a:\n{filepath}')
        except Exception as e:
            self._show_error_box(f'Error al exportar: {str(e)}')
    
    def export_statistics_report(self):
        """Export comprehensive statistics report"""
        try:
            stats = self.controller.get_statistics()
            filepath = self.export_service.export_statistics_report(stats)
            QMessageBox.information(self, 'Éxito', 
                                   f'Reporte de estadísticas exportado:\n{filepath}')
        except Exception as e:
            self._show_error_box(f'Error al exportar estadísticas: {str(e)}')
    
    def export_complete_statistics(self):
        """Export complete statistics with all areas and categories"""
        try:
            cases = self.controller.get_all_cases()
            if not cases:
                QMessageBox.warning(self, 'Advertencia', 
                                   'No hay casos disponibles para exportar.')
                return
            
            filepath = self.export_service.export_complete_statistics(cases)
            QMessageBox.information(self, 'Éxito', 
                                   f'Estadísticas completas exportadas exitosamente:\n{filepath}\n\n'
                                   f'El archivo incluye {len(cases)} casos organizados por área:\n'
                                   f'• Pensión Alimentaria\n'
                                   f'• Tránsito\n'
                                   f'• Otros Casos\n'
                                   f'• Tipos de Resolución')
        except Exception as e:
            self._show_error_box(f'Error al exportar estadísticas completas: {str(e)}')
    
    def create_manual_backup(self):
        """Create manual database backup"""
        try:
            from utils.backup_manager import BackupManager
            backup_mgr = BackupManager()
            backup_path = backup_mgr.create_backup(prefix='manual')
            QMessageBox.information(self, 'Éxito', 
                                   f'Respaldo creado exitosamente:\n{backup_path}')
        except Exception as e:
            self._show_error_box(f'Error al crear respaldo: {str(e)}')
    
    def refresh_export_case_list(self):
        """Refresh the list of cases in the export combo box"""
        try:
            self.export_case_combo.clear()
            cases = self.controller.get_all_cases()
            
            if not cases:
                self.export_case_combo.addItem('No hay casos disponibles')
                return
            
            # Add cases to combo box with format: "Caso #123 - Víctima vs Investigado"
            for case in cases:
                display_text = f"Caso #{case.numero_carpeta} - {case.victima} vs {case.investigado}"
                self.export_case_combo.addItem(display_text, case.id)
                
        except Exception as e:
            print(f"Error refreshing export case list: {str(e)}")
    
    def export_single_case(self, format):
        """Export a single selected case"""
        if self.export_case_combo.count() == 0 or self.export_case_combo.currentText() == 'No hay casos disponibles':
            QMessageBox.warning(self, 'Sin datos', 'No hay casos disponibles para exportar.')
            return
        
        # Get selected case ID
        case_id = self.export_case_combo.currentData()
        if case_id is None:
            QMessageBox.warning(self, 'Error', 'Por favor selecciona un caso válido.')
            return
        
        # Get the case from database
        all_cases = self.controller.get_all_cases()
        selected_case = None
        for case in all_cases:
            if case.id == case_id:
                selected_case = case
                break
        
        if not selected_case:
            QMessageBox.warning(self, 'Error', 'No se pudo encontrar el caso seleccionado.')
            return
        
        try:
            # Export single case as a list with one item
            if format == 'csv':
                filepath = self.export_service.export_to_csv([selected_case], filtered=False, single=True)
            elif format == 'excel':
                filepath = self.export_service.export_to_excel([selected_case], filtered=False, single=True)
            else:
                QMessageBox.warning(self, 'Error', 'Formato no soportado.')
                return
            
            QMessageBox.information(self, 'Éxito', 
                f'Caso exportado exitosamente:\n{filepath}\n\nCaso: #{selected_case.numero_carpeta}')
        except Exception as e:
            self._show_error_box(f'Error al exportar caso: {str(e)}')
    
    def create_import_tab(self):
        """Create import tab for bulk case import"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(16)
        
        # Header card
        header_card = QFrame()
        header_card.setObjectName('card')
        header_card.setStyleSheet("#card { background: #111827; border: 1px solid #1e293b; border-radius: 12px; }")
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel('📥 Importación Masiva de Casos')
        title.setStyleSheet('font-size: 20px; font-weight: 700; color: #60a5fa;')
        desc = QLabel('Importe múltiples casos desde archivos CSV o Excel (.xlsx, .xls)')
        desc.setStyleSheet('font-size: 14px; color: #94a3b8; margin-top: 4px;')
        
        header_layout.addWidget(title)
        header_layout.addWidget(desc)
        header_card.setLayout(header_layout)
        layout.addWidget(header_card)
        
        # Template section
        template_card = QFrame()
        template_card.setObjectName('card')
        template_card.setStyleSheet("#card { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; }")
        template_layout = QVBoxLayout()
        template_layout.setContentsMargins(16, 16, 16, 16)
        
        template_title = QLabel('📄 Plantilla de Importación')
        template_title.setStyleSheet('font-size: 16px; font-weight: 600; color: #f1f5f9;')
        template_info = QLabel('Descargue una plantilla con el formato correcto para importar casos.')
        template_info.setStyleSheet('font-size: 13px; color: #cbd5e1; margin-top: 4px;')
        
        template_buttons = QHBoxLayout()
        download_excel_btn = QPushButton('⬇️ Descargar Plantilla Excel')
        download_excel_btn.clicked.connect(lambda: self.download_template('excel'))
        download_csv_btn = QPushButton('⬇️ Descargar Plantilla CSV')
        download_csv_btn.clicked.connect(lambda: self.download_template('csv'))
        template_buttons.addWidget(download_excel_btn)
        template_buttons.addWidget(download_csv_btn)
        template_buttons.addStretch()
        
        template_layout.addWidget(template_title)
        template_layout.addWidget(template_info)
        template_layout.addLayout(template_buttons)
        template_card.setLayout(template_layout)
        layout.addWidget(template_card)
        
        # File selection section
        file_card = QFrame()
        file_card.setObjectName('card')
        file_card.setStyleSheet("#card { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; }")
        file_layout = QVBoxLayout()
        file_layout.setContentsMargins(16, 16, 16, 16)
        
        file_title = QLabel('📂 Seleccionar Archivo')
        file_title.setStyleSheet('font-size: 16px; font-weight: 600; color: #f1f5f9;')
        
        file_select_layout = QHBoxLayout()
        self.import_file_path = QLineEdit()
        self.import_file_path.setPlaceholderText('Seleccione un archivo CSV o Excel...')
        self.import_file_path.setReadOnly(True)
        browse_btn = QPushButton('🔍 Examinar')
        browse_btn.clicked.connect(self.browse_import_file)
        browse_btn.setFixedWidth(120)
        file_select_layout.addWidget(self.import_file_path)
        file_select_layout.addWidget(browse_btn)
        
        self.skip_duplicates_check = QCheckBox('Omitir carpetas duplicadas (no mostrar error)')
        self.skip_duplicates_check.setChecked(True)
        self.skip_duplicates_check.setStyleSheet('font-size: 13px; color: #cbd5e1; margin-top: 8px;')
        
        validate_btn = QPushButton('✓ Validar Archivo')
        validate_btn.clicked.connect(self.validate_import_file)
        validate_btn.setFixedWidth(180)
        
        file_layout.addWidget(file_title)
        file_layout.addLayout(file_select_layout)
        file_layout.addWidget(self.skip_duplicates_check)
        file_layout.addWidget(validate_btn)
        file_card.setLayout(file_layout)
        layout.addWidget(file_card)
        
        # Preview section
        preview_card = QFrame()
        preview_card.setObjectName('card')
        preview_card.setStyleSheet("#card { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; }")
        preview_layout = QVBoxLayout()
        preview_layout.setContentsMargins(16, 16, 16, 16)
        
        preview_title = QLabel('👁️ Vista Previa')
        preview_title.setStyleSheet('font-size: 16px; font-weight: 600; color: #f1f5f9;')
        
        self.import_preview_text = QTextEdit()
        self.import_preview_text.setReadOnly(True)
        self.import_preview_text.setMaximumHeight(200)
        self.import_preview_text.setPlaceholderText('La vista previa aparecerá aquí después de validar el archivo...')
        
        preview_layout.addWidget(preview_title)
        preview_layout.addWidget(self.import_preview_text)
        preview_card.setLayout(preview_layout)
        layout.addWidget(preview_card)
        
        # Progress section
        self.import_progress_bar = QProgressBar()
        self.import_progress_bar.setVisible(False)
        self.import_progress_bar.setStyleSheet('''
            QProgressBar {
                border: 2px solid #1e293b;
                border-radius: 8px;
                text-align: center;
                background: #0f172a;
                color: #f1f5f9;
                font-weight: 600;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #60a5fa, stop:1 #3b82f6);
                border-radius: 6px;
            }
        ''')
        layout.addWidget(self.import_progress_bar)
        
        # Import button
        import_btn = QPushButton('📤 Importar Casos')
        import_btn.clicked.connect(self.import_cases)
        import_btn.setMinimumHeight(44)
        import_btn.setEnabled(False)
        self.import_button = import_btn
        layout.addWidget(import_btn)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, 'Importar')
        
        # Store validated dataframe
        self.validated_import_df = None
    
    def download_template(self, format):
        """Download import template"""
        try:
            ext = 'xlsx' if format == 'excel' else 'csv'
            filepath, _ = QFileDialog.getSaveFileName(
                self,
                'Guardar Plantilla',
                f'plantilla_importacion.{ext}',
                f'{"Excel Files (*.xlsx)" if format == "excel" else "CSV Files (*.csv)"}'
            )
            
            if filepath:
                self.import_service.generate_template(filepath, format)
                QMessageBox.information(self, 'Éxito', f'Plantilla guardada en:\n{filepath}')
        except Exception as e:
            self._show_error_box(f'Error al generar plantilla: {str(e)}')
    
    def browse_import_file(self):
        """Browse for import file"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            'Seleccionar Archivo',
            '',
            'All Supported (*.csv *.xlsx *.xls);;CSV Files (*.csv);;Excel Files (*.xlsx *.xls)'
        )
        
        if filepath:
            self.import_file_path.setText(filepath)
            self.import_preview_text.clear()
            self.import_button.setEnabled(False)
            self.validated_import_df = None
    
    def validate_import_file(self):
        """Validate import file"""
        filepath = self.import_file_path.text()
        if not filepath:
            QMessageBox.warning(self, 'Advertencia', 'Seleccione un archivo primero.')
            return
        
        try:
            valid, message, df = self.import_service.validate_file(filepath)
            
            if not valid:
                self._show_error_box(f'Validación fallida:\n{message}')
                self.import_button.setEnabled(False)
                self.validated_import_df = None
                return
            
            # Show preview
            preview_data = self.import_service.preview_import(df, limit=10)
            preview_text = f"✓ {message}\n\n"
            preview_text += "Vista previa (primeros 10 registros):\n"
            preview_text += "=" * 50 + "\n\n"
            
            for i, record in enumerate(preview_data, 1):
                preview_text += f"Registro {i}:\n"
                preview_text += f"  • Carpeta: {record.get('numero_carpeta', 'N/A')}\n"
                preview_text += f"  • Categoría: {record.get('categoria', 'N/A')}\n"
                preview_text += f"  • Víctima: {record.get('victima', 'N/A')}\n"
                preview_text += f"  • Investigado: {record.get('investigado', 'N/A')}\n"
                preview_text += f"  • Fiscal: {record.get('fiscal_asignado', 'N/A')}\n"
                preview_text += "\n"
            
            self.import_preview_text.setText(preview_text)
            self.validated_import_df = df
            self.import_button.setEnabled(True)
            
            QMessageBox.information(self, 'Validación Exitosa', message)
            
        except Exception as e:
            self._show_error_box(f'Error durante validación:\n{str(e)}')
            self.import_button.setEnabled(False)
    
    def import_cases(self):
        """Import cases from validated file"""
        if self.validated_import_df is None:
            QMessageBox.warning(self, 'Advertencia', 'Valide el archivo primero.')
            return
        
        total_rows = len(self.validated_import_df)
        
        # Confirm import
        reply = QMessageBox.question(
            self,
            'Confirmar Importación',
            f'¿Desea importar {total_rows} casos?\n\n'
            f'{"Se omitirán" if self.skip_duplicates_check.isChecked() else "Se reportarán"} las carpetas duplicadas.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        try:
            # Show progress bar
            self.import_progress_bar.setVisible(True)
            self.import_progress_bar.setValue(0)
            self.import_button.setEnabled(False)
            
            # Import cases
            skip_dupes = self.skip_duplicates_check.isChecked()
            successful, skipped, errors = self.import_service.import_cases(
                self.validated_import_df,
                skip_duplicates=skip_dupes
            )
            
            self.import_progress_bar.setValue(100)
            
            # Show results
            result_msg = f'Importación completada:\n\n'
            result_msg += f'✓ Exitosos: {successful}\n'
            if skipped > 0:
                result_msg += f'⊘ Omitidos (duplicados): {skipped}\n'
            if errors:
                result_msg += f'✗ Errores: {len(errors)}\n\n'
                result_msg += 'Primeros errores:\n'
                result_msg += '\n'.join(errors[:5])
                if len(errors) > 5:
                    result_msg += f'\n... y {len(errors) - 5} más'
            
            if successful > 0:
                # Refresh data
                self.load_cases()
                self.setup_autocompleters()
                self.refresh_alerts()
            
            if errors:
                self._show_error_box(result_msg)
            else:
                QMessageBox.information(self, 'Importación Completada', result_msg)
            
            # Reset
            self.import_file_path.clear()
            self.import_preview_text.clear()
            self.validated_import_df = None
            self.import_button.setEnabled(False)
            self.import_progress_bar.setVisible(False)
            
        except Exception as e:
            self._show_error_box(f'Error durante importación:\n{str(e)}')
        finally:
            self.import_progress_bar.setVisible(False)
            self.import_button.setEnabled(True)

    def create_alerts_tab(self):
        """Create tab for notifications and alerts"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(12)
        
        # Header card
        header_card = QFrame()
        header_card.setObjectName('card')
        header_card.setStyleSheet("#card { background: #111827; border: 1px solid #1e293b; border-radius: 12px; }")
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(16, 16, 16, 16)
        
        title = QLabel('Sistema de Alertas y Notificaciones')
        title.setStyleSheet("font-size: 18px; font-weight: 700;")
        header_layout.addWidget(title)
        
        subtitle = QLabel('Monitoreo automático de casos que requieren atención')
        subtitle.setStyleSheet("font-size: 14px; color: #cbd5e1;")
        header_layout.addWidget(subtitle)
        
        # Refresh button
        refresh_btn = QPushButton('Actualizar Alertas')
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #60a5fa, stop:1 #3b82f6);
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 12px 20px;
                font-weight: 700;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #60a5fa, stop:1 #2563eb);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }
        """)
        refresh_btn.clicked.connect(self.refresh_alerts)
        header_layout.addWidget(refresh_btn)
        
        header_card.setLayout(header_layout)
        layout.addWidget(header_card)
        
        # Summary cards
        self.alerts_summary_container = QFrame()
        layout.addWidget(self.alerts_summary_container)
        
        # Alerts table
        table_card = QFrame()
        table_card.setObjectName('card')
        table_card.setStyleSheet("#card { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; }")
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(10, 10, 10, 10)
        
        self.alerts_table = QTableWidget()
        self.alerts_table.setColumnCount(5)
        self.alerts_table.setHorizontalHeaderLabels(['Severidad', 'Carpeta', 'Tipo', 'Mensaje', 'Acción'])
        self.alerts_table.setAlternatingRowColors(True)
        self.alerts_table.setShowGrid(False)
        self.alerts_table.horizontalHeader().setStretchLastSection(False)
        # Set column widths - fixed sizes for better control
        self.alerts_table.setColumnWidth(0, 100)  # Severidad
        self.alerts_table.setColumnWidth(1, 120)  # Carpeta
        self.alerts_table.setColumnWidth(2, 150)  # Tipo
        self.alerts_table.setColumnWidth(4, 140)  # Acción - wider for complete button
        # Mensaje column will stretch to fill remaining space
        self.alerts_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.alerts_table.setStyleSheet("""
            QTableWidget { 
                background-color: #0f172a;
                alternate-background-color: #1e293b;
                color: #f1f5f9;
                gridline-color: #334155;
                border: none;
            }
            QTableWidget::item { 
                padding: 8px;
                color: #f1f5f9;
            }
            QHeaderView::section { 
                background-color: #0f172a;
                color: #cbd5e1;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #334155;
                font-weight: 600;
            }
        """)
        
        table_layout.addWidget(self.alerts_table)
        table_card.setLayout(table_layout)
        layout.addWidget(table_card)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, 'Alertas')
        
        # Load alerts initially
        self.refresh_alerts()
    
    def refresh_alerts(self):
        """Refresh alerts and update display"""
        try:
            cases = self.controller.get_all_cases()
            alerts = self.notification_manager.check_case_alerts(cases)
            summary = self.notification_manager.get_alert_summary(alerts)
            
            # Update summary cards
            self._update_alerts_summary(summary)
            
            # Update table
            self.alerts_table.setRowCount(len(alerts))
            for row, alert in enumerate(alerts):
                # Set row height for better button visibility
                self.alerts_table.setRowHeight(row, 45)
                
                # Severity with color
                severity_item = QTableWidgetItem(alert['severity'].upper())
                if alert['severity'] == 'critical':
                    severity_item.setForeground(Qt.GlobalColor.red)
                elif alert['severity'] == 'warning':
                    severity_item.setForeground(Qt.GlobalColor.yellow)
                else:
                    severity_item.setForeground(Qt.GlobalColor.cyan)
                self.alerts_table.setItem(row, 0, severity_item)
                
                # Case info
                self.alerts_table.setItem(row, 1, QTableWidgetItem(alert['carpeta']))
                
                # Type
                type_names = {
                    'inactive': 'Sin actualización',
                    'prolonged_trial': 'Juicio prolongado',
                    'missing_denuncia': 'Sin denuncia',
                    'long_pending': 'Pendiente largo tiempo',
                    'arrest_warrant_pending': 'Orden de arresto pendiente',
                    'upcoming_citation': 'Citación próxima',
                    'citation_no_show': 'Citación no comparecida'
                }
                self.alerts_table.setItem(row, 2, QTableWidgetItem(type_names.get(alert['type'], alert['type'])))
                
                # Message
                self.alerts_table.setItem(row, 3, QTableWidgetItem(alert['message']))
                
                # Action button - properly sized and centered
                action_btn = QPushButton('Ver caso')
                action_btn.setFixedSize(120, 34)  # Wider button for complete text
                action_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #3b82f6, stop:1 #2563eb);
                        color: #ffffff;
                        border: none;
                        border-radius: 6px;
                        padding: 6px 10px;
                        font-weight: 600;
                        font-size: 12px;
                        text-align: center;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #60a5fa, stop:1 #3b82f6);
                    }
                    QPushButton:pressed {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #2563eb, stop:1 #1d4ed8);
                    }
                """)
                action_btn.clicked.connect(lambda checked, cid=alert['case_id']: self.view_case_from_alert(cid))
                
                # Center button using layout with alignment
                container = QWidget()
                container.setStyleSheet("background: transparent;")
                container_layout = QHBoxLayout(container)
                container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                container_layout.addWidget(action_btn)
                container_layout.setContentsMargins(0, 0, 0, 0)
                container_layout.setSpacing(0)
                
                self.alerts_table.setCellWidget(row, 4, container)
        
        except Exception as e:
            self._show_error_box(f'Error al cargar alertas: {str(e)}')
    
    def _update_alerts_summary(self, summary):
        """Update alerts summary cards"""
        # Get or create layout
        layout = self.alerts_summary_container.layout()
        if layout is None:
            layout = QHBoxLayout()
            layout.setSpacing(12)
            self.alerts_summary_container.setLayout(layout)
        else:
            # Clear existing widgets
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        
        # Total alerts
        layout.addWidget(self._build_metric_card(
            'Total Alertas',
            str(summary['total']),
            f"{summary['critical']} críticas"
        ))
        
        # Critical
        layout.addWidget(self._build_metric_card(
            'Críticas',
            str(summary['critical']),
            'Requieren atención inmediata',
            '#ef4444'
        ))
        
        # Warnings
        layout.addWidget(self._build_metric_card(
            'Advertencias',
            str(summary['warning']),
            'Revisar pronto',
            '#f59e0b'
        ))
        
        # Info
        layout.addWidget(self._build_metric_card(
            'Informativas',
            str(summary['info']),
            'Para conocimiento',
            '#3b82f6'
        ))
    
    def view_case_from_alert(self, case_id):
        """Navigate to case from alert and open it for editing"""
        try:
            # Get the case from database
            all_cases = self.controller.get_all_cases()
            case = None
            for c in all_cases:
                if hasattr(c, 'id') and c.id == case_id:
                    case = c
                    break
                elif isinstance(c, dict) and c.get('id') == case_id:
                    case = c
                    break
            
            if not case:
                self._show_error_box(f'No se encontró el caso con ID {case_id}')
                return
            
            # Switch to register tab
            self.tabs.setCurrentIndex(0)
            
            # Helper function to get attribute from Case object or dict
            def get_value(obj, key, default=''):
                if isinstance(obj, dict):
                    return obj.get(key, default)
                else:
                    return getattr(obj, key, default)
            
            # Load the case into the form
            self.current_edit_id = case_id
            self.numero_carpeta.setText(get_value(case, 'numero_carpeta'))

            categoria_val = get_value(case, 'categoria')
            if categoria_val in self.categories:
                idx = self.categories.index(categoria_val)
                self.categoria.setCurrentIndex(idx)
                self.categoria_custom.hide()
                self.categoria_custom.clear()
            else:
                self.categoria.setCurrentText('Otros')
                self.categoria_custom.show()
                self.categoria_custom.setText(categoria_val)

            self.etapa_procesal.setCurrentText(get_value(case, 'etapa_procesal'))
            self.victima.setText(get_value(case, 'victima'))
            self.investigado.setText(get_value(case, 'investigado'))

            def set_date(widget, value):
                if value:
                    widget.setDate(QDate.fromString(value, 'yyyy-MM-dd'))
                    widget.lineEdit().setText(widget.date().toString('yyyy-MM-dd'))
                else:
                    widget.setDate(self._date_min)
                    widget.lineEdit().setPlaceholderText('Seleccione')
                    widget.lineEdit().clear()

            set_date(self.fecha_denuncia, get_value(case, 'fecha_denuncia'))
            set_date(self.fecha_formalizacion, get_value(case, 'fecha_formalizacion'))
            set_date(self.fecha_acusacion, get_value(case, 'fecha_acusacion'))
            set_date(self.fecha_sentencia, get_value(case, 'fecha_sentencia'))
            set_date(self.fecha_archivo, get_value(case, 'fecha_archivo'))

            self.estado_actual.setCurrentText(get_value(case, 'estado_actual'))
            self.resultado.setCurrentText(get_value(case, 'resultado'))
            
            apelacion_val = get_value(case, 'apelacion', 0)
            self.apelacion.setChecked(apelacion_val == 1)
            self.fiscal_asignado.setText(get_value(case, 'fiscal_asignado'))
            self.fiscal_inicial.setText(get_value(case, 'fiscal_inicial'))
            
            # Departamento actual - safe handling
            depto_actual = get_value(case, 'departamento_actual', '')
            if depto_actual and depto_actual in [self.departamento_actual.itemText(i) for i in range(self.departamento_actual.count())]:
                self.departamento_actual.setCurrentText(depto_actual)
            else:
                self.departamento_actual.setCurrentIndex(0)  # Set to first item (usually empty or default)
            
            self.fiscal_cierre.setText(get_value(case, 'fiscal_cierre'))
            
            # Load citation data
            tiene_cita = get_value(case, 'tiene_citacion', 0)
            self.tiene_citacion.setChecked(tiene_cita == 1)
            set_date(self.fecha_emision_citacion, get_value(case, 'fecha_emision_citacion'))
            set_date(self.fecha_comparecencia, get_value(case, 'fecha_comparecencia'))
            
            # Estado citacion - safe handling
            estado_cita = get_value(case, 'estado_citacion', '')
            if estado_cita and estado_cita in [self.estado_citacion.itemText(i) for i in range(self.estado_citacion.count())]:
                self.estado_citacion.setCurrentText(estado_cita)
            else:
                self.estado_citacion.setCurrentIndex(0)
            
            self.observaciones_citacion.setPlainText(get_value(case, 'observaciones_citacion'))
            
            # Load arrest warrant data
            tiene_orden = get_value(case, 'tiene_orden_arresto', 0)
            self.tiene_orden_arresto.setChecked(tiene_orden == 1)
            
            # Origen orden arresto - safe handling
            origen_orden = get_value(case, 'origen_orden_arresto', '')
            if origen_orden and origen_orden in [self.origen_orden_arresto.itemText(i) for i in range(self.origen_orden_arresto.count())]:
                self.origen_orden_arresto.setCurrentText(origen_orden)
            else:
                self.origen_orden_arresto.setCurrentIndex(0)
            
            set_date(self.fecha_emision_orden, get_value(case, 'fecha_emision_orden'))
            
            # Estado orden - safe handling
            estado_orden = get_value(case, 'estado_orden', '')
            if estado_orden and estado_orden in [self.estado_orden.itemText(i) for i in range(self.estado_orden.count())]:
                self.estado_orden.setCurrentText(estado_orden)
            else:
                self.estado_orden.setCurrentIndex(0)
            
            set_date(self.fecha_cumplimiento_orden, get_value(case, 'fecha_cumplimiento_orden'))
            self.observaciones_orden.setPlainText(get_value(case, 'observaciones_orden'))
            
            if hasattr(self, 'save_button'):
                self.save_button.setText('✏️ Actualizar Carpeta')
            
            # Show success notification
            QMessageBox.information(
                self,
                '✓ Caso Cargado',
                f'Caso {get_value(case, "numero_carpeta")} cargado para edición.\n\n'
                f'Víctima: {get_value(case, "victima")}\n'
                f'Investigado: {get_value(case, "investigado")}\n'
                f'Estado: {get_value(case, "etapa_procesal")}'
            )
        except Exception as e:
            import traceback
            self._show_error_box(f'Error al cargar el caso: {str(e)}\n\n{traceback.format_exc()}')
    
    def _build_metric_card(self, title, value, detail, color='#3b82f6'):
        """Build a metric card with custom color"""
        frame = QFrame()
        frame.setObjectName('metric')
        frame.setStyleSheet(f"#metric {{ background: #111827; border: 1px solid #1e293b; border-radius: 10px; padding: 12px; }}")
        frame.setMinimumWidth(180)
        
        vbox = QVBoxLayout()
        vbox.setSpacing(4)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 14px; color: #9ca3af;")
        value_lbl = QLabel(value)
        value_lbl.setStyleSheet(f"font-size: 24px; font-weight: 800; color: {color};")
        detail_lbl = QLabel(detail)
        detail_lbl.setStyleSheet("font-size: 12px; color: #cbd5e1;")
        
        vbox.addWidget(title_lbl)
        vbox.addWidget(value_lbl)
        vbox.addWidget(detail_lbl)
        frame.setLayout(vbox)
        return frame

    def open_documents_dialog(self):
        """Open documents management dialog for selected case"""
        case_id = self.get_selected_case_id()
        if case_id is None:
            QMessageBox.information(self, 'Seleccionar', 'Seleccione un caso para ver sus documentos.')
            return
        
        # Get case info
        cases = self.controller.get_all_cases()
        case = next((c for c in cases if c.id == case_id), None)
        if not case:
            return
        
        # Create dialog
        from PyQt6.QtWidgets import QDialog, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f'Documentos - {case.numero_carpeta}')
        dialog.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        
        # Header
        header = QLabel(f'📁 Documentos de {case.numero_carpeta}')
        header.setStyleSheet('font-size: 18px; font-weight: 700; color: #60a5fa; margin-bottom: 8px;')
        layout.addWidget(header)
        
        case_info = QLabel(f'{case.categoria} • {case.victima} vs {case.investigado}')
        case_info.setStyleSheet('font-size: 13px; color: #94a3b8; margin-bottom: 12px;')
        layout.addWidget(case_info)
        
        # Documents table
        docs_table = QTableWidget()
        docs_table.setColumnCount(5)
        docs_table.setHorizontalHeaderLabels(['Archivo', 'Tamaño', 'Descripción', 'Fecha', 'Acciones'])
        docs_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        docs_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        docs_table.verticalHeader().setVisible(False)
        docs_table.setAlternatingRowColors(True)
        
        # Load documents
        documents = self.document_service.get_documents(case_id)
        docs_table.setRowCount(len(documents))
        
        for row, doc in enumerate(documents):
            doc_id, _, filename, original_filename, filepath, file_type, file_size, description, uploaded_at = doc
            
            # Filename
            docs_table.setItem(row, 0, QTableWidgetItem(original_filename))
            
            # Size
            size_str = self.document_service.format_file_size(file_size)
            docs_table.setItem(row, 1, QTableWidgetItem(size_str))
            
            # Description
            docs_table.setItem(row, 2, QTableWidgetItem(description or ''))
            
            # Date
            try:
                date = datetime.fromisoformat(uploaded_at)
                date_str = date.strftime('%Y-%m-%d %H:%M')
            except:
                date_str = uploaded_at
            docs_table.setItem(row, 3, QTableWidgetItem(date_str))
            
            # Actions buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(4, 2, 4, 2)
            actions_layout.setSpacing(4)
            
            open_btn = QPushButton('👁️')
            open_btn.setFixedSize(32, 28)
            open_btn.setToolTip('Abrir documento')
            open_btn.clicked.connect(lambda checked, d=doc_id: self.open_document(d))
            
            delete_btn = QPushButton('🗑️')
            delete_btn.setFixedSize(32, 28)
            delete_btn.setToolTip('Eliminar documento')
            delete_btn.clicked.connect(lambda checked, d=doc_id, t=docs_table: self.delete_document(d, t, case_id))
            
            actions_layout.addWidget(open_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()
            actions_widget.setLayout(actions_layout)
            
            docs_table.setCellWidget(row, 4, actions_widget)
        
        layout.addWidget(docs_table)
        
        # Storage info
        storage_info = self.document_service.get_storage_info()
        storage_label = QLabel(
            f"💾 Total: {storage_info['total_documents']} documentos • "
            f"{storage_info['total_size_formatted']}"
        )
        storage_label.setStyleSheet('font-size: 12px; color: #94a3b8; margin-top: 8px;')
        layout.addWidget(storage_label)
        
        # Add document button
        add_doc_btn = QPushButton('📎 Agregar Documento')
        add_doc_btn.clicked.connect(lambda: self.add_document_to_case(case_id, docs_table))
        add_doc_btn.setMinimumHeight(40)
        layout.addWidget(add_doc_btn)
        
        # Close button
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(dialog.close)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def add_document_to_case(self, case_id, table):
        """Add a document to a case"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            'Seleccionar Documento',
            '',
            'Todos los archivos (*.*);;PDF (*.pdf);;Word (*.doc *.docx);;Excel (*.xls *.xlsx);;Imágenes (*.jpg *.png *.gif)'
        )
        
        if not filepath:
            return
        
        # Ask for description
        from PyQt6.QtWidgets import QInputDialog
        description, ok = QInputDialog.getText(
            self,
            'Descripción del Documento',
            'Ingrese una descripción (opcional):',
            text=''
        )
        
        if not ok:
            description = ''
        
        try:
            # Add document
            doc_id = self.document_service.add_document(case_id, filepath, description)
            
            # Refresh table
            self.refresh_documents_table(case_id, table)
            
            QMessageBox.information(self, 'Éxito', 'Documento agregado exitosamente.')
        except Exception as e:
            self._show_error_box(f'Error al agregar documento:\n{str(e)}')
    
    def refresh_documents_table(self, case_id, table):
        """Refresh documents table"""
        documents = self.document_service.get_documents(case_id)
        table.setRowCount(len(documents))
        
        for row, doc in enumerate(documents):
            doc_id, _, filename, original_filename, filepath, file_type, file_size, description, uploaded_at = doc
            
            table.setItem(row, 0, QTableWidgetItem(original_filename))
            
            size_str = self.document_service.format_file_size(file_size)
            table.setItem(row, 1, QTableWidgetItem(size_str))
            
            table.setItem(row, 2, QTableWidgetItem(description or ''))
            
            try:
                date = datetime.fromisoformat(uploaded_at)
                date_str = date.strftime('%Y-%m-%d %H:%M')
            except:
                date_str = uploaded_at
            table.setItem(row, 3, QTableWidgetItem(date_str))
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(4, 2, 4, 2)
            actions_layout.setSpacing(4)
            
            open_btn = QPushButton('👁️')
            open_btn.setFixedSize(32, 28)
            open_btn.setToolTip('Abrir documento')
            open_btn.clicked.connect(lambda checked, d=doc_id: self.open_document(d))
            
            delete_btn = QPushButton('🗑️')
            delete_btn.setFixedSize(32, 28)
            delete_btn.setToolTip('Eliminar documento')
            delete_btn.clicked.connect(lambda checked, d=doc_id, t=table: self.delete_document(d, t, case_id))
            
            actions_layout.addWidget(open_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()
            actions_widget.setLayout(actions_layout)
            
            table.setCellWidget(row, 4, actions_widget)
    
    def open_document(self, doc_id):
        """Open a document"""
        try:
            self.document_service.open_document(doc_id)
        except Exception as e:
            self._show_error_box(f'Error al abrir documento:\n{str(e)}')
    
    def delete_document(self, doc_id, table, case_id):
        """Delete a document"""
        reply = QMessageBox.question(
            self,
            'Confirmar',
            '¿Está seguro de eliminar este documento?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.document_service.delete_document(doc_id)
                self.refresh_documents_table(case_id, table)
                QMessageBox.information(self, 'Éxito', 'Documento eliminado.')
            except Exception as e:
                self._show_error_box(f'Error al eliminar documento:\n{str(e)}')
    
    def show_fiscal_history(self):
        """Show fiscal transfer history dialog"""
        if not self.current_edit_id:
            QMessageBox.information(
                self,
                'Información',
                'Primero debe guardar el caso para ver el historial de transferencias.'
            )
            return
        
        from controllers.fiscal_history_controller import FiscalHistoryController
        from views.fiscal_history_dialog import FiscalHistoryDialog
        
        fiscal_controller = FiscalHistoryController()
        dialog = FiscalHistoryDialog(
            caso_id=self.current_edit_id,
            fiscal_controller=fiscal_controller,
            parent=self
        )
        dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())