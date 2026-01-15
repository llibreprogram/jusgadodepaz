class FiscalHistory:
    """Model for fiscal transfer history"""
    
    def __init__(self, caso_id, fiscal_nombre, departamento, accion,
                 fiscal_destino=None, departamento_destino=None, motivo=None,
                 fecha_movimiento=None, observaciones=None, id=None, created_at=None):
        self.id = id
        self.caso_id = caso_id
        self.fiscal_nombre = fiscal_nombre
        self.departamento = departamento
        self.accion = accion  # 'Recepción inicial', 'Declinación', 'Transferencia', 'Cierre'
        self.fiscal_destino = fiscal_destino
        self.departamento_destino = departamento_destino
        self.motivo = motivo
        self.fecha_movimiento = fecha_movimiento
        self.observaciones = observaciones
        self.created_at = created_at
    
    def to_tuple(self):
        """Convert to tuple for database insertion"""
        return (
            self.caso_id,
            self.fiscal_nombre,
            self.departamento,
            self.accion,
            self.fiscal_destino,
            self.departamento_destino,
            self.motivo,
            self.fecha_movimiento,
            self.observaciones
        )
    
    @staticmethod
    def from_row(row):
        """Create FiscalHistory from database row"""
        return FiscalHistory(
            caso_id=row[1],
            fiscal_nombre=row[2],
            departamento=row[3],
            accion=row[4],
            fiscal_destino=row[5] if len(row) > 5 else None,
            departamento_destino=row[6] if len(row) > 6 else None,
            motivo=row[7] if len(row) > 7 else None,
            fecha_movimiento=row[8] if len(row) > 8 else None,
            observaciones=row[9] if len(row) > 9 else None,
            id=row[0],
            created_at=row[10] if len(row) > 10 else None
        )
    
    def get_action_icon(self):
        """Get emoji icon for action type"""
        icons = {
            'Recepción inicial': '📥',
            'Declinación': '↪️',
            'Transferencia': '🔄',
            'Cierre': '✅'
        }
        return icons.get(self.accion, '📋')
    
    def get_action_color(self):
        """Get color for action type"""
        colors = {
            'Recepción inicial': '#10b981',  # green
            'Declinación': '#f59e0b',  # amber
            'Transferencia': '#3b82f6',  # blue
            'Cierre': '#6366f1'  # indigo
        }
        return colors.get(self.accion, '#64748b')
