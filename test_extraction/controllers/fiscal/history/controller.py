from database.db import Database
from models.fiscal_history import FiscalHistory
from datetime import datetime

class FiscalHistoryController:
    """Controller for managing fiscal transfer history"""
    
    def __init__(self):
        self.db = Database()
    
    def add_history(self, caso_id, fiscal_nombre, departamento, accion,
                    fiscal_destino=None, departamento_destino=None, 
                    motivo=None, observaciones=None):
        """Add a new fiscal history entry"""
        fecha_movimiento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        history = FiscalHistory(
            caso_id=caso_id,
            fiscal_nombre=fiscal_nombre,
            departamento=departamento,
            accion=accion,
            fiscal_destino=fiscal_destino,
            departamento_destino=departamento_destino,
            motivo=motivo,
            fecha_movimiento=fecha_movimiento,
            observaciones=observaciones
        )
        
        return self.db.insert_fiscal_history(history.to_tuple())
    
    def get_case_history(self, caso_id):
        """Get all history entries for a case"""
        rows = self.db.get_fiscal_history(caso_id)
        return [FiscalHistory.from_row(row) for row in rows]
    
    def delete_history(self, history_id):
        """Delete a history entry"""
        self.db.delete_fiscal_history(history_id)
    
    def get_statistics(self):
        """Get fiscal transfer statistics"""
        return self.db.get_fiscal_statistics()
    
    def record_initial_reception(self, caso_id, fiscal_nombre, departamento, observaciones=None):
        """Record initial case reception by a fiscal"""
        return self.add_history(
            caso_id=caso_id,
            fiscal_nombre=fiscal_nombre,
            departamento=departamento,
            accion='Recepción inicial',
            observaciones=observaciones
        )
    
    def record_transfer(self, caso_id, fiscal_origen, departamento_origen,
                       fiscal_destino, departamento_destino, motivo, observaciones=None):
        """Record a case transfer/declination between fiscals"""
        accion = 'Declinación' if motivo and 'declin' in motivo.lower() else 'Transferencia'
        
        return self.add_history(
            caso_id=caso_id,
            fiscal_nombre=fiscal_origen,
            departamento=departamento_origen,
            accion=accion,
            fiscal_destino=fiscal_destino,
            departamento_destino=departamento_destino,
            motivo=motivo,
            observaciones=observaciones
        )
    
    def record_closure(self, caso_id, fiscal_nombre, departamento, observaciones=None):
        """Record case closure by a fiscal"""
        return self.add_history(
            caso_id=caso_id,
            fiscal_nombre=fiscal_nombre,
            departamento=departamento,
            accion='Cierre',
            observaciones=observaciones
        )
    
    def get_fiscal_summary(self, fiscal_nombre):
        """Get summary of cases for a specific fiscal"""
        stats = self.get_statistics()
        
        return {
            'recibidos': stats.get('recibidos', {}).get(fiscal_nombre, 0),
            'asignados': stats.get('asignados', {}).get(fiscal_nombre, 0),
            'cerrados': stats.get('cerrados', {}).get(fiscal_nombre, 0),
            'declinados': stats.get('declinaciones_salida', {}).get(fiscal_nombre, 0),
            'recibidos_por_declinacion': stats.get('declinaciones_entrada', {}).get(fiscal_nombre, 0)
        }
