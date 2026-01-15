from datetime import datetime, timedelta
from typing import List, Dict

class NotificationManager:
    """Manage notifications and alerts for cases"""
    
    def __init__(self):
        self.notifications = []
    
    def check_case_alerts(self, cases) -> List[Dict]:
        """Check all cases and generate alerts"""
        alerts = []
        today = datetime.now().date()
        
        for case in cases:
            # Alert: Cases without updates in 30+ days
            if case.updated_at:
                try:
                    updated = datetime.fromisoformat(str(case.updated_at)).date()
                    days_since_update = (today - updated).days
                    
                    if days_since_update >= 30:
                        alerts.append({
                            'type': 'inactive',
                            'severity': 'warning',
                            'case_id': case.id,
                            'carpeta': case.numero_carpeta,
                            'message': f'Sin actualización hace {days_since_update} días',
                            'days': days_since_update
                        })
                except (ValueError, AttributeError):
                    pass
            
            # Alert: Cases in "En juicio" stage for 90+ days
            if case.estado_actual == 'En juicio' and case.fecha_acusacion:
                try:
                    fecha_acusacion = datetime.strptime(case.fecha_acusacion, '%Y-%m-%d').date()
                    days_in_trial = (today - fecha_acusacion).days
                    
                    if days_in_trial >= 90:
                        alerts.append({
                            'type': 'prolonged_trial',
                            'severity': 'warning',
                            'case_id': case.id,
                            'carpeta': case.numero_carpeta,
                            'message': f'En juicio hace {days_in_trial} días',
                            'days': days_in_trial
                        })
                except (ValueError, AttributeError):
                    pass
            
            # Alert: Cases without denuncia date
            if not case.fecha_denuncia:
                alerts.append({
                    'type': 'missing_denuncia',
                    'severity': 'info',
                    'case_id': case.id,
                    'carpeta': case.numero_carpeta,
                    'message': 'Sin fecha de denuncia registrada',
                    'days': 0
                })
            
            # Alert: Pending cases (no archivo/sentencia) older than 180 days
            if case.estado_actual in ['Investigación', 'Formalizado'] and case.fecha_denuncia:
                try:
                    fecha_denuncia = datetime.strptime(case.fecha_denuncia, '%Y-%m-%d').date()
                    days_pending = (today - fecha_denuncia).days
                    
                    if days_pending >= 180:
                        alerts.append({
                            'type': 'long_pending',
                            'severity': 'critical',
                            'case_id': case.id,
                            'carpeta': case.numero_carpeta,
                            'message': f'Caso pendiente hace {days_pending} días',
                            'days': days_pending
                        })
                except (ValueError, AttributeError):
                    pass
            
            # Alert: Arrest warrants pending fulfillment
            tiene_orden = getattr(case, 'tiene_orden_arresto', 0)
            estado_orden = getattr(case, 'estado_orden', '')
            fecha_emision = getattr(case, 'fecha_emision_orden', '')
            
            if tiene_orden == 1 and estado_orden == 'Pendiente de cumplimiento' and fecha_emision:
                try:
                    emision = datetime.strptime(fecha_emision, '%Y-%m-%d').date()
                    days_pending = (today - emision).days
                    
                    # Critical if pending more than 30 days
                    severity = 'critical' if days_pending >= 30 else 'warning'
                    
                    alerts.append({
                        'type': 'arrest_warrant_pending',
                        'severity': severity,
                        'case_id': case.id,
                        'carpeta': case.numero_carpeta,
                        'message': f'Orden de arresto pendiente hace {days_pending} días',
                        'days': days_pending
                    })
                except (ValueError, AttributeError):
                    pass
            
            # Alert: Upcoming citations (7 days or less)
            tiene_cita = getattr(case, 'tiene_citacion', 0)
            estado_cita = getattr(case, 'estado_citacion', '')
            fecha_comparecencia = getattr(case, 'fecha_comparecencia', '')
            
            if tiene_cita == 1 and estado_cita == 'Pendiente' and fecha_comparecencia:
                try:
                    comparecencia = datetime.strptime(fecha_comparecencia, '%Y-%m-%d').date()
                    days_until = (comparecencia - today).days
                    
                    # Alert if 7 days or less until citation
                    if 0 <= days_until <= 7:
                        severity = 'critical' if days_until <= 2 else 'warning'
                        
                        if days_until == 0:
                            message = 'Citación programada para hoy'
                        elif days_until == 1:
                            message = 'Citación mañana'
                        else:
                            message = f'Citación en {days_until} días'
                        
                        alerts.append({
                            'type': 'upcoming_citation',
                            'severity': severity,
                            'case_id': case.id,
                            'carpeta': case.numero_carpeta,
                            'message': message,
                            'days': days_until
                        })
                except (ValueError, AttributeError):
                    pass
            
            # Alert: Missed citations (no show)
            if tiene_cita == 1 and estado_cita == 'No compareció':
                fecha_emision_cita = getattr(case, 'fecha_emision_citacion', '')
                
                if fecha_emision_cita:
                    try:
                        emision_cita = datetime.strptime(fecha_emision_cita, '%Y-%m-%d').date()
                        days_since = (today - emision_cita).days
                        
                        # Suggest arrest warrant if no show and no arrest warrant yet
                        if tiene_orden == 0:
                            alerts.append({
                                'type': 'citation_no_show',
                                'severity': 'critical',
                                'case_id': case.id,
                                'carpeta': case.numero_carpeta,
                                'message': f'No compareció a citación - Considerar orden de arresto',
                                'days': days_since
                            })
                        else:
                            alerts.append({
                                'type': 'citation_no_show',
                                'severity': 'warning',
                                'case_id': case.id,
                                'carpeta': case.numero_carpeta,
                                'message': f'No compareció a citación hace {days_since} días',
                                'days': days_since
                            })
                    except (ValueError, AttributeError):
                        pass
        
        # Sort by severity and days
        severity_order = {'critical': 0, 'warning': 1, 'info': 2}
        alerts.sort(key=lambda x: (severity_order.get(x['severity'], 3), -x['days']))
        
        return alerts
    
    def get_alert_summary(self, alerts: List[Dict]) -> Dict:
        """Get summary of alerts by type and severity"""
        summary = {
            'total': len(alerts),
            'critical': sum(1 for a in alerts if a['severity'] == 'critical'),
            'warning': sum(1 for a in alerts if a['severity'] == 'warning'),
            'info': sum(1 for a in alerts if a['severity'] == 'info'),
            'by_type': {}
        }
        
        for alert in alerts:
            alert_type = alert['type']
            summary['by_type'][alert_type] = summary['by_type'].get(alert_type, 0) + 1
        
        return summary
