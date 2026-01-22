# -*- coding: utf-8 -*-
from database.db import Database
from models.case import Case
import pandas as pd
from datetime import datetime, timedelta
from functools import wraps

def cache_with_ttl(ttl_seconds=300):
    """Decorator for caching results with time-to-live"""
    def decorator(func):
        cache = {}
        
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            cache_key = f"{func.__name__}_{args}_{kwargs}"
            now = datetime.now()
            
            if cache_key in cache:
                result, timestamp = cache[cache_key]
                if now - timestamp < timedelta(seconds=ttl_seconds):
                    return result
            
            result = func(self, *args, **kwargs)
            cache[cache_key] = (result, now)
            return result
        
        wrapper.clear_cache = lambda: cache.clear()
        return wrapper
    return decorator

class CaseController:
    def __init__(self):
        self.db = Database()
    
    def invalidate_caches(self):
        """Manually invalidate all caches"""
        if hasattr(self.get_all_cases, 'clear_cache'):
            self.get_all_cases.clear_cache()
        if hasattr(self.get_statistics, 'clear_cache'):
            self.get_statistics.clear_cache()
        if hasattr(self.search_cases_advanced, 'clear_cache'):
            self.search_cases_advanced.clear_cache()
        if hasattr(self.get_unique_fiscales, 'clear_cache'):
            self.get_unique_fiscales.clear_cache()
        if hasattr(self.get_unique_victimas, 'clear_cache'):
            self.get_unique_victimas.clear_cache()
        if hasattr(self.get_unique_investigados, 'clear_cache'):
            self.get_unique_investigados.clear_cache()

    def add_case(self, case_data):
        self._validate_case_data(case_data)
        # Uniqueness check
        existing = self.db.get_case_by_carpeta(case_data[0])
        if existing:
            raise ValueError('El número de carpeta ya existe.')
        case = Case(*case_data)
        case_id = self.db.insert_case(case.to_tuple())
        # Clear statistics cache after adding
        self.invalidate_caches()
        return case_id

    @cache_with_ttl(ttl_seconds=60)
    def get_all_cases(self):
        rows = self.db.get_all_cases()
        return [Case.from_row(row) for row in rows]

    def update_case(self, case_id, case_data):
        self._validate_case_data(case_data, is_update=True, case_id=case_id)
        # Check uniqueness if carpeta changes
        existing = self.db.get_case_by_carpeta(case_data[0])
        if existing and existing[0] != case_id:
            raise ValueError('El número de carpeta ya existe en otro registro.')
        self.db.update_case(case_id, case_data)
        # Clear caches after update
        self.invalidate_caches()

    def delete_case(self, case_id):
        self.db.delete_case(case_id)
        # Clear caches after delete
        self.invalidate_caches()

    def search_cases(self, filters):
        # Implement filtering
        all_cases = self.get_all_cases()
        # Apply filters
        return all_cases
    
    @cache_with_ttl(ttl_seconds=120)
    def search_cases_advanced(self, **filters):
        """Advanced search with multiple filter combinations"""
        cases = self.get_all_cases()
        filtered = cases
        
        # Text search across multiple fields
        if filters.get('text_query'):
            query = filters['text_query'].lower()
            filtered = [c for c in filtered if 
                       query in (c.numero_carpeta or '').lower() or
                       query in (c.victima or '').lower() or
                       query in (c.investigado or '').lower() or
                       query in (c.fiscal_asignado or '').lower()]
        
        # Category filter
        if filters.get('categoria') and filters['categoria'] != 'Todas':
            filtered = [c for c in filtered if c.categoria == filters['categoria']]
        
        # State filter
        if filters.get('estado') and filters['estado'] != 'Todos':
            filtered = [c for c in filtered if c.estado_actual == filters['estado']]
        
        # Fiscal filter
        if filters.get('fiscal'):
            fiscal_query = filters['fiscal'].lower()
            filtered = [c for c in filtered if 
                       fiscal_query in (c.fiscal_asignado or '').lower()]
        
        # Date range filter
        if filters.get('fecha_desde'):
            filtered = [c for c in filtered if 
                       c.fecha_denuncia and c.fecha_denuncia >= filters['fecha_desde']]
        
        if filters.get('fecha_hasta'):
            filtered = [c for c in filtered if 
                       c.fecha_denuncia and c.fecha_denuncia <= filters['fecha_hasta']]
        
        # Apelacion filter
        if filters.get('solo_apelados'):
            filtered = [c for c in filtered if c.apelacion == 1]
        
        return filtered

    @cache_with_ttl(ttl_seconds=300)
    def get_unique_fiscales(self):
        """Get list of unique fiscal names for autocomplete"""
        conn = self.db.get_connection()
        cursor = conn.execute(
            "SELECT DISTINCT fiscal_asignado FROM cases WHERE fiscal_asignado IS NOT NULL AND fiscal_asignado != '' ORDER BY fiscal_asignado"
        )
        return [row[0] for row in cursor.fetchall()]
    
    @cache_with_ttl(ttl_seconds=300)
    def get_unique_victimas(self):
        """Get list of unique victim names for autocomplete"""
        conn = self.db.get_connection()
        cursor = conn.execute(
            "SELECT DISTINCT victima FROM cases WHERE victima IS NOT NULL AND victima != '' ORDER BY victima"
        )
        return [row[0] for row in cursor.fetchall()]
    
    @cache_with_ttl(ttl_seconds=300)
    def get_unique_investigados(self):
        """Get list of unique investigado names for autocomplete"""
        conn = self.db.get_connection()
        cursor = conn.execute(
            "SELECT DISTINCT investigado FROM cases WHERE investigado IS NOT NULL AND investigado != '' ORDER BY investigado"
        )
        return [row[0] for row in cursor.fetchall()]

    @cache_with_ttl(ttl_seconds=300)
    def get_statistics(self):
        cases = self.get_all_cases()
        if not cases:
            return {
                'resolved': 0,
                'pending': 0,
                'avg_resolution_time': 0,
                'cases_by_category': {},
                'cases_by_estado': {},
                'cases_by_etapa': {},
                'appeal_percentage': 0,
                'appeal_count': 0,
                'cases_per_month': {},
                'by_judge': {},
                'success_rate': 0,
                'closed_per_quarter': {},
                'avg_delay': 0,
            }

        df = pd.DataFrame([vars(c) for c in cases])
        stats = {}

        resolved_states = ['Sentencia', 'Archivo definitivo', 'Sobreseimiento', 'Condena', 'Absolución']
        stats['resolved'] = len(df[df['estado_actual'].isin(resolved_states)])
        stats['pending'] = len(df[~df['estado_actual'].isin(resolved_states)])

        df['fecha_denuncia'] = pd.to_datetime(df['fecha_denuncia'], errors='coerce')
        df['fecha_archivo'] = pd.to_datetime(df['fecha_archivo'], errors='coerce')
        df['resolution_time'] = (df['fecha_archivo'] - df['fecha_denuncia']).dt.days
        stats['avg_resolution_time'] = df['resolution_time'].mean()

        stats['cases_by_category'] = df['categoria'].value_counts().to_dict()
        stats['cases_by_estado'] = df['estado_actual'].value_counts().to_dict()
        stats['cases_by_etapa'] = df['etapa_procesal'].value_counts().to_dict()
        stats['appeal_percentage'] = df['apelacion'].mean() * 100
        stats['appeal_count'] = int(df['apelacion'].sum())

        df['month'] = df['fecha_denuncia'].dt.to_period('M')
        month_counts = df['month'].value_counts().sort_index()
        stats['cases_per_month'] = {str(k): v for k, v in month_counts.items()}

        stats['by_judge'] = df['fiscal_asignado'].value_counts().to_dict()

        success_cases = len(df[df['resultado'].isin(['Condena', 'Acuerdo', 'Conciliación'])])
        stats['success_rate'] = (success_cases / len(df)) * 100 if len(df) > 0 else 0

        df['quarter'] = df['fecha_archivo'].dt.to_period('Q')
        quarter_counts = df[df['estado_actual'].isin(resolved_states)]['quarter'].value_counts().sort_index()
        stats['closed_per_quarter'] = {str(k): v for k, v in quarter_counts.items()}

        df['fecha_formalizacion'] = pd.to_datetime(df['fecha_formalizacion'], errors='coerce')
        df['delay'] = (df['fecha_archivo'] - df['fecha_formalizacion']).dt.days
        stats['avg_delay'] = df['delay'].mean()
        return stats

    def _validate_case_data(self, case_data, is_update=False, case_id=None):
        (
            numero_carpeta,
            categoria,
            etapa_procesal,
            victima,
            investigado,
            fecha_denuncia,
            fecha_formalizacion,
            fecha_acusacion,
            fecha_sentencia,
            fecha_archivo,
            estado_actual,
            resultado,
            apelacion,
            fiscal_asignado,
            tiene_citacion,
            fecha_emision_citacion,
            fecha_comparecencia,
            estado_citacion,
            observaciones_citacion,
            tiene_orden_arresto,
            fecha_emision_orden,
            estado_orden,
            fecha_cumplimiento_orden,
            observaciones_orden,
            origen_orden_arresto,
            fiscal_inicial,
            departamento_actual,
            fiscal_cierre,
            monto_pension,
        ) = case_data

        if not numero_carpeta or not numero_carpeta.strip():
            raise ValueError('El número de carpeta es obligatorio.')

        # Date ordering: denuncia <= formalización <= acusación <= sentencia/archivo
        import pandas as pd

        def to_ts(val):
            ts = pd.to_datetime(val, errors='coerce')
            return None if pd.isna(ts) else ts

        fd = to_ts(fecha_denuncia)
        ff = to_ts(fecha_formalizacion)
        fa = to_ts(fecha_acusacion)
        fs = to_ts(fecha_sentencia)
        far = to_ts(fecha_archivo)

        def strictly_after(a, b):
            # True if either date missing or b occurs after a (no mismo día)
            return (a is None) or (b is None) or (b > a)

        if fd is not None and ff is not None and not strictly_after(fd, ff):
            raise ValueError('La formalización debe ser posterior a la denuncia (no el mismo día).')
        if ff is not None and fa is not None and not strictly_after(ff, fa):
            raise ValueError('La acusación debe ser posterior a la formalización (no el mismo día).')
        if fa is not None and fs is not None and not strictly_after(fa, fs):
            raise ValueError('La sentencia debe ser posterior a la acusación (no el mismo día).')
        if fd is not None and fs is not None and not strictly_after(fd, fs):
            raise ValueError('La sentencia debe ser posterior a la denuncia (no el mismo día).')
        if fd is not None and far is not None and not strictly_after(fd, far):
            raise ValueError('El archivo/cierre debe ser posterior a la denuncia (no el mismo día).')
        if fa is not None and far is not None and not strictly_after(fa, far):
            raise ValueError('El archivo/cierre debe ser posterior a la acusación (no el mismo día).')

    def export_data(self, filepath, format='csv', cases=None):
        data = cases if cases is not None else self.get_all_cases()
        df = pd.DataFrame([vars(c) for c in data])
        if format == 'csv':
            df.to_csv(filepath, index=False)
        elif format == 'excel':
            df.to_excel(filepath, index=False)