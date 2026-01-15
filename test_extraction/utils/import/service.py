import pandas as pd
from datetime import datetime
from typing import List, Dict, Tuple
import os

class ImportService:
    """Service for bulk importing cases from CSV/Excel"""
    
    def __init__(self, controller):
        self.controller = controller
        self.required_columns = [
            'numero_carpeta',
            'categoria',
            'etapa_procesal',
            'victima',
            'investigado'
        ]
        self.optional_columns = [
            'fecha_denuncia',
            'fecha_formalizacion',
            'fecha_acusacion',
            'fecha_sentencia',
            'fecha_archivo',
            'monto_reparacion',
            'estado_actual',
            'resultado',
            'apelacion',
            'fiscal_asignado'
        ]
        self.all_columns = self.required_columns + self.optional_columns
    
    def validate_file(self, filepath: str) -> Tuple[bool, str, pd.DataFrame]:
        """Validate import file format and contents"""
        try:
            # Check file exists
            if not os.path.exists(filepath):
                return False, "El archivo no existe", None
            
            # Read file based on extension
            ext = os.path.splitext(filepath)[1].lower()
            if ext == '.csv':
                df = pd.read_csv(filepath)
            elif ext in ['.xlsx', '.xls']:
                df = pd.read_excel(filepath)
            else:
                return False, "Formato no soportado. Use CSV o Excel (.xlsx, .xls)", None
            
            # Check if file is empty
            if df.empty:
                return False, "El archivo está vacío", None
            
            # Check required columns
            missing_cols = [col for col in self.required_columns if col not in df.columns]
            if missing_cols:
                return False, f"Columnas requeridas faltantes: {', '.join(missing_cols)}", None
            
            # Check for duplicate carpeta numbers in file
            if df['numero_carpeta'].duplicated().any():
                duplicates = df[df['numero_carpeta'].duplicated()]['numero_carpeta'].tolist()
                return False, f"Números de carpeta duplicados en el archivo: {', '.join(map(str, duplicates[:5]))}", None
            
            return True, f"Archivo válido con {len(df)} registros", df
            
        except Exception as e:
            return False, f"Error al leer archivo: {str(e)}", None
    
    def preview_import(self, df: pd.DataFrame, limit: int = 10) -> List[Dict]:
        """Generate preview of data to be imported"""
        preview_df = df.head(limit)
        return preview_df.to_dict('records')
    
    def import_cases(self, df: pd.DataFrame, skip_duplicates: bool = True) -> Tuple[int, int, List[str]]:
        """
        Import cases from dataframe
        Returns: (successful_count, skipped_count, error_messages)
        """
        successful = 0
        skipped = 0
        errors = []
        
        for idx, row in df.iterrows():
            try:
                # Check if carpeta already exists
                numero_carpeta = str(row.get('numero_carpeta', '')).strip()
                if not numero_carpeta:
                    errors.append(f"Fila {idx+2}: Número de carpeta vacío")
                    continue
                
                existing = self.controller.db.get_case_by_carpeta(numero_carpeta)
                if existing:
                    if skip_duplicates:
                        skipped += 1
                        continue
                    else:
                        errors.append(f"Fila {idx+2}: Carpeta {numero_carpeta} ya existe")
                        continue
                
                # Prepare case data
                case_data = self._prepare_case_data(row, idx)
                
                # Validate and insert
                self.controller.add_case(case_data)
                successful += 1
                
            except ValueError as e:
                errors.append(f"Fila {idx+2} ({numero_carpeta}): {str(e)}")
            except Exception as e:
                errors.append(f"Fila {idx+2}: Error inesperado - {str(e)}")
        
        return successful, skipped, errors
    
    def _prepare_case_data(self, row, idx) -> tuple:
        """Prepare case data tuple from dataframe row"""
        def safe_get(col, default=''):
            val = row.get(col, default)
            return str(val).strip() if pd.notna(val) and str(val).strip() != 'nan' else default
        
        def safe_date(col):
            val = row.get(col, '')
            if pd.isna(val) or str(val).strip() in ['', 'nan', 'NaT']:
                return ''
            # Try to parse as date
            try:
                dt = pd.to_datetime(val)
                return dt.strftime('%Y-%m-%d')
            except:
                return ''
        
        def safe_float(col, default=0.0):
            val = row.get(col, default)
            if pd.isna(val) or str(val).strip() in ['', 'nan']:
                return default
            try:
                return float(val)
            except:
                return default
        
        def safe_bool(col):
            val = row.get(col, 0)
            if pd.isna(val):
                return 0
            if isinstance(val, (bool, int)):
                return 1 if val else 0
            val_str = str(val).lower().strip()
            return 1 if val_str in ['1', 'true', 'sí', 'si', 'yes', 'verdadero'] else 0
        
        # Build case data tuple
        case_data = (
            safe_get('numero_carpeta'),
            safe_get('categoria'),
            safe_get('etapa_procesal'),
            safe_get('victima'),
            safe_get('investigado'),
            safe_date('fecha_denuncia'),
            safe_date('fecha_formalizacion'),
            safe_date('fecha_acusacion'),
            safe_date('fecha_sentencia'),
            safe_date('fecha_archivo'),
            safe_float('monto_reparacion'),
            safe_get('estado_actual'),
            safe_get('resultado'),
            safe_bool('apelacion'),
            safe_get('fiscal_asignado')
        )
        
        return case_data
    
    def generate_template(self, filepath: str, format: str = 'excel'):
        """Generate import template file"""
        template_data = {
            'numero_carpeta': ['RUC-2024-001-EJEMPLO'],
            'categoria': ['Delitos contra la propiedad'],
            'etapa_procesal': ['Investigación'],
            'victima': ['Juan Pérez'],
            'investigado': ['María García'],
            'fecha_denuncia': ['2024-01-15'],
            'fecha_formalizacion': [''],
            'fecha_acusacion': [''],
            'fecha_sentencia': [''],
            'fecha_archivo': [''],
            'monto_reparacion': [0],
            'estado_actual': ['Investigación'],
            'resultado': [''],
            'apelacion': [0],
            'fiscal_asignado': ['Fiscal Ejemplo']
        }
        
        df = pd.DataFrame(template_data)
        
        if format == 'excel':
            df.to_excel(filepath, index=False, sheet_name='Casos')
        else:
            df.to_csv(filepath, index=False)
        
        return filepath
